# MCVS 论文与资料索引

更新时间：2026-09-14

本文件保存 MCVS 方向的论文、数据集、开源工具和工程参考入口。英文论文 PDF 已保存在本地，同时保留 DOI、arXiv、官方项目页和代码仓库链接以核对来源与版本。

零基础读者先从 [学习体系](learning/README.md)补编程、几何、IMU 与时钟知识。当前学习方案在第 29–30 周优先安排 VersaVIS 和 OpenVINS，具体读法见 [资料导航](learning/resources.md)。下表 P0/P1 是研究优先级，不要求初学者开头就读完全部论文。

## 阅读优先级

| 优先级 | 主题 | 先读材料 |
|---|---|---|
| P0 | 同步与标定 | VersaVIS、Kalibr、MC-Calib、OpenVINS calibration guide |
| P0 | MC-VIO / MC-SLAM | mc-VINS、OpenVINS、VINS-Mono / VINS-Fusion、ORB-SLAM3、MAVIS |
| P1 | 多相机 SLAM 建模 | MultiCol Bundle Adjustment、MultiCol-SLAM、BundledSLAM |
| P1 | 数据集与评测 | EuRoC、TUM-VI、Hilti 2022/2023、Hilti-Trimble-Oxford 2026 |
| P2 | 重建与应用 | Neural 3D Video、Instant-NGP、3D Gaussian Splatting |

## 本地 PDF 收录

已下载的开放 PDF 存放在 [pdf/](pdf/) 目录。未收录的论文通常是因为只有 IEEE / Elsevier / SAGE 付费页，或官网直链返回 403/404。

完整中文版的配对清单与进度见 [translation/README.md](translation/README.md)。截至 2026-09-14，15 篇英文 PDF 已完成可读性检查，中文全文 PDF 尚未生成；翻译服务接通后输出到 `pdf/zh/`，并记录服务来源及校对状态。

| 论文 / 资料 | 本地 PDF |
|---|---|
| VersaVIS: An Open Versatile Multi-Camera Visual-Inertial Sensor Suite | [pdf/2020_VersaVIS_Open_Versatile_Multi_Camera_Visual_Inertial_Sensor_Suite.pdf](pdf/2020_VersaVIS_Open_Versatile_Multi_Camera_Visual_Inertial_Sensor_Suite.pdf) |
| VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator | [pdf/2017_VINS_Mono_Robust_Versatile_Monocular_VINS.pdf](pdf/2017_VINS_Mono_Robust_Versatile_Monocular_VINS.pdf) |
| OpenVINS: A Research Platform for Visual-Inertial Estimation | [pdf/2020_OpenVINS_Research_Platform_for_Visual_Inertial_Estimation.pdf](pdf/2020_OpenVINS_Research_Platform_for_Visual_Inertial_Estimation.pdf) |
| MIMC-VINS: Multi-IMU Multi-Camera VINS | [pdf/2020_MIMC_VINS_Multi_IMU_Multi_Camera_VINS.pdf](pdf/2020_MIMC_VINS_Multi_IMU_Multi_Camera_VINS.pdf) |
| MAVIS: Multi-Camera Augmented Visual-Inertial SLAM | [pdf/2023_MAVIS_Multi_Camera_Augmented_Visual_Inertial_SLAM.pdf](pdf/2023_MAVIS_Multi_Camera_Augmented_Visual_Inertial_SLAM.pdf) |
| MultiCol-SLAM: A Modular Real-Time Multi-Camera SLAM System | [pdf/2016_MultiCol_SLAM_Modular_Real_Time_Multi_Camera_SLAM.pdf](pdf/2016_MultiCol_SLAM_Modular_Real_Time_Multi_Camera_SLAM.pdf) |
| ORB-SLAM3: Visual, Visual-Inertial and Multi-Map SLAM | [pdf/2021_ORB_SLAM3_Visual_Visual_Inertial_Multimap_SLAM.pdf](pdf/2021_ORB_SLAM3_Visual_Visual_Inertial_Multimap_SLAM.pdf) |
| Multi-Camera Visual-Inertial SLAM for Autonomous Valet Parking | [pdf/2023_Multi_Camera_VISLAM_Autonomous_Valet_Parking.pdf](pdf/2023_Multi_Camera_VISLAM_Autonomous_Valet_Parking.pdf) |
| The TUM VI Benchmark for Evaluating Visual-Inertial Odometry | [pdf/2018_TUM_VI_Benchmark.pdf](pdf/2018_TUM_VI_Benchmark.pdf) |
| Hilti SLAM Challenge 2023 | [pdf/2024_Hilti_SLAM_Challenge_2023.pdf](pdf/2024_Hilti_SLAM_Challenge_2023.pdf) |
| Hilti-Trimble-Oxford 360 Visual-Inertial Benchmark | [pdf/2026_Hilti_Trimble_Oxford_360_VI_Benchmark.pdf](pdf/2026_Hilti_Trimble_Oxford_360_VI_Benchmark.pdf) |
| Calousel: Non-overlapping Multi-camera Calibration | [pdf/2026_Calousel_Non_Overlapping_Multi_Camera_Calibration.pdf](pdf/2026_Calousel_Non_Overlapping_Multi_Camera_Calibration.pdf) |
| Instant Neural Graphics Primitives | [pdf/2022_Instant_NGP_Multiresolution_Hash_Encoding.pdf](pdf/2022_Instant_NGP_Multiresolution_Hash_Encoding.pdf) |
| 3D Gaussian Splatting for Real-Time Radiance Field Rendering | [pdf/2023_3D_Gaussian_Splatting_for_Real_Time_Radiance_Field_Rendering.pdf](pdf/2023_3D_Gaussian_Splatting_for_Real_Time_Radiance_Field_Rendering.pdf) |
| Neural 3D Video Synthesis from Multi-view Video | [pdf/2022_Neural_3D_Video_Synthesis_from_Multi_View_Video.pdf](pdf/2022_Neural_3D_Video_Synthesis_from_Multi_View_Video.pdf) |

