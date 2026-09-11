# 多相机智能视觉系统工程（MCVS）

本仓库用于沉淀 **多相机高质量同步采集、Camera/IMU 同步、标定、VIO/SLAM、嵌入式计算与产品化工程** 相关资料。它不是单纯的相机采购调研，也不是单纯的 SLAM 算法仓库，而是一个偏 **智能硬件系统工程** 的综合方向。

---

## 1. 方向定位与简称

当前项目更适合定义为：

> **多相机智能视觉系统工程**  
> **Multi-Camera Vision System Engineering**

推荐简称：

> **MCVS — Multi-Camera Vision System**

也可以按子方向细分：

| 简称 | 全称 | 适用范围 |
|---|---|---|
| **MCS** | Multi-Camera System | 偏多相机硬件、同步、采集、传输、存储 |
| **MCVS** | Multi-Camera Vision System | 多相机 + 标定 + 视觉处理 + 3D / SLAM，最适合当前整体方向 |
| **MC-VIO** | Multi-Camera Visual-Inertial Odometry | 多相机 + IMU 实时位姿估计 |
| **MC-VSLAM** | Multi-Camera Visual / Visual-Inertial SLAM | 多相机 + IMU + 建图与回环 |
| **VIS** | Visual-Inertial System | 如果未来更偏 XR / 机器人定位，可作为上层系统简称 |

当前建议统一使用：

```text
MCVS = Multi-Camera Vision System = 多相机智能视觉系统
```

---

## 2. GitHub 仓库归属建议

根据当前已有仓库：

```text
FTP-LI/RL-Project
FTP-LI/Deep_Learning-Project
FTP-LI/MCU-Project
FTP-LI/Activity-Project
```

建议 **单独新建一个仓库**，不要放进现有四个仓库中。

推荐仓库名：

```text
FTP-LI/Multi-Camera-Vision-Project
```

备选名称：

```text
FTP-LI/MCVS-Project
FTP-LI/Multi-Camera-System-Project
FTP-LI/Visual-Inertial-System-Project
FTP-LI/XR-Vision-System-Project
```

最推荐：

```text
Multi-Camera-Vision-Project
```

原因如下：

| 放入位置 | 是否推荐 | 原因 |
|---|---:|---|
| `RL-Project` | 不推荐 | 当前方向不是强化学习，RL 不是主线 |
| `Deep_Learning-Project` | 不推荐 | 项目可能用深度学习，但核心不是纯 DL，而是系统级多相机视觉硬件 |
| `MCU-Project` | 不推荐 | MCU 只是同步、触发、控制的一部分，不代表完整项目 |
| `Activity-Project` | 不推荐 | 方向过泛，不利于沉淀技术栈 |
| **单开 `Multi-Camera-Vision-Project`** | **推荐** | 最能覆盖 Camera、Sync、IMU、Calibration、VIO/SLAM、硬件工程和产品化 |

核心判断：

```text
MCU / FPGA / DL / SLAM 都只是 MCVS 的模块。
MCVS 本身是系统级工程方向，应该单独建仓库。
```

---

## 3. 当前文件说明

### `README.md`

当前文件，是整个多相机智能视觉系统方向的总入口。用于说明项目定位、简称、仓库归属、技术链路、资料索引、后续目录结构和下一步计划。

### `multicamera_hardware_research_report.docx`

多相机高画质同步采集硬件方案调研报告。该报告是当前项目的主要技术资料，内容包括：

- 多相机同步采集硬件路线；
- 全局快门工业相机方案；
- Hardware Trigger、PTP、CoaXPress、GMSL/FPD-Link、Genlock 的对比；
- 高像素、高画质、多路数据采集的带宽与存储测算；
- 论文和数据集中的典型多相机系统案例；
- 代表性相机、采集卡、嵌入式方案和影视相机路线；
- 多相机系统从实验室 Demo 走向 EVT/DVT/PVT 的工程注意事项。

报告核心结论：

```text
高质量动态多相机采集优先选择：

Global Shutter Cameras
        +
Hardware Trigger / Common Clock
        +
High-bandwidth Links
        +
Distributed Capture Nodes
        +
NVMe Storage
        +
Calibration / Logging / Validation
```

### `fdd97994-63fa-495f-846f-ed9e7fb4a9c9.png`

GitHub 仓库列表截图。该图片用于辅助判断当前多相机方向应该单开仓库，而不是放入 `RL-Project`、`Deep_Learning-Project`、`MCU-Project` 或 `Activity-Project`。

---

## 4. 项目要解决的问题

当前项目围绕以下问题展开：

```text
多路相机如何同时采集？
多相机曝光时间如何同步？
高像素、高画质数据如何稳定传输和存储？
Camera 与 IMU 如何对齐时间？
多相机系统如何完成内参、外参和 Camera-IMU 标定？
采集到的数据如何用于 VIO / SLAM / 3D Reconstruction / AI？
如何从实验室 Demo 走向可验证、可生产、可维护的智能硬件？
```

