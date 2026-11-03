# MCVS: 多相机智能视觉系统工程

MCVS 是 **Multi-Camera Vision System** 的缩写。本仓库用于沉淀多相机智能硬件系统从论文研究、技术路线、原型验证到工程化落地的资料。

**零基础从这里开始：[学习体系入口](doc/learning/README.md)。** 按每周 4–6 小时规划 36 周，提供中文基础手册、每周任务、实验验收、路线图、打印版和进度表。新增硬件总预算不超过 1000 元，核心采购上限 520 元，分阶段购买。今天先做 [第一周行动单](doc/learning/first_week.md)，不需要先买设备或读完论文。

学习方案编制与个人学习进度分开管理：[进度表](doc/learning/progress.md)从零开始，按实际证据逐项验收。原有工程方案调研和论文资料继续保留。

申请与科研安排（2026-11-02）：计划申请 2027 年中外合作办学硕士，院校与专业待定。新增 [申请前科研计划](doc/research/application_research_plan.md)，把可复现实验、论文准备与申请材料并行安排，保留 ICRA/IROS 等高水平投稿目标；各阶段完成状态按真实成果记录。

当前研究重点不是单纯购买相机，也不是单纯复现某个 SLAM 算法，而是把下面这条系统链路打通：

```text
Camera Rig
  -> Synchronization
  -> IMU / Timestamp
  -> Calibration
  -> MC-VIO / MC-SLAM
  -> 3D Reconstruction / AI
  -> Embedded Compute / Storage
  -> EVT / DVT / PVT
```

## 1. 项目目标

本项目要回答的问题：

- 多路相机如何实现同一时刻曝光，而不只是同一时刻收到图像；
- Camera-Camera、Camera-IMU 的时间基准如何统一、验证和补偿；
- 多相机系统如何完成内参、外参、Camera-IMU 标定；
- 多相机数据如何进入 VIO、SLAM、3D Reconstruction 或 AI 管线；
- 高分辨率、多路 RAW / RGB 数据如何稳定传输、记录和诊断；
- 一个实验室 Demo 如何走向可验证、可维护、可生产的智能硬件系统。

## 2. 当前文档

| 文件 | 内容 |
|---|---|
| [doc/research/application_research_plan.md](doc/research/application_research_plan.md) | 暂定 2027 年硕士申请前科研安排、论文成熟度与申请材料准备 |
| [doc/learning/README.md](doc/learning/README.md) | 零基础学习入口、36 周路径与六个关卡 |
| [doc/learning/MCVS_learning_guide.pdf](doc/learning/MCVS_learning_guide.pdf) | 可打印中文学习手册与进度页 |
| [doc/learning/hardware.md](doc/learning/hardware.md) | 1000 元预算分配、具体型号、官方来源与采购门槛 |
| [doc/papers.md](doc/papers.md) | 已筛选论文、数据集、工具和工程参考 |
| [doc/technical_route.md](doc/technical_route.md) | 推荐技术路线、阶段目标、验证指标和风险 |
| [doc/hardware_scheme_research.md](doc/hardware_scheme_research.md) | 旧版 README 中保留下来的硬件、同步、采集与系统方案调研 |
| [doc/pdf/](doc/pdf/) | 已下载的开放论文 PDF |
| [doc/translation/README.md](doc/translation/README.md) | 完整中文 PDF 的配对清单、翻译来源、术语与处理进度 |

中文 PDF 进度（2026-09-14）：已检查 15 篇英文论文，共 184 页；尚未生成中文全文 PDF。已准备 DeepL 官方 API 批量翻译入口，等待可用的翻译服务凭据。专业服务生成的译文标注为机器翻译，作者或出版社发布并可核验的版本才标注为官方译本。

## 3. 技术路线总览

推荐采用 **先同步与标定，后算法集成，再工程化扩展** 的路线。

```text
Phase 0: 论文与工具链调研
  -> 明确同步、标定、VIO/SLAM、重建的候选路线

Phase 1: 2-Camera + IMU 最小原型
  -> 验证硬件触发、中心曝光时间戳、Camera-IMU 时间偏移

Phase 2: 4-Camera Rig
  -> 验证多相机外参稳定性、带宽、丢帧、热漂移

Phase 3: MC-VIO / MC-SLAM
  -> 接入 OpenVINS / VINS-Fusion / ORB-SLAM3 / MAVIS 等路线做对比

Phase 4: 3D Reconstruction / 3DGS
  -> 使用同步多视角数据验证重建质量和动态场景处理能力

Phase 5: 工程化样机
  -> 引入结构、公差、功耗、散热、工厂标定、日志和诊断
```

更细的阶段拆解见 [doc/technical_route.md](doc/technical_route.md)。

## 4. 系统架构

一个典型 MCVS 系统可以抽象为四层：

| 层级 | 关键内容 |
|---|---|
| Sensor Layer | Camera、镜头、Global/Rolling Shutter、IMU、曝光、照明 |
| Sync & Capture Layer | Hardware Trigger、FSYNC、PTP、Timestamp、SerDes、GigE、USB3、CXP、NVMe |
| Geometry & Estimation Layer | Intrinsic、Extrinsic、Camera-IMU Calibration、VIO、SLAM、Bundle Adjustment |
| Product Layer | 机械公差、热稳定、功耗、日志、诊断、工厂标定、EVT/DVT/PVT |

