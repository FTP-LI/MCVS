"""MCVS first exercise: standard library only; all data are teaching examples.

Run: python doc/learning/examples/first_steps.py
Edit only the three constants below for the first-week exercise.
"""

from math import isfinite

FPS = 30
POINT_Z_M = 2.0
DISPARITY_PX = 30.0


def positive(value, name):
    """Reject invalid physical inputs rather than silently invent a result."""
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def frame_interval_ms(fps):
    return 1000.0 / positive(fps, "fps")


def raw_bytes_per_second(cameras, width, height, bytes_per_pixel, fps):
    """Ideal uncompressed payload only: no padding, headers or compression."""
    values = ((cameras, "cameras"), (width, "width"), (height, "height"),
              (bytes_per_pixel, "bytes_per_pixel"), (fps, "fps"))
    result = 1.0
    for value, name in values:
        result *= positive(value, name)
    return result


def project_u(fx_px, x_m, z_m, cx_px):
    """Ideal pinhole, no distortion, point in front of the camera."""
    return positive(fx_px, "fx_px") * x_m / positive(z_m, "z_m") + cx_px


def stereo_depth_m(focal_px, baseline_m, disparity_px):
    """Calibrated, rectified parallel stereo under the stated convention."""
    return (positive(focal_px, "focal_px") * positive(baseline_m, "baseline_m")
            / positive(disparity_px, "disparity_px"))


def main():
    print("Teaching calculations; these are NOT measurements of your devices.")
    print(f"frame interval: {frame_interval_ms(FPS):.3f} ms")
    rate = raw_bytes_per_second(2, 1280, 720, 1, FPS)
    print(f"raw payload: {rate:,.0f} B/s = {rate / 1_000_000:.3f} MB/s")
    print(f"raw payload: {rate / (1024 ** 2):.3f} MiB/s")
    print(f"10-minute raw payload: {rate * 600 / 1_000_000_000:.3f} GB")
    print(f"projected u: {project_u(600, 0.2, POINT_Z_M, 320):.3f} px")
    print(f"stereo depth: {stereo_depth_m(600, 0.06, DISPARITY_PX):.3f} m")
    print("Try FPS=60, POINT_Z_M=4, DISPARITY_PX=15, one change at a time.")


if __name__ == "__main__":
    main()
