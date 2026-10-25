"""Pair local papers with Chinese PDFs using the official DeepL SDK."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "pdf"
OUTPUT = SOURCE / "zh"
STATE = BASE / ".state"


def write_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def pdf_info(path):
    from pypdf import PdfReader

    with path.open("rb") as stream:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
        digest = hasher.hexdigest()
    with path.open("rb") as stream:
        reader = PdfReader(stream)
        text = [page.extract_text() or "" for page in reader.pages]
    if not text:
        raise ValueError(f"Empty PDF: {path.name}")
    return {
        "pages": len(text),
        "bytes": path.stat().st_size,
        "sha256": digest,
        "low_text_pages": [i + 1 for i, t in enumerate(text) if len(t.strip()) < 20],
        "chinese_characters": sum("\u4e00" <= c <= "\u9fff" for t in text for c in t),
    }


def destination(source):
    return OUTPUT / (source.stem + ".zh-CN.deepl.pdf")


def translate_one(client, deepl, source, source_info, glossary):
    output = destination(source)
    record_path = output.with_suffix(".translation.json")
    if output.exists():
        if not record_path.exists():
            raise RuntimeError(f"Output has no provenance record: {output.name}")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if record["source_sha256"] != source_info["sha256"]:
            raise RuntimeError(f"Source changed for existing output: {source.name}")
        if pdf_info(output)["sha256"] != record["output_sha256"]:
            raise RuntimeError(f"Output changed; review its provenance: {output.name}")
        print(f"SKIP {output.name} (existing translation; review separately)", flush=True)
        return

    job_path = STATE / (source.stem + ".json")
    if job_path.exists():
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if job["source_sha256"] != source_info["sha256"] or job["glossary_id"] != glossary:
            raise RuntimeError(f"Source or glossary differs from saved task: {source.name}")
        if "document_id" not in job or job["stage"] == "downloading":
            raise RuntimeError(f"Uncertain upload/download; inspect saved task before retry: {source.name}")
        handle = deepl.DocumentHandle(job["document_id"], job["document_key"])
    else:
        # Persist before uploading: an uncertain response must not trigger a new billable upload.
        job = {"source_sha256": source_info["sha256"], "glossary_id": glossary, "stage": "uploading"}
        write_json(job_path, job)
        with source.open("rb") as stream:
            handle = client.translate_document_upload(
                stream, source_lang="EN", target_lang="ZH-HANS",
                output_format="pdf", glossary=glossary,
            )
        job.update(document_id=handle.document_id, document_key=handle.document_key, stage="uploaded")
        write_json(job_path, job)

    print(f"WAIT {source.name}", flush=True)
    status = client.translate_document_wait_until_done(handle, timeout_s=1800)
    if not status.ok or not status.done:
        raise RuntimeError(f"Service task not downloadable: {source.name}")
    job["stage"] = "downloading"
    write_json(job_path, job)
    temp_pdf = STATE / (source.stem + ".download.pdf")
    with temp_pdf.open("wb") as stream:
        client.translate_document_download(handle, stream, chunk_size=65536)
    result = pdf_info(temp_pdf)
    if result["chinese_characters"] < 50:
        raise RuntimeError(f"Downloaded PDF needs manual Chinese-text verification: {source.name}")
    record = {
        "provider": "DeepL official API", "translation_type": "machine_translation",
        "review_status": "pending_review", "source_file": source.name,
        "source_sha256": source_info["sha256"], "source_pages": source_info["pages"],
        "target_language": "ZH-HANS", "glossary_id": glossary,
        "output_sha256": result["sha256"], "output_pages": result["pages"],
        "billed_characters": status.billed_characters,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(record_path, record)
    temp_pdf.replace(output)
    job_path.unlink()
    print(f"SAVED {output.name} (pending content and visual review)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--match", default="", help="Filename substring to select papers")
    parser.add_argument("--inventory", action="store_true", help="Write local inventory.json")
    parser.add_argument("--run", action="store_true", help="Upload full PDFs and consume DeepL quota")
    parser.add_argument("--glossary-id", help="Existing DeepL glossary with an English-Chinese dictionary")
    args = parser.parse_args()
    files = [p for p in sorted(SOURCE.glob("*.pdf")) if args.match.casefold() in p.name.casefold()]
    if not files:
        parser.error("No matching source PDFs")
    if args.inventory and args.match:
        parser.error("--inventory requires the complete, unfiltered collection")
    rows = []
    for source in files:
        info = pdf_info(source)
        output = destination(source)
        rows.append({"source_file": source.name, **info, "planned_output": "zh/" + output.name,
                     "output_present": output.exists()})
        print(f"{info['pages']:2} pages | {source.name} -> {output.name}", flush=True)
    print(f"{len(rows)} PDFs, {sum(r['pages'] for r in rows)} pages.")
    if args.inventory:
        write_json(BASE / "inventory.json", {"checked_at": datetime.now(timezone.utc).isoformat(), "papers": rows})
    if not args.run:
        print("Local check only. No document uploaded or translated.")
        return 0

    auth_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not auth_key:
        parser.error("No DeepL API key configured locally. No documents were uploaded.")
    import deepl

    STATE.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)
    lock = STATE / "run.lock"
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        parser.error("run.lock exists; confirm the previous process has stopped before removing it")
    os.close(lock_fd)
    client = None
    try:
        client = deepl.DeepLClient(auth_key, send_platform_info=False)
        if "ZH-HANS" not in {language.code.upper() for language in client.get_target_languages()}:
            raise RuntimeError("Simplified Chinese is unavailable for this API account")
        for source, info in zip(files, rows):
            translate_one(client, deepl, source, info, args.glossary_id)
    finally:
        if client is not None:
            client.close()
        lock.unlink()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Stopped. Saved task state retained; rerun to resume where possible.", file=sys.stderr)
        sys.exit(130)
    except Exception as error:
        # Service errors can contain document keys; do not echo remote error bodies.
        print(f"Stopped ({type(error).__name__}). Inspect local inputs and saved task state.", file=sys.stderr)
        sys.exit(1)
