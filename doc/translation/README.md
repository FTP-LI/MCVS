# 论文中文全文 PDF

更新日期：2026-09-14。

目标是给每篇已下载的英文论文配备完整简体中文 PDF，保留公式、图表、章节编号和参考文献，以便对照阅读。摘要、导读或技术路线笔记不计入全文翻译完成数量。

## 当前进度

- 英文原文：15 篇，共 184 页，均可通过 PDF 解析器打开并提取文本。
- 完整中文 PDF：0 篇。
- 当前可用的工具中没有已连接的专业翻译服务；本机未配置 `DEEPL_AUTH_KEY` 或 `DEEPL_API_KEY`。
- 已查看 VersaVIS 作者仓库、OpenVINS 官方文档及 ORB-SLAM3 作者仓库，并检索中文译本线索；本次未找到可核验的作者或出版社中文全文译本。这是本次检索结果，不代表所有论文都不存在官方译本。
- 已准备 DeepL 官方 Python SDK 的批量处理入口；尚未向 DeepL 上传论文，也未发生翻译请求。

## 来源与命名

| 类型 | 标注方式 | 所需依据 |
|---|---|---|
| 作者或出版社官方译本 | 官方中文译本 | 发布方页面、译者或审定说明，以及可核验的原文版本 |
| DeepL 等专业服务译文 | 服务名称、机器翻译、校对状态 | 实际服务返回的 PDF、生成时间和原文校验值 |
| 人工或 AI 辅助翻译 | 译者或生成方式、校对状态 | 逐篇记录翻译范围与复核结果 |

专业翻译服务不等同于作者认可或专家审定。当前脚本使用 DeepL 官方接口；术语表采用本项目统一用词，不宣称为国家标准或官方审定译名。

英文原文保持在 `doc/pdf/`。服务生成的文件命名为 `doc/pdf/zh/<英文原文件名去掉.pdf>.zh-CN.deepl.pdf`；同名 `.translation.json` 记录来源、日期、原文 SHA-256、页数和待校对状态。下表只链接已经存在的原文；中文文件真实生成后再补充下载链接。

## 逐篇配对清单

| 原文 | 页数 | 中文工作标题 | 完整中文版 |
|---|---:|---|---|
| [MultiCol-SLAM](../pdf/2016_MultiCol_SLAM_Modular_Real_Time_Multi_Camera_SLAM.pdf) | 15 | MultiCol-SLAM：模块化实时多相机 SLAM 系统 | 待翻译 |
| [VINS-Mono](../pdf/2017_VINS_Mono_Robust_Versatile_Monocular_VINS.pdf) | 17 | VINS-Mono：鲁棒且通用的单目视觉惯性状态估计器 | 待翻译 |
| [TUM VI](../pdf/2018_TUM_VI_Benchmark.pdf) | 9 | 用于评估视觉惯性里程计的 TUM VI 基准 | 待翻译 |
| [MIMC-VINS](../pdf/2020_MIMC_VINS_Multi_IMU_Multi_Camera_VINS.pdf) | 20 | MIMC-VINS：通用且具备容错能力的多 IMU 多相机视觉惯性导航系统 | 待翻译 |
| [OpenVINS](../pdf/2020_OpenVINS_Research_Platform_for_Visual_Inertial_Estimation.pdf) | 7 | OpenVINS：视觉惯性估计研究平台 | 待翻译 |
| [VersaVIS](../pdf/2020_VersaVIS_Open_Versatile_Multi_Camera_Visual_Inertial_Sensor_Suite.pdf) | 18 | VersaVIS：开放通用的多相机视觉惯性传感器套件 | 待翻译 |
| [ORB-SLAM3](../pdf/2021_ORB_SLAM3_Visual_Visual_Inertial_Multimap_SLAM.pdf) | 18 | ORB-SLAM3：用于视觉、视觉惯性与多地图 SLAM 的高精度开源库 | 待翻译 |
| [Instant-NGP](../pdf/2022_Instant_NGP_Multiresolution_Hash_Encoding.pdf) | 15 | 采用多分辨率哈希编码的即时神经图形基元 | 待翻译 |
| [Neural 3D Video](../pdf/2022_Neural_3D_Video_Synthesis_from_Multi_View_Video.pdf) | 11 | 从多视角视频合成神经三维视频 | 待翻译 |
| [3D Gaussian Splatting](../pdf/2023_3D_Gaussian_Splatting_for_Real_Time_Radiance_Field_Rendering.pdf) | 14 | 用于实时辐射场渲染的三维高斯泼溅 | 待翻译 |
| [MAVIS](../pdf/2023_MAVIS_Multi_Camera_Augmented_Visual_Inertial_SLAM.pdf) | 7 | MAVIS：使用基于 SE₂(3) 的精确 IMU 预积分的多相机增强视觉惯性 SLAM | 待翻译 |
| [Autonomous Valet Parking](../pdf/2023_Multi_Camera_VISLAM_Autonomous_Valet_Parking.pdf) | 8 | 面向自主代客泊车的多相机视觉惯性同步定位与建图 | 待翻译 |
| [Hilti SLAM Challenge 2023](../pdf/2024_Hilti_SLAM_Challenge_2023.pdf) | 8 | Hilti SLAM 挑战赛 2023：施工场景跨传感器配置的单次与多次采集 SLAM 评测 | 待翻译 |
| [Calousel](../pdf/2026_Calousel_Non_Overlapping_Multi_Camera_Calibration.pdf) | 8 | Calousel：基于纯旋转的非重叠视场多相机系统外参标定 | 待翻译 |
| [Hilti-Trimble-Oxford](../pdf/2026_Hilti_Trimble_Oxford_360_VI_Benchmark.pdf) | 9 | Hilti-Trimble-Oxford 数据集：带平面图先验、用于 SLAM 与定位的 360 度视觉惯性基准 | 待翻译 |