它的完整链路可以概括为：

```text
Camera
  ↓
Synchronization
  ↓
IMU / Sensor Fusion
  ↓
Calibration
  ↓
VIO / SLAM / 3D Reconstruction
  ↓
Compute / Storage
  ↓
Mechanical / Thermal / Power
  ↓
EVT → DVT → PVT → MP
```

---

## 5. 系统技术架构

一个典型的 MCVS 系统可以抽象为：

```text
                     ┌── RGB / Capture Camera × N
                     │
现实世界 ────────────┼── Tracking Camera × N
                     │
                     └── IMU
                          │
                          ▼
                Synchronization Layer
          Trigger / FSYNC / PTP / Timestamp
                          │
                          ▼
                   Sensor Drivers
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       Imaging Pipeline          Time Alignment
       RAW / ISP / AE                  │
             │                         ▼
             │                  Sensor Calibration
             │               Intrinsic / Extrinsic
             │                  Camera ↔ IMU
             │                         │
             │                         ▼
             │                     VIO / SLAM
             │                         │
             ▼                         ▼
      High-quality Frames        6DoF Pose / Map
             │                         │
             └────────────┬────────────┘
                          ▼
                  3D / AI Application
```

系统可以分为四层：

| 层级 | 内容 |
|---|---|
| **Sensor Layer** | Camera、IMU、镜头、照明、滤光片、快门、曝光 |
| **Hardware/System Layer** | Trigger、Clock、PTP、SerDes、GigE、CXP、SoC、FPGA、MCU、Power、Thermal、Storage |
| **Geometry/Algorithm Layer** | Intrinsic、Extrinsic、Camera-IMU Calibration、VIO、SLAM、Bundle Adjustment、Loop Closure |
| **Productization Layer** | 机械公差、工厂标定、日志、诊断、供应链、EVT、DVT、PVT、MP |

---

## 6. 硬件技术路线

### 6.1 工业相机 + Hardware Trigger

这是当前最推荐的原型路线，尤其适合动态三维重建、人体采集、机器人视觉、多视角数据集采集。

```text
Trigger Generator / MCU / FPGA
              │
              ├── Camera 0
              ├── Camera 1
              ├── Camera 2
              └── Camera N
```

优点：

- 曝光同步链路清晰；
- 易于用示波器、光学测试进行验证；
- 支持全局快门相机实现真正意义上的同时曝光；
- 适合作为 2/4/8 路原型起点。

注意点：

- 必须确认触发电平、输入延迟、曝光启动延迟；
- 不建议把多个相机输入简单并联到一个 GPIO，应使用有源触发分配；
- 同型号、同固件、同曝光模式更容易控制系统误差。

### 6.2 PTP / IEEE 1588 + Scheduled Action

适合多相机数量较多、布线距离较远、希望通过网络统一管理的场景。

核心逻辑：

```text
PTP 同步相机时钟
        ↓
提前下发目标采集时刻
        ↓
各相机按统一时间基准执行曝光
```

关键认识：

```text
PTP 时钟同步 ≠ 自动曝光同步
```

必须确认相机是否支持 Scheduled Action、Synchronous Free Run 或等效机制，并实测真实曝光误差。

### 6.3 CoaXPress + Frame Grabber

适合高像素、高帧率、低延迟和高确定性的工业/科研场景。

优点：

- 带宽高；
- 采集确定性强；
- 适合高端高速相机；
- 可通过采集卡实现更稳定的数据接入。

限制：

- 采集卡、线缆和主机成本高；
- 单台高规格相机可能占用多条 CXP 链路；
- PCIe、内存、NVMe 写入能力也要一起计算。

### 6.4 GMSL / FPD-Link + Embedded SoC

适合 XR、机器人、无人机、车载、多摄像头紧凑硬件。

典型链路：

```text
Camera Module
    ↓
Serializer
    ↓
GMSL / FPD-Link Cable
    ↓
Deserializer
    ↓
MIPI CSI-2
    ↓
SoC / ISP / VIO / SLAM
```

注意点：

- 必须确认 FSYNC 是否真正接入传感器；
- 多路 CSI 带宽、ISP 能力和驱动能力要一起核实；
- 模组标称 RAW 并不等于应用层可稳定获得全路 RAW。

### 6.5 Genlock + Timecode + Cinema Camera

适合影视级高画质、虚拟制作、体积视频、Volumetric Capture 等场景。

特点：

- 画质、镜头、影视工作流强；
- Genlock 用于锁定视频时序；
- Timecode 用于素材时间对齐；
- 成本与数据管理复杂度较高。

注意：

```text
Timecode 不等于曝光同步。
Genlock 也要区分锁定的是视频输出还是传感器采集时序。
```

