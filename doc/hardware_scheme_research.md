# MCVS 硬件与系统方案调研

更新时间：2026-09-11

本文件保留旧版 README 中与技术方案有关的调研内容，并将其整理为硬件、同步、采集、标定和系统路线参考。

## 1. 项目要解决的问题

MCVS 围绕以下工程问题展开：

```text
多路相机如何同时采集？
多相机曝光时间如何同步？
高像素、高画质数据如何稳定传输和存储？
Camera 与 IMU 如何对齐时间？
多相机系统如何完成内参、外参和 Camera-IMU 标定？
采集到的数据如何用于 VIO / SLAM / 3D Reconstruction / AI？
如何从实验室 Demo 走向可验证、可生产、可维护的智能硬件？
```

完整链路：

```text
Camera
  -> Synchronization
  -> IMU / Sensor Fusion
  -> Calibration
  -> VIO / SLAM / 3D Reconstruction
  -> Compute / Storage
  -> Mechanical / Thermal / Power
  -> EVT -> DVT -> PVT -> MP
```

## 2. 系统技术架构

一个典型 MCVS 系统可以抽象为：

```text
                     +-- RGB / Capture Camera x N
                     |
Reality ------------+-- Tracking Camera x N
                     |
                     +-- IMU
                          |
                          v
                Synchronization Layer
          Trigger / FSYNC / PTP / Timestamp
                          |
                          v
                   Sensor Drivers
                          |
             +------------+------------+
             v                         v
       Imaging Pipeline          Time Alignment
       RAW / ISP / AE                  |
             |                         v
             |                  Sensor Calibration
             |               Intrinsic / Extrinsic
             |                  Camera <-> IMU
             |                         |
             |                         v
             |                     VIO / SLAM
             |                         |
             v                         v
      High-quality Frames        6DoF Pose / Map
             |                         |
             +------------+------------+
                          v
                  3D / AI Application
```

系统分层：

| 层级 | 内容 |
|---|---|
| Sensor Layer | Camera、IMU、镜头、照明、滤光片、快门、曝光 |
| Hardware/System Layer | Trigger、Clock、PTP、SerDes、GigE、CXP、SoC、FPGA、MCU、Power、Thermal、Storage |
| Geometry/Algorithm Layer | Intrinsic、Extrinsic、Camera-IMU Calibration、VIO、SLAM、Bundle Adjustment、Loop Closure |
| Productization Layer | 机械公差、工厂标定、日志、诊断、供应链、EVT、DVT、PVT、MP |

## 3. 硬件技术路线

### 3.1 工业相机 + Hardware Trigger

这是当前最推荐的原型路线，尤其适合动态三维重建、人体采集、机器人视觉、多视角数据集采集。

```text
Trigger Generator / MCU / FPGA
              |
              +-- Camera 0
              +-- Camera 1
              +-- Camera 2
              +-- Camera N
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

### 3.2 PTP / IEEE 1588 + Scheduled Action

适合多相机数量较多、布线距离较远、希望通过网络统一管理的场景。

核心逻辑：

```text
PTP 同步相机时钟
        |
        v
提前下发目标采集时刻
        |
        v
各相机按统一时间基准执行曝光
```

关键认识：

```text
PTP 时钟同步 != 自动曝光同步
```

必须确认相机是否支持 Scheduled Action、Synchronous Free Run 或等效机制，并实测真实曝光误差。

### 3.3 CoaXPress + Frame Grabber

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

### 3.4 GMSL / FPD-Link + Embedded SoC

适合 XR、机器人、无人机、车载、多摄像头紧凑硬件。

典型链路：

```text
Camera Module
    |
    v
Serializer
    |
    v
GMSL / FPD-Link Cable
    |
    v
Deserializer
    |
    v
MIPI CSI-2
    |
    v
SoC / ISP / VIO / SLAM
```

注意点：

- 必须确认 FSYNC 是否真正接入传感器；
- 多路 CSI 带宽、ISP 能力和驱动能力要一起核实；
- 模组标称 RAW 并不等于应用层可稳定获得全路 RAW。

### 3.5 Genlock + Timecode + Cinema Camera

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

## 4. Multi-Camera SLAM 在系统中的位置

Multi-Camera SLAM 不是让每台相机各自跑一套 SLAM，而是把刚性连接的多台相机视作一个统一的 Camera Rig。

```text
                Camera 0
                    ^
                    |
Camera 3 <------ [Rig] ------> Camera 1
                    |
                    v
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
        -> Camera Calibration
        -> Feature Detection / Description
        -> Feature Matching / Tracking
        -> Multi-Camera Pose Estimation
        -> Mapping
        -> Bundle Adjustment
        -> Loop Closure
        -> 6DoF Pose + Map
```

多相机的价值：

- 更大的总 FOV；
- 更多特征点；
- 更强的方向冗余；
- 单个相机被遮挡或低纹理时，其他相机仍可提供约束；
- 对 XR、机器人、空间定位、3D Mapping 很有价值。

## 5. Camera + IMU + VIO/SLAM

如果加入 IMU，系统会从纯视觉 SLAM 进入 Visual-Inertial 系统。

```text
Camera x N ----+
               +-> Time Alignment -> Calibration -> VIO / SLAM -> Pose / Map
IMU -----------+
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

## 6. 下一阶段建议

当前阶段不要直接采购完整阵列，而是先做最小可验证系统。

推荐原型路径：

```text
Phase 1: 2-Camera + IMU Prototype
    -> 验证相机同步、IMU 时间戳、基础标定、RAW 采集、日志

Phase 2: 4-Camera Sync Prototype
    -> 验证外参稳定性、带宽、存储、热、同步误差

Phase 3: 8-Camera Capture Prototype
    -> 验证分布式采集、NVMe 写入、帧号一致性、长时间稳定性

Phase 4: VIO / SLAM Integration
    -> 验证 Camera + IMU 标定、实时位姿、回环、地图质量

Phase 5: EVT Thinking
    -> 引入结构、公差、功耗、热、供应链、工厂标定和测试规范
```

最小原型应优先验证：

- 真实曝光是否同步；
- Camera-IMU 时间偏移是否可测、可补偿；
- 内外参是否稳定；
- RAW 数据是否完整无丢帧；
- 带宽与存储是否满足目标；
- 热稳定性是否影响成像和标定；
- 日志能否定位掉帧、错帧、时钟漂移和驱动异常。