机器可读的原文清单见 [inventory.json](inventory.json)，包含文件名、页数、大小和 SHA-256。文件名中的年份沿用已下载文件，不代替正式出版年份。

## 批量处理入口

脚本：[translate_pdfs.py](translate_pdfs.py)。默认仅检查本地文件并显示配对，不联网；`--run` 才会将选中的完整 PDF 上传到 DeepL 并消耗账号额度。

```powershell
python -m pip install -r doc/translation/requirements.txt
python doc/translation/translate_pdfs.py --inventory
python doc/translation/translate_pdfs.py --match VersaVIS
```

实际运行需要 DeepL API 账号，在本机环境中设置 `DEEPL_AUTH_KEY` 或 `DEEPL_API_KEY`，不要写入仓库。DeepL 网页账号与 API 产品的权限和额度需分别核实。

```powershell
python doc/translation/translate_pdfs.py --run --match VersaVIS
python doc/translation/translate_pdfs.py --run
```

先完成 VersaVIS 样本并检查版式和术语，再处理其余论文。文件大小、文档额度和计费规则依账号及服务当前限制而定；以 [DeepL 官方用量说明](https://developers.deepl.com/docs/resources/usage-limits) 为准。

[terminology.tsv](terminology.tsv) 是 UTF-8、无表头、两列的英中术语表。导入服务并获得匹配英中语言对的术语表 ID 后，可传入 `--glossary-id <ID>`；不传该参数时脚本不会自动应用本地术语表。保留 SLAM、VIO、IMU、SE(3)、SE₂(3) 等缩写或数学记号，并在校对时核对原文语境。

脚本逐篇记录上传任务，失败后保留 `.state/` 中的续传信息。再次运行可恢复已有任务；上传结果不明、下载中断或服务任务已过期时会停止，避免自动重复提交。`.state/` 含文档下载凭据，已通过本目录 `.gitignore` 排除；不要提交或分享。若进程被强制终止且留下 `run.lock`，先确认没有翻译进程仍在运行，再移除该锁。

## 译后复核

脚本仅检查 PDF 可打开、含中文文本及输出页数，输出状态仍是 `pending_review`。以下工作完成后才能把表格中的状态改为“已校对”：

1. 对照原文逐节核对摘要、正文、结论、附录与参考文献是否完整。
2. 核对公式、上下标、坐标变换方向、正负号、单位及实验数字。
3. 核对双栏阅读顺序、表格跨页、图注、图内英文和中文字体；逐页渲染检查遮挡与乱码。中文排版可能改变页数，页数一致不能证明翻译完整。
4. 统一视觉惯性、内外参、预积分、可观性、回环、辐射场等术语；含混处保留英文。
5. 记录复核人员、日期和修订范围；在 README 与论文索引中补上真实中文 PDF 链接。

## 已核对的来源

- [DeepL PDF 文档翻译](https://support.deepl.com/hc/en-us/articles/4411308018450-Translate-PDF-files)：账号要求与 PDF 版式限制。
- [DeepL 文档翻译接口](https://developers.deepl.com/api-reference/document/upload-and-translate-a-document)：完整文档上传、源语言、目标语言、输出格式及术语表参数。
- [DeepL 官方 Python SDK](https://github.com/DeepL/deepl-python)：上传、状态查询与下载接口。
- [VersaVIS 作者仓库](https://github.com/ethz-asl/versavis)、[OpenVINS 官方文档](https://docs.openvins.com/)、[ORB-SLAM3 作者仓库](https://github.com/UZ-SLAMLab/ORB_SLAM3)：原作与项目入口。

VersaVIS 本地 PDF 第 18 页明确列出 CC BY 4.0；其余论文的许可需按具体版本核对。论文、代码及数据集的许可分别记录，不互相替代。