---

## 7. Multi-Camera SLAM 在系统中的位置

Multi-Camera SLAM 不是让每台相机各自跑一套 SLAM，而是把刚性连接的多台相机视作一个统一的 **Camera Rig**。

```text
                Camera 0
                    ↑
                    │
Camera 3 ←────── [Rig] ──────→ Camera 1
                    │
                    ↓
                Camera 2
```

每台相机相对于 Rig 的外参固定：

```text
T_rig_cam0
T_rig_cam1
T_rig_cam2
T_rig_cam3
```

运行时估计整个 Rig 相对于世界的位姿：

```text
T_world_rig(t)
```

典型算法链路：

```text
Synchronized Images
        ↓
Camera Calibration
        ↓
Feature Detection / Description
        ↓
Feature Matching / Tracking
        ↓
Multi-Camera Pose Estimation
        ↓
Mapping
        ↓
Bundle Adjustment
        ↓
Loop Closure
        ↓
6DoF Pose + Map
```

多相机的价值：

- 更大的总 FOV；
- 更多特征点；
- 更强的方向冗余；
- 单个相机被遮挡或低纹理时，其他相机仍可提供约束；
- 对 XR、机器人、空间定位、3D Mapping 很有价值。

---

## 8. Camera + IMU + VIO/SLAM

如果加入 IMU，系统会从纯视觉 SLAM 进入 Visual-Inertial 系统。

```text
Camera × N ─────┐
                 ├── Time Alignment ─── Calibration ─── VIO / SLAM ─── Pose / Map
IMU ─────────────┘
```

IMU 的价值：

- 高频角速度和加速度；
- 快速运动时补充视觉；
- 视觉模糊或低纹理时提升短时稳定性；
- 为 XR、机器人、无人机等实时定位提供低延迟预测。

最关键的问题：

```text
Camera-Camera Sync
Camera-IMU Sync
Camera Intrinsic
Camera-Camera Extrinsic
Camera-IMU Extrinsic
Camera-IMU Time Offset
```

快速运动下，几毫秒时间偏差都可能使视觉观测和 IMU 预测对不上。因此同步和标定不是附属功能，而是系统核心能力。

---

## 9. 系统负责人画像对应的真实职责

该方向需要的负责人不是纯算法负责人，也不是纯硬件负责人，而是：

> **Hands-on System Lead / System Architect / 多相机智能硬件系统负责人**

他需要负责把如下模块打通：

```text
Camera
  ↓
Synchronization
  ↓
IMU / Sensor Fusion
  ↓
Calibration
  ↓
VIO / SLAM
  ↓
Compute / Bandwidth
  ↓
Power / Thermal
  ↓
Mechanical Tolerance
  ↓
Factory Calibration
  ↓
EVT → DVT → PVT → MP
```

典型职责：

| 职责 | 实际内容 |
|---|---|
| 系统架构 | Camera、IMU、SoC、FPGA、MCU、Storage、Power 的总体方案 |
| 同步体系 | Camera-Camera、Camera-IMU 的 Trigger、Clock、Timestamp 设计 |
| 性能预算 | 带宽、延迟、算力、功耗、热、内存、存储 |
| 标定体系 | Intrinsic、Extrinsic、Camera-IMU、工厂标定流程 |
| 工程化 | EVT、DVT、PVT、MP、日志、诊断、供应商调试 |
| 跨团队决策 | 在算法、硬件、嵌入式、光学、结构、供应链之间做 trade-off |

这也是为什么候选人画像中会强调：

```text
7 年以上软硬件系统经历
完整交付过多相机智能硬件
经历 EVT / DVT / PVT
理解 Camera / IMU / Sync / SLAM / 机械公差 / 功耗 / 热 / 标定 / 供应链
仍然愿意亲自写接口文档、查日志、跟供应商调板子
```

---

## 10. 推荐仓库目录结构

建议单独新建仓库后采用如下结构：

```text
Multi-Camera-Vision-Project/
│
├── README.md
│
├── docs/
│   ├── research/              # 调研报告、论文笔记、方案对比
│   ├── architecture/          # 系统架构、数据流、时钟树、接口定义
│   ├── hardware/              # 相机、IMU、触发器、采集卡、SoC、线缆
│   ├── calibration/           # 标定理论、流程、数据格式
│   ├── productization/        # EVT/DVT/PVT、供应链、测试计划
│   └── videos/                # 视频学习笔记
│
├── camera/
│   ├── drivers/
│   ├── capture/
│   └── configs/
│
├── synchronization/
│   ├── hardware-trigger/
│   ├── ptp/
│   ├── timestamp/
│   └── validation/
│
├── imu/
│   ├── drivers/
│   └── calibration/
│
├── calibration/
│   ├── intrinsic/
│   ├── extrinsic/
│   ├── camera-imu/
│   └── factory-calibration/
│
├── vio/
│   ├── notes/
│   └── experiments/
│
├── slam/
│   ├── notes/
│   └── experiments/
│
├── reconstruction/
│   ├── nerf/
│   ├── 3dgs/
│   └── multiview-stereo/
│
├── embedded/
│   ├── mcu/
│   ├── fpga/
│   ├── soc/
│   └── serdes/
│
├── tools/
│   ├── bandwidth_calculator/
│   ├── timestamp_checker/
│   ├── calibration_checker/
│   └── log_parser/
│
├── datasets/
│   ├── README.md
│   └── samples/
│
└── experiments/
    ├── 2cam_imu_prototype/
    ├── 4cam_sync_test/
    └── 8cam_capture_test/
```

