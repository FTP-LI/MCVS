# 官方资料与论文阅读导航

核对日期：2026-10-31。优先使用作者、大学、设备厂商和项目官方资料。每周只读解决当前任务的一小部分，建议先读本地中文手册，再查原文。外部网页和软件版本会变化，进入对应阶段时再次核对。

## 按编号查资料

| 编号 | 官方来源 | 使用周次与最小阅读范围 | 语言 / 成本 / 前提 |
|---|---|---|---|
| R01 | [Harvard CS50P](https://cs50.harvard.edu/python/) | 1–3 周：Functions, Variables；Conditionals；Loops。随后按需读 Exceptions、Libraries、File I/O，每次 30–45 分钟 | 英文免费 OCW；可零编程基础入门，不要求购买证书 |
| R02 | [Python 中文教程](https://docs.python.org/zh-cn/3/tutorial/)；[Windows 安装说明](https://docs.python.org/zh-cn/3/using/windows.html) | 1–3 周：运行、数值、控制流；作为查语法的资料 | 官方中文；教程面向有基本编程概念者，先看本地示例 |
| R03 | [NumPy absolute beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) | 4 周：数组创建、shape、索引、统计；不读完全部 API | 英文免费；先会变量、循环和函数 |
| R04 | [OpenCV-Python 教程入口](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) | 5–6 周读 GUI Features、Core Operations 中的图像/视频读写；20 周读 Feature Detection and Description | 英文免费；先会数组，不需要先读 C++ |
| R05 | [3Blue1Brown 线性代数主题](https://www.3blue1brown.com/topics/linear-algebra) | 7–8 周：Vectors、Linear combinations、Linear transformations、Matrix multiplication；23 周再看局部变化率的直觉 | 作者英文内容；作者站链接的 [Bilibili 频道](https://space.bilibili.com/88461692) 可查中文内容，逐个核对字幕来源 |
| R06 | [高翔《视觉 SLAM 十四讲》第二版作者代码](https://github.com/gaoxiang12/slambook2) | 8–12 周选三维刚体运动、相机模型；22–24 周选非线性优化与视觉里程计；先看图和例子 | 中文书可借阅/合法购买；仓库代码不是整本书的免费授权 |
| R07 | [OpenCV 相机标定](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)；[双目深度示例](https://docs.opencv.org/4.x/dd/d53/tutorial_py_depthmap.html)；[calib3d API](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) | 9–12 周：object/image points、角点、calibrateCamera、projectPoints；19–21 周：stereoCalibrate、stereoRectify、视差 | 英文免费；先理解坐标与单位。我们的棋盘是 8×5 内角点，不照抄教程的格数 |
| R08 | [XIAO nRF52840 系列官方入门](https://wiki.seeedstudio.com/XIAO_BLE/)；[Sense 官方商店](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html) | 13–14 周：型号差异、板卡包、USB、引脚和开发环境 | 英文免费；硬件另购，确认 SKU 102010469 |
| R09 | [XIAO Sense IMU 教程](https://wiki.seeedstudio.com/XIAO-BLE-Sense-IMU-Usage/)；[Seeed LSM6DS3 官方库](https://github.com/Seeed-Studio/Seeed_Arduino_LSM6DS3) | 14–18 周：HighLevelExample、单位、轴方向；先原样运行再加日志 | 英文免费；先认识加速度和角速度，记录实际安装版本 |
| R10 | [VersaVIS 作者项目](https://github.com/ethz-asl/versavis)；[本地论文](../pdf/2020_VersaVIS_Open_Versatile_Multi_Camera_Visual_Inertial_Sensor_Suite.pdf) | 17–18 周只看系统结构与时间关系；29 周读摘要、图、同步实验、结论 | 英文论文；带着“如何证明同步”这个问题读，不要求复造硬件 |
| R11 | [OpenVINS 作者项目](https://github.com/rpng/open_vins)；[官方安装](https://docs.openvins.com/gs-installing.html)；[简单教程](https://docs.openvins.com/gs-tutorial.html)；[本地论文](../pdf/2020_OpenVINS_Research_Platform_for_Visual_Inertial_Estimation.pdf) | 25–30 周：版本、配置、数据、运行、评测；论文优先系统图与实验 | 英文免费；需要编程/坐标/IMU 基础，完整推导后置 |
| R12 | [ETH EuRoC 数据集](https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets)；[OpenVINS 数据集说明](https://docs.openvins.com/gs-datasets.html) | 26–28 周选一个较易序列如 MH_01_easy；读 sensor.yaml、时间格式、相机/IMU/参考轨迹说明 | 英文公开数据；下载前确认许可、格式和剩余空间，不一次下载全库 |
| R13 | [OpenVINS ROS-free 安装](https://docs.openvins.com/gs-installing-free.html) | 25–27 周作为减少 ROS 依赖的候选；理解 `run_simulation` 是模拟输入 | 英文免费；官方明确该接口支持有限，不能保证当前机器一键构建 |
| R14 | [evo 作者项目](https://github.com/MichaelGrupp/evo)；[格式说明](https://github.com/MichaelGrupp/evo/wiki/Formats)；[指标说明](https://github.com/MichaelGrupp/evo/wiki/Metrics) | 28 周：格式、时间关联、APE/RPE、对齐与保存结果，先看 `--help` | 英文免费；适用于轨迹评测，不替代传感器同步验证 |
| R15 | [ROS Noetic 生命周期公告](https://www.ros.org/blog/noetic-eol/)；[ROS 2 版本表](https://docs.ros.org/en/jazzy/Releases.html) | 25 周：核对软件实际支持的系统、ROS、编译器与依赖版本 | Noetic 已于 2025-05-31 结束官方维护；ROS 2 较新版本存在不等于 OpenVINS 已兼容 |

以上索引给出小节/关键词而非要求每周读完一本书。`Rxx` 是本地导航编号，不是论文质量排名。

## 研究环境的选择原则

截至核对时，OpenVINS 安装文档仍列出 Ubuntu 16.04/18.04/20.04 及旧 ROS 组合，也说明 ROS-free 构建支持有限。因此不把“Windows 上装最新 Ubuntu + 最新 ROS”写成必然可行的命令。

第 25 周先填写环境矩阵：OS、架构、项目提交哈希、编译器、OpenCV/Eigen/Ceres、是否使用 ROS、数据格式。优先选当前项目明确支持且有现成示例的组合，使用隔离环境记录过程。ROS-free 路径减少 ROS 依赖，但仍要验证依赖与示例运行；它不是省掉所有环境工作的捷径。

遇到超过 2 小时的构建阻塞，先完成公开/模拟轨迹分析，并保留错误记录；G5 保持“预备”，之后安排补课。只打印程序帮助、只看他人视频或只分析他人结果都不算实际 VIO 运行。

## 论文阅读顺序与产出

1. 第 29 周：VersaVIS。目标是回答传感器结构、触发与时间戳、同步如何验证、结论适用于什么条件。先摘要和系统图，再读实验，方法推导按需查。
2. 第 30 周：OpenVINS。目标是画出输入、状态、传播、观测更新和输出的关系，并把自己运行的配置与论文实验条件分开。
3. G5 之后：根据问题查 [原论文索引](../papers.md)。需要 Camera-IMU 标定再看标定工具；需要多相机算法再看 MIMC-VINS、MAVIS、MultiCol；需要回环与地图再看 ORB-SLAM3。重建与 3DGS 放到几何基础和数据质量稳定之后。

每篇只交一页读书卡：问题；输入输出；关键假设；一张自己重画的系统图；最支持结论的实验；作者承认的限制；与当前 1000 元学习原型的差距；三个仍不理解的问题。

原有 15 篇英文 PDF 和方案调研继续保留。本地中文学习手册是原创教学内容，**不充当论文全文译本或官方译本**。[全文翻译清单](../translation/README.md)仍单独记录真实进度；后续使用专业服务的机器翻译，也应标明服务、日期、版本和人工复核情况。