未能直接下载但仍建议阅读：

| 论文 / 资料 | 原因 | 链接 |
|---|---|---|
| Unified Temporal and Spatial Calibration for Multi-Sensor Systems | IEEE / 项目页直链不可用，保留 DOI 与 Kalibr wiki | [Kalibr wiki](https://github.com/ethz-asl/kalibr/wiki/Camera-IMU-calibration), [DOI](https://doi.org/10.1109/IROS.2013.6696514) |
| Continuous-Time Batch Estimation Using Temporal Basis Functions | IEEE / 作者页直链不可用，保留 DOI | [DOI](https://doi.org/10.1109/ICRA.2012.6225005) |
| MC-Calib: A Generic and Robust Calibration Toolbox for Multi-Camera Systems | Elsevier 正式 PDF 需要访问权限，保留项目页和 DOI | [GitHub](https://github.com/rameau-fr/MC-Calib), [DOI](https://doi.org/10.1016/j.cviu.2021.103353) |
| Multi-Camera Visual-Inertial Navigation with Online Intrinsic and Extrinsic Calibration | IEEE 正式 PDF 需要访问权限，保留 DOI 和 IEEE 页面 | [IEEE Xplore](https://ieeexplore.ieee.org/document/8793886/), [DOI](https://doi.org/10.1109/ICRA.2019.8793886) |
| EuRoC MAV Dataset paper | SAGE PDF 返回 403，官方 ETH 数据集页可访问 | [ETH ASL](https://projects.asl.ethz.ch/datasets/euroc-mav/), [DOI](https://doi.org/10.1177/0278364915620033) |

## 1. 同步硬件与多传感器采集

| 年份 | 论文 / 资料 | 价值 | 链接 |
|---:|---|---|---|
| 2020 | VersaVIS: An Open Versatile Multi-Camera Visual-Inertial Sensor Suite | 开源多相机 + IMU 同步硬件、固件和 ROS 驱动；重点看 exposure compensation、host clock translation、camera-camera / camera-IMU sync 验证。 | [MDPI](https://www.mdpi.com/1424-8220/20/5/1439), [PubMed](https://pubmed.ncbi.nlm.nih.gov/32155749/), [GitHub](https://github.com/ethz-asl/versavis) |
| 2019 | IEEE 1588-2019 Precision Time Protocol | 网络化多相机系统的时间同步基础；适合 GigE Vision / 分布式采集节点。 | [IEEE SA](https://standards.ieee.org/ieee/1588/6825/) |
| 2026 | GigE Vision 2.0 for Multi-Camera Systems | 工业相机工程参考；说明 PTP + Scheduled Action Command 如何替代部分硬件触发线。 | [Basler](https://www.baslerweb.com/en-us/learning/multi-camera-systems-gige-vision-2-0/) |
| 2024 | Hilti SLAM Challenge 2023 robot hardware notes | 真实系统参考：PTP master、PTP-to-trigger board、相机 start-of-exposure trigger、中心曝光时间戳。 | [GitHub](https://github.com/Hilti-Research/hilti-slam-challenge-2023/blob/main/documentation/hardware/Robot.md) |

工程结论：

- 如果是 2/4/8 路原型，优先硬件触发或 FSYNC，便于测量和定位问题。
- 如果相机数量多、布线距离远、系统分布式，研究 PTP + Scheduled Action。
- 无论哪种方案，都必须记录中心曝光时间戳，而不只是驱动收到图像的时间。

## 2. 标定：Camera、Multi-Camera、Camera-IMU

| 年份 | 论文 / 工具 | 价值 | 链接 |
|---:|---|---|---|
| 2013 | Unified Temporal and Spatial Calibration for Multi-Sensor Systems | Kalibr 的核心论文；研究 Camera-IMU 空间外参与时间偏移的统一估计。 | [Kalibr wiki](https://github.com/ethz-asl/kalibr/wiki/Camera-IMU-calibration), [GitHub](https://github.com/ethz-asl/kalibr) |
| 2012 | Continuous-Time Batch Estimation Using Temporal Basis Functions | 连续时间轨迹建模基础；理解 Kalibr 为什么用 spline 表达传感器运动。 | [Kalibr references](https://github.com/ethz-asl/kalibr/wiki/Camera-IMU-calibration) |
| 2022 | MC-Calib: A Generic and Robust Calibration Toolbox for Multi-Camera Systems | 多相机系统标定工具，覆盖非重叠视场、多目标标定等问题。 | [GitHub](https://github.com/rameau-fr/MC-Calib), [DOI](https://doi.org/10.1016/j.cviu.2021.103353) |
| 2026 | Calousel: Extrinsic Calibration of Non-overlapping Multi-camera Systems from Pure Rotation | 新近非重叠视场外参标定方法；适合研究车载 / 环视 / 大视场相机阵列。 | [arXiv](https://arxiv.org/abs/2606.25646) |
| 2017 | MultiCol Bundle Adjustment | 任意多相机系统的位姿估计、自标定和重建统一 BA 模型。 | [KITopen](https://publikationen.bibliothek.kit.edu/1000067467), [DOI](https://doi.org/10.1007/s11263-016-0935-0) |

工程结论：

- 标定不是一次性脚本，而应成为系统流程：采集规范、标定目标、结果文件、重投影误差、时间偏移、版本记录都要固化。
- 对 MCVS，至少需要保存 `T_rig_cam_i`、`T_imu_cam_i`、camera intrinsics、distortion、time offset、timestamp convention。
- 非重叠视场相机需要额外设计标定动作或辅助装置，不能默认普通棋盘格流程一定可行。

## 3. MC-VIO / VINS

| 年份 | 论文 / 系统 | 价值 | 链接 |
|---:|---|---|---|
| 2018 | VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator | 优化式滑窗 VIO、IMU 预积分、初始化、在线外参/时间标定、回环，是 VINS-Fusion 的基础。 | [DOI](https://doi.org/10.1109/TRO.2018.2853729), [GitHub](https://github.com/HKUST-Aerial-Robotics/VINS-Mono) |
| 2019 | Multi-Camera Visual-Inertial Navigation with Online Intrinsic and Extrinsic Calibration | 真正面向任意数量异步相机的 mc-VINS；重点看 MSCKF 中多相机观测和在线内外参/时间标定。 | [IEEE Xplore](https://ieeexplore.ieee.org/document/8793886/), [DOI](https://doi.org/10.1109/ICRA.2019.8793886) |
| 2020 | OpenVINS: A Research Platform for Visual-Inertial Estimation | 工程友好的 MSCKF / VIO 平台，支持在线相机内外参和 camera-IMU time offset，文档非常适合作为原型工具链。 | [Docs](https://docs.openvins.com/), [GitHub](https://github.com/rpng/open_vins), [DOI](https://doi.org/10.1109/ICRA40945.2020.9196524) |
| 2020 | MIMC-VINS: A Versatile and Resilient Multi-IMU Multi-Camera Visual-Inertial Navigation System | OpenVINS 生态中面向多 IMU、多相机、传感器失效鲁棒性的扩展路线。 | [arXiv](https://arxiv.org/abs/2006.15699) |
| 2019 | VINS-Fusion | VINS-Mono 扩展，支持 stereo、stereo+IMU、GPS 融合；适合做算法基线。 | [GitHub](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) |
| 2023 | MAVIS: Multi-Camera Augmented Visual-Inertial SLAM | 面向多相机部分重叠系统的优化式 VI-SLAM；Hilti SLAM Challenge 2023 表现强，适合研究多相机后端。 | [arXiv](https://arxiv.org/abs/2309.08142) |

工程结论：

- Phase 1 可以先用 OpenVINS / VINS-Fusion 做可跑通基线。
- 如果目标是任意多相机、异步相机和在线标定，重点研究 mc-VINS 与 OpenVINS。
- 如果目标是强鲁棒 SLAM 与复杂场景，研究 MAVIS、ORB-SLAM3 和 Hilti 数据集。

## 4. MC-SLAM 与多相机 Rig 建模

| 年份 | 论文 / 系统 | 价值 | 链接 |
|---:|---|---|---|
| 2016 | MultiCol-SLAM: A Modular Real-Time Multi-Camera SLAM System | 将 ORB-SLAM 扩展到刚性多鱼眼相机系统；提出 MultiKeyframe、多相机 BA、多相机回环等思路。 | [arXiv / DOI](https://doi.org/10.48550/arXiv.1610.07336), [GitHub](https://github.com/urbste/MultiCol-SLAM) |
| 2021 | ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM | 单目、双目、RGB-D、鱼眼、VI 和多地图 SLAM 的强基线；不是任意多相机系统，但非常适合作为 SLAM 框架参考。 | [arXiv](https://doi.org/10.48550/ARXIV.2007.11898), [DOI](https://doi.org/10.1109/TRO.2021.3075644) |
| 2023 | Multi-Camera Visual-Inertial SLAM for Autonomous Valet Parking | 基于 Kimera 扩展多相机和外部里程计，针对真实自动泊车场景。 | [arXiv](https://arxiv.org/abs/2304.13182) |
| 2024 | BundledSLAM: An Accurate Visual SLAM System Using Multiple Cameras | 将多相机测量映射到 BundledFrame / virtual camera，扩展 ORB-SLAM2。 | [IEEE Xplore](https://ieeexplore.ieee.org/document/10503743/) |

工程结论：

- 多相机 SLAM 不是每个相机各跑一套 SLAM，而是估计统一 Rig 位姿 `T_world_rig(t)`。
- 每个相机固定在 Rig 上，外参 `T_rig_cam_i` 是核心系统参数。
- 后端优化需要同时处理多相机观测、相机模型、外参约束和回环。

## 5. 数据集与评测

| 年份 | 数据集 / 论文 | 价值 | 链接 |
|---:|---|---|---|
| 2016 | EuRoC MAV Dataset | 经典 stereo + IMU 数据集，包含同步 IMU、相机内外参和 ground truth；适合 VIO 入门评测。 | [ETH ASL](https://projects.asl.ethz.ch/datasets/euroc-mav/) |
| 2018 | TUM VI Benchmark | 鱼眼 stereo + IMU，硬件同步，高动态范围和光度标定；适合 AR / XR 风格手持运动评测。 | [TUM](https://cvg.cit.tum.de/data/datasets/visual-inertial-dataset), [arXiv](https://arxiv.org/abs/1804.06120) |
| 2022 | Hilti SLAM Challenge Dataset | 真实施工环境，包含视觉、激光、惯性传感器，强调真实世界鲁棒性。 | [IEEE Xplore](https://ieeexplore.ieee.org/document/9797800/), [DOI](https://doi.org/10.1109/LRA.2022.3183759) |
| 2024 | Hilti SLAM Challenge 2023 | 跨传感器配置的 single / multi-session SLAM benchmark。 | [Hugging Face](https://huggingface.co/datasets/Hilti-Research/hilti-slam-challenge-2023), [arXiv](https://arxiv.org/abs/2404.09765) |
| 2026 | Hilti-Trimble-Oxford Dataset: 360 Visual-Inertial Benchmark with Floor Plan Priors | 360 VI SLAM 与建筑平面图先验 benchmark；适合研究最新大视场 VI 系统。 | [GitHub](https://github.com/Hilti-Research/hilti-trimble-slam-challenge-2026), [arXiv](https://arxiv.org/abs/2607.06464) |

工程结论：

- 自研数据格式应尽量接近公开数据集的字段：图像、IMU、calibration、ground truth、timestamp convention、frame id。
- 评测至少保存 ATE、RPE、丢帧率、时间戳抖动、重投影误差、轨迹完整率。

## 6. 多视角重建、NeRF 与 3DGS

| 年份 | 论文 / 系统 | 价值 | 链接 |
|---:|---|---|---|
| 2022 | Neural 3D Video Synthesis from Multi-view Video | 多视角同步视频到动态神经表示；适合研究高质量多相机采集对动态重建的要求。 | [Project](https://neural-3d-video.github.io/), [GitHub](https://github.com/facebookresearch/Neural_3D_Video), [DOI](https://doi.org/10.1109/CVPR52688.2022.00544) |
| 2022 | Instant Neural Graphics Primitives with a Multiresolution Hash Encoding | 快速 NeRF / SDF / neural graphics primitives，适合原型阶段快速验证重建链路。 | [GitHub](https://github.com/NVlabs/instant-ngp), [DOI](https://doi.org/10.1145/3528223.3530127) |
| 2023 | 3D Gaussian Splatting for Real-Time Radiance Field Rendering | 实时高质量 novel-view synthesis，适合后续 MCVS 的 3D 表示和可视化路线。 | [ACM](https://doi.org/10.1145/3592433) |

工程结论：

- 3D 重建质量高度依赖相机同步、曝光一致性、标定质量和多视角覆盖。
- 动态重建比静态重建更严格：时间错位会直接表现为 ghosting、几何撕裂和纹理错位。

## 7. 建议阅读顺序

1. VersaVIS：先建立硬件同步、中心曝光时间戳和 camera-IMU 同步的工程意识。
2. Kalibr + MC-Calib：理解系统标定需要哪些参数、数据和验证报告。
3. OpenVINS + mc-VINS：研究多相机观测如何进入 VIO 状态估计。
4. MultiCol-SLAM + ORB-SLAM3 + MAVIS：研究 Rig 位姿、BA、回环和多地图。
5. EuRoC / TUM-VI / Hilti：用公开数据建立评测标准。
6. Neural 3D Video / 3DGS：把同步多视角数据延伸到高质量重建和应用。