---

## 11. 建议优先沉淀的文档

### `docs/architecture/system_overview.md`

说明整套系统由哪些模块组成、数据怎么流、时间同步怎么走。

### `docs/architecture/clock_and_sync.md`

专门记录 Trigger、PTP、FSYNC、Timestamp、Camera-IMU 时间偏移。

### `docs/hardware/camera_selection.md`

记录相机型号、Sensor、Global/Rolling Shutter、分辨率、帧率、接口、RAW 格式、同步能力。

### `docs/hardware/bandwidth_storage_budget.md`

记录不同相机数量、分辨率、帧率、位深下的数据量和存储需求。

### `docs/calibration/calibration_pipeline.md`

记录内参、外参、Camera-IMU 标定、工厂标定、标定文件格式。

### `docs/productization/evt_dvt_pvt_checklist.md`

记录从实验室原型到工程样机、设计验证、生产验证的检查清单。

### `docs/videos/multicamera_slam_video_notes.md`

记录 Multi-Camera SLAM 视频学习笔记，包括技术链路、实现方式、与 MCVS 的关系。

---

## 12. 关键词索引

### Camera / Imaging

```text
Global Shutter
Rolling Shutter
Sony Pregius / Pregius S
Bayer RAW
SNR
Dynamic Range
MTF
Exposure
ISP
HDR
```

### Synchronization

```text
Hardware Trigger
FSYNC
IEEE 1588 PTP
Scheduled Action Command
Synchronous Free Run
Genlock
LTC / Timecode
Hardware Timestamp
Clock Domain
Time Offset
```

### Data Link / Hardware

```text
USB3 Vision
GigE Vision
5GigE
10GigE
CoaXPress
GMSL2
FPD-Link
MIPI CSI-2
PCIe
FPGA
MCU
SoC
NVMe RAID
```

### Geometry / Algorithm

```text
Camera Intrinsic
Camera Extrinsic
Camera-IMU Calibration
VIO
SLAM
Multi-Camera SLAM
Bundle Adjustment
Loop Closure
6DoF Pose
Feature Tracking
Visual-Inertial Odometry
```

### Product Engineering

```text
System Engineering
EVT
DVT
PVT
MP
NPI
Mechanical Tolerance
Thermal
Power Budget
Factory Calibration
Supply Chain
Reliability Test
Log Diagnosis
```

---

## 13. 下一阶段建议

当前阶段已经完成了方向梳理和硬件路线初步调研。下一阶段建议不要直接采购完整阵列，而是先做最小可验证系统。

推荐原型路径：

```text
Phase 1: 2-Camera + IMU Prototype
    ↓
验证相机同步、IMU 时间戳、基础标定、RAW 采集、日志

Phase 2: 4-Camera Sync Prototype
    ↓
验证外参稳定性、带宽、存储、热、同步误差

Phase 3: 8-Camera Capture Prototype
    ↓
验证分布式采集、NVMe 写入、帧号一致性、长时间稳定性

Phase 4: VIO / SLAM Integration
    ↓
验证 Camera + IMU 标定、实时位姿、回环、地图质量

Phase 5: EVT Thinking
    ↓
开始引入结构、公差、功耗、热、供应链、工厂标定和测试规范
```

最小原型应优先验证：

- 真实曝光是否同步；
- Camera-IMU 时间偏移是否可测、可补偿；
- 内外参是否稳定；
- RAW 数据是否完整无丢帧；
- 带宽与存储是否满足目标；
- 热稳定性是否影响成像和标定；
- 日志能否定位掉帧、错帧、时钟漂移和驱动异常。

---

## 14. 一句话总结

```text
方向：多相机智能视觉系统工程
简称：MCVS = Multi-Camera Vision System
仓库：建议单开 Multi-Camera-Vision-Project
硬件核心：Camera + IMU + Sync + Compute + Storage
算法核心：Calibration + MC-VIO + MC-VSLAM
工程核心：把实验室多相机 Demo 做成可验证、可标定、可诊断、可量产的智能硬件系统
```
