# MCVS 技术路线

更新时间：2026-09-11

本路线面向一个可落地的多相机智能视觉系统：先生产可信数据，再接入 VIO / SLAM / 3D 重建，最后进入工程化样机。

## 1. 总体原则

```text
Data correctness first.
Algorithm second.
Productization always in mind.
```

对 MCVS 来说，算法失败经常不是算法本身的问题，而是前面的同步、标定、时间戳、带宽、曝光或日志没有做好。因此技术路线应从数据生产系统开始。

## 2. 推荐路线

```text
2-Camera + IMU
  -> 4-Camera Rig
  -> 8-Camera / Distributed Capture
  -> MC-VIO / MC-SLAM
  -> Multi-view Reconstruction
  -> Engineering Prototype
```

不建议一开始直接做 8 路或 16 路完整阵列。多相机系统的问题不是线性增加，而是同步、带宽、热、日志、标定和机械公差一起放大。

## 3. Phase 0: 论文与工具链调研

目标：

- 明确硬件同步路线：Hardware Trigger / FSYNC / PTP Scheduled Action；
- 明确标定路线：Kalibr、MC-Calib、AprilGrid、多目标或非重叠视场标定；
- 明确算法基线：OpenVINS、VINS-Fusion、ORB-SLAM3、MAVIS、MultiCol-SLAM；
- 明确数据集基线：EuRoC、TUM-VI、Hilti、Hilti-Trimble-Oxford；
- 明确数据格式：image、imu、calibration、timestamps、frame ids、logs。

输出物：

- 论文笔记；
- 候选硬件清单；
- 数据格式草案；
- 同步和标定验证计划。

## 4. Phase 1: 2-Camera + IMU 最小原型

推荐配置：

```text
Global Shutter Camera x 2
IMU x 1
Hardware Trigger / FSYNC x 1
Host PC or Embedded SoC
ROS bag / MCAP logger
Kalibr / OpenVINS toolchain
```

需要验证：

| 项目 | 验证方法 | 合格标准 |
|---|---|---|
| Camera-Camera 曝光同步 | 示波器测触发和曝光信号，LED timing board 拍摄 | 同一帧观测一致，无系统性错帧 |
| Camera-IMU 时间关系 | 记录统一时钟下的 image + imu，运行 Kalibr time offset | time offset 稳定、可重复 |
| 相机内参 | AprilGrid / checkerboard，多距离多角度采集 | 重投影误差稳定 |
| 相机间外参 | Kalibr / MC-Calib | 外参重复标定漂移小 |
| 数据记录 | 长时间采集，统计帧号、时间戳、丢帧 | 无连续丢帧，无异常 timestamp jump |

关键设计：

- timestamp 必须指向中心曝光时刻；
- image frame id、sequence id、trigger id 需要同时保存；
- IMU rate 建议先从 200 Hz 或以上开始；
- 相机曝光要尽量短，避免标定动作中运动模糊；
- 日志要能反查每一帧来自哪个 trigger。

## 5. Phase 2: 4-Camera Rig

目标：

- 从 stereo 扩展到刚性多相机 Rig；
- 验证 `T_rig_cam_i` 的可重复标定；
- 评估带宽、CPU、内存、NVMe 写入和热稳定性；
- 验证不同视场重叠程度对 VIO / SLAM 的影响。

重点风险：

| 风险 | 影响 | 对策 |
|---|---|---|
| 触发线分配不稳定 | 相机间曝光偏移 | 使用有源触发分配或同步板 |
| 外参随温度或结构应力漂移 | SLAM / 重建几何变差 | 做热态标定和重复标定 |
| USB / GigE 带宽抢占 | 丢帧、延迟抖动 | 独立 controller / NIC，记录吞吐与队列 |
| 自动曝光不一致 | 特征质量和重建纹理不稳 | 原型阶段优先固定曝光或同步 AE 策略 |

输出物：

- 4-Camera Rig 标定文件；
- 同步误差报告；
- 带宽与存储预算；
- OpenVINS / VINS-Fusion / ORB-SLAM3 基线结果。