核心原则：

```text
同步精度决定数据是否可用。
标定质量决定几何是否可信。
带宽与存储决定系统是否稳定。
日志和验证决定问题是否可定位。
```

## 5. 推荐原型方向

以下是具备基础后的工程原型方向，需要独立预算。当前零基础阶段先按 [学习硬件方案](doc/learning/hardware.md)使用普通 USB 摄像头、板载 IMU 与公开数据完成练习。

进入工程阶段后建议先做：

```text
2 个全局快门相机
+ 1 个 IMU
+ 统一硬件触发 / FSYNC
+ 中心曝光时间戳
+ Kalibr / OpenVINS 标定与评估
+ ROS bag / MCAP 数据记录
```

时间戳需明确所指事件和时钟域。全局曝光可约定中心曝光时刻；卷帘快门还要建模逐行时间，不能用一个中心时刻代表所有像素行。学习用 USB 相机与独立 IMU 并不自动具备这里要求的硬件同步。

理由：

- 2-Camera + IMU 已经能覆盖 Camera-Camera Sync、Camera-IMU Sync、内外参、时间偏移和基础 VIO；
- 系统规模足够小，便于用示波器、LED timing board、日志和离线标定快速定位问题；
- 验证通过后可以自然扩展到 4 路、8 路或分布式采集节点。

## 6. 关键研究方向

| 方向 | 需要重点研究的问题 |
|---|---|
| 多相机同步 | Hardware Trigger、PTP Scheduled Action、FSYNC、中心曝光时间戳 |
| 多传感器标定 | Multi-camera intrinsic/extrinsic、Camera-IMU spatial/temporal calibration |
| MC-VIO | 多相机观测如何进入 MSCKF 或滑窗优化，异步相机如何处理 |
| MC-SLAM | 多相机 Rig 位姿、MultiKeyframe、Bundle Adjustment、Loop Closure |
| 数据集与评测 | EuRoC、TUM-VI、Hilti、Hilti-Trimble-Oxford 等真实传感器数据 |
| 多视角重建 | Multi-view Video、NeRF、3D Gaussian Splatting、动态重建 |
| 工程化 | 带宽、存储、热漂移、触发分配、工厂标定、日志诊断 |

## 7. 关键词

```text
Multi-Camera Vision System
Multi-Camera Rig
Global Shutter
Hardware Trigger
FSYNC
IEEE 1588 PTP
Scheduled Action Command
Center-of-Exposure Timestamp
Camera-IMU Calibration
Kalibr
MC-Calib
OpenVINS
VINS-Fusion
ORB-SLAM3
MAVIS
MultiCol-SLAM
Bundle Adjustment
Visual-Inertial Odometry
Visual-Inertial SLAM
3D Gaussian Splatting
Volumetric Capture
EVT DVT PVT
```

## 8. 下一步

1. 按 [第一周行动单](doc/learning/first_week.md)完成单位计算和首个 Python 练习。
2. 按 [36 周课程](doc/learning/curriculum.md)依次补齐编程、几何、标定、IMU 与时钟基础，用 [实验任务书](doc/learning/labs.md)和 [进度表](doc/learning/progress.md)验收。
3. 达到相应阶段后，再按 [硬件采购门槛](doc/learning/hardware.md)添置设备；基础阶段沿用现有电脑。
4. 第 25–30 周核对研究环境，运行已有 VIO 示例并评测，再读 VersaVIS 与 OpenVINS。更多论文按 [阅读导航](doc/learning/resources.md)选择。
5. 完成学习关卡后，再进入 [工程技术路线](doc/technical_route.md)的硬件同步、Camera-IMU 时空标定、多相机扩展与算法对比。

## 9. 工程目录与获取

当前工程包含零基础学习体系、技术调研资料、15 篇英文论文 PDF，以及中文全文翻译的配对清单、术语表和处理脚本。中文学习手册为原创教学整理，不是论文的完整译本。

```text
MCVS/
|-- README.md
|-- .gitattributes
|-- .gitignore
`-- doc/
    |-- hardware_scheme_research.md
    |-- papers.md
    |-- technical_route.md
    |-- learning/                    # Curriculum, labs, hardware, progress and examples
    |   |-- README.md
    |   |-- MCVS_learning_guide.pdf
    |   |-- assets/                  # Roadmap and printable calibration target
    |   `-- tools/                   # Reproducible material builder
    |-- pdf/                         # 15 original paper PDFs
    `-- translation/
        |-- README.md
        |-- inventory.json           # Original PDF sizes, page counts and SHA-256
        |-- terminology.tsv
        |-- requirements.txt
        |-- translate_pdfs.py
        `-- .gitignore
```

完整获取工程：

```bash
git clone https://github.com/FTP-LI/MCVS.git
cd MCVS
```

论文 PDF 以完整二进制文件收录，可随仓库直接获取。原文校验信息见 [inventory.json](doc/translation/inventory.json)，翻译工具的依赖与运行方法见 [翻译说明](doc/translation/README.md)。Python 缓存、虚拟环境、环境密钥文件及翻译任务凭据不纳入版本控制。中文全文 PDF 当前仍为待翻译状态。