## 6. Phase 3: MC-VIO / MC-SLAM

推荐基线：

| 基线 | 用途 |
|---|---|
| OpenVINS | MSCKF/VIO 研究和工程调试，文档清晰 |
| VINS-Fusion | 优化式 VIO / stereo+IMU 基线 |
| ORB-SLAM3 | VI-SLAM、回环、多地图框架参考 |
| MAVIS | 多相机 VI-SLAM 重点研究对象 |
| MultiCol-SLAM | 多相机 Rig + BA + loop closing 的经典参考 |

核心建模：

```text
T_world_rig(t): 运行时估计的 Rig 位姿
T_rig_cam_i: 每个相机相对 Rig 的固定外参
T_imu_rig: IMU 与 Rig 的固定外参
dt_cam_i_imu: 每个相机相对 IMU 的时间偏移
```

算法集成前置条件：

- 所有图像有可信时间戳；
- 所有相机内参与畸变模型明确；
- `T_rig_cam_i` 可重复；
- IMU 噪声参数经过 Allan variance 或数据手册校准；
- 数据格式能被工具链稳定读取。

## 7. Phase 4: 多视角重建

目标：

- 用同步多视角数据做静态和动态重建；
- 比较 Multi-view Stereo、NeRF、3D Gaussian Splatting 的适用范围；
- 建立从采集到重建结果的质量指标。

评估指标：

| 指标 | 说明 |
|---|---|
| 几何一致性 | 多视角边缘、轮廓和深度是否对齐 |
| 纹理一致性 | 是否出现错位、重影、闪烁 |
| 动态质量 | 快速运动下是否 ghosting |
| 标定敏感性 | 外参扰动对结果影响多大 |
| 训练 / 重建时间 | 是否满足目标应用 |

关键判断：

- 静态场景可以容忍较小时间问题，动态场景几乎不能；
- 3DGS / NeRF 的输入仍然依赖相机位姿和标定质量；
- 如果目标是实时系统，应尽早记录端到端延迟和数据吞吐。

## 8. Phase 5: 工程化样机

工程化不是最后补文档，而是把验证能力固化进系统。

必须具备：

- Trigger / timestamp / frame id 全链路日志；
- 标定文件版本管理；
- 相机和 IMU 健康状态诊断；
- 丢帧、错帧、时钟漂移报警；
- 带宽、CPU、GPU、内存、NVMe、温度监控；
- 工厂标定流程；
- EVT / DVT / PVT 检查清单。

建议目录后续扩展：

```text
doc/
  papers.md
  technical_route.md
  sync_validation.md
  calibration_pipeline.md
  bandwidth_storage_budget.md
  hardware_selection.md
  dataset_format.md
  evt_dvt_pvt_checklist.md
```

## 9. 当前推荐决策

| 决策项 | 推荐 |
|---|---|
| 项目简称 | MCVS = Multi-Camera Vision System |
| 原型起点 | 2-Camera + IMU |
| 相机快门 | 优先 Global Shutter |
| 同步方式 | 原型优先 Hardware Trigger / FSYNC；规模化再评估 PTP |
| 标定工具 | Kalibr + MC-Calib |
| VIO 基线 | OpenVINS + VINS-Fusion |
| SLAM 基线 | ORB-SLAM3 + MAVIS + MultiCol-SLAM |
| 数据集 | EuRoC、TUM-VI、Hilti |
| 重建方向 | 先 3DGS / Instant-NGP 快速验证，再研究动态 Neural 3D Video |

## 10. 近期任务清单

1. 建立 `sync_validation.md`，定义示波器、LED timing board 和日志验证方法。
2. 建立 `calibration_pipeline.md`，定义相机内参、外参、Camera-IMU 标定流程。
3. 建立 `bandwidth_storage_budget.md`，按分辨率、帧率、位深、相机数量计算吞吐。
4. 选择 2-Camera + IMU 原型硬件。
5. 用 EuRoC / TUM-VI 跑通 OpenVINS 或 VINS-Fusion，作为算法环境烟测。
