"""Build MCVS learning artifacts; never write learner progress or reports."""

import argparse
import html
import json
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image,
    KeepTogether,
)

ROOT = Path(__file__).resolve().parents[1]
INK = "#223B38"
GREEN = "#176B55"
PAPER = "#FAF8F2"
MUTED = "#5F706A"
LINE = "#D7DFD8"


def load_course():
    course = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
    assert [w["week"] for w in course["weeks"]] == list(range(1, 37))
    assert len(course["phases"]) == 6
    for phase in course["phases"]:
        assert sum(w["phase"] == phase["id"] for w in course["weeks"]) == 6
    total = sum(x["qty"] * x["unit_cap"] for x in course["budget"])
    core = sum(x["qty"] * x["unit_cap"] for x in course["budget"] if x["required"])
    assert total == course["hardware_budget_cny"] == 1000
    assert core == 520
    return course


def curriculum(course):
    lines = ["# 36 周学习课程", "",
             "由 [course.json](course.json) 生成。每周 4–6 小时，共约 144–216 小时；可按实际进度延长。",
             "先读 [学习入口](README.md)，实验步骤见 [任务书](labs.md)，资料编号见 [资料导航](resources.md)。",
             "预备练习不自动替代正式关卡，个人完成记录只写在 [进度表](progress.md)。", ""]
    labs = {"A": "L01–L03", "B": "L04–L05", "C": "L06–L07",
            "D": "L08–L09", "E": "L10", "F": "L11–L12"}
    for phase in course["phases"]:
        lines += [f"## {phase['id']}｜第 {phase['weeks']} 周：{phase['name']}", "",
                  phase["goal"] + "。", "", f"对应实验：{labs[phase['id']]}。", "",
                  "**阶段验收：** " + phase["gate"], ""]
        for week in (w for w in course["weeks"] if w["phase"] == phase["id"]):
            lines += [f"### 第 {week['week']:02d} 周｜{week['title']}", "",
                      "- 理论：" + week["theory"], "- 动手：" + week["practice"],
                      "- 交付：" + week["evidence"], "- 检查：" + week["check"],
                      "- 阅读：" + "、".join(week["resources"]) + "（每次先选 30–45 分钟的小节）。", ""]
    lines += ["## 暂停、补课与延长", "",
              "连续排错超过两小时，记录环境、命令、第一条错误与已排除原因，完成对应预备任务。",
              "每六周复盘一次；未达到标准的关卡保持未勾选。第 36 周若 G5 未通过，继续补实际 VIO 运行，不宣称整条路径完成。", ""]
    (ROOT / "curriculum.md").write_text("\n".join(lines), encoding="utf-8")


def draw_wrapped(draw, text, pos, font, fill, max_width, leading):
    x, y = pos
    line = ""
    for character in text:
        if character == "\n" or (line and draw.textlength(line + character, font=font) > max_width):
            draw.text((x, y), line, font=font, fill=fill)
            y += leading
            line = "" if character == "\n" else character
        else:
            line += character
    if line:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def roadmap(course, font_path, bold_path):
    image = PILImage.new("RGB", (1800, 1200), PAPER)
    draw = ImageDraw.Draw(image)
    regular = lambda size: ImageFont.truetype(str(font_path), size, index=0)
    bold = lambda size: ImageFont.truetype(str(bold_path), size, index=0)
    draw.text((80, 52), "MCVS / 从零开始的学习路线", font=bold(54), fill=INK)
    draw.text((84, 138), "每周 4–6 小时  ·  36 周可延长  ·  按证据过关", font=regular(29), fill=MUTED)
    outputs = ["程序、图像、记录文件", "实测棋盘、内参、留出检查", "六轴数据、静止统计、时间线",
               "静态双目结果、融合数据流", "版本、运行日志、轨迹与评测", "原始数据、诊断、复现报告"]
    for index, phase in enumerate(course["phases"]):
        row, col = divmod(index, 2)
        x, y = 80 + col * 840, 220 + row * 272
        draw.rounded_rectangle((x, y, x + 800, y + 240), radius=18, fill="white", outline=LINE, width=2)
        draw.rounded_rectangle((x, y, x + 12, y + 240), radius=6, fill=phase["color"])
        draw.text((x + 34, y + 22), f"0{index + 1}  /  第 {phase['weeks']} 周", font=bold(25), fill=phase["color"])
        draw.text((x + 34, y + 67), phase["name"], font=bold(36), fill=INK)
        draw_wrapped(draw, phase["goal"], (x + 34, y + 127), regular(27), MUTED, 730, 36)
        draw_wrapped(draw, "交付：" + outputs[index], (x + 34, y + 180), regular(25), INK, 730, 33)
    draw.text((84, 1067), "核心采购上限 520 元  /  全部硬件预算不超过 1000 元", font=bold(30), fill=GREEN)
    draw.text((84, 1120), "今天先做第一周行动单；先不采购。G5 须实际运行 VIO，轨迹分析仅为预备。", font=regular(25), fill=MUTED)
    image.save(ROOT / "assets/roadmap.png")


def make_styles():
    base = dict(fontName="MCVS", textColor=colors.HexColor(INK), wordWrap="CJK")
    return {
        "body": ParagraphStyle("body", fontSize=10, leading=17, spaceAfter=8, **base),
        "small": ParagraphStyle("small", fontSize=8.7, leading=14, spaceAfter=5, **base),
        "week": ParagraphStyle("week", fontSize=9.1, leading=14.3, spaceAfter=4, **base),
        "h1": ParagraphStyle("h1", fontName="MCVS-Bold", fontSize=24, leading=34,
                             spaceAfter=15, textColor=colors.HexColor(INK), wordWrap="CJK"),
        "h2": ParagraphStyle("h2", fontName="MCVS-Bold", fontSize=13, leading=21,
                             spaceBefore=8, spaceAfter=7, textColor=colors.HexColor(GREEN), wordWrap="CJK"),
        "h3": ParagraphStyle("h3", fontName="MCVS-Bold", fontSize=10.5, leading=17,
                             spaceBefore=6, spaceAfter=3, textColor=colors.HexColor(GREEN), wordWrap="CJK"),
        "caption": ParagraphStyle("caption", fontName="MCVS", fontSize=8.4, leading=13,
                                  textColor=colors.HexColor(MUTED), spaceAfter=6, wordWrap="CJK"),
        "hero": ParagraphStyle("hero", fontName="MCVS-Bold", fontSize=35, leading=48,
                               spaceAfter=16, textColor=colors.HexColor(INK), wordWrap="CJK"),
    }


def guide(course):
    styles = make_styles()
    story = []
    esc = lambda text: html.escape(str(text)).replace("–", "-")
    def p(text, style="body", raw=False):
        return Paragraph(text if raw else esc(text), styles[style])
    def add(text, style="body"):
        story.append(p(text, style))
    def page(title, subtitle):
        if story:
            story.append(PageBreak())
        add(title, "h1")
        add(subtitle, "caption")
    def box(title, text):
        table = Table([[p(title, "h2")], [p(text)]], colWidths=[499])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF3ED")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor(LINE)),
            ("LEFTPADDING", (0, 0), (-1, -1), 13),
            ("RIGHTPADDING", (0, 0), (-1, -1), 13),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.extend([table, Spacer(1, 12)])
    def table(rows, widths, header=True):
        converted = [[p(cell, "small") for cell in row] for row in rows]
        item = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
        commands = [("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor(LINE)),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]
        if header:
            commands.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7EEE7")))
        item.setStyle(TableStyle(commands))
        story.extend([item, Spacer(1, 10)])

    # 1. Cover
    add("MCVS  /  LEARNING FIELD GUIDE", "caption")
    story.append(Spacer(1, 30))
    add("从零认识\n多相机视觉", "hero")
    add("把图像、运动和时间，变成可以检查的实验。", "h2")
    story.append(Spacer(1, 24))
    table([["36 周", "4-6 小时 / 周", "1000 元以内"],
           ["六个阶段，按能力推进", "总工作量约 144-216 小时", "沿用现有电脑，分阶段购买"]], [166, 166, 167])
    story.append(Spacer(1, 14))
    box("这本手册适合谁", "当前理论基础较少，希望从编程与单位开始，逐步学会单相机标定、IMU 采集、时间戳诊断、静态双目和已有 VIO 示例的学习者。")
    add("今天的第一步", "h2")
    add("计算 30 fps 对应多少毫秒，再运行 first_steps.py。第一周不需要采购，也不要求读完论文。")
    add("使用顺序", "h2")
    add("先看路线与第一周行动，再查每周课程。具体实验步骤在同目录 labs.md；完整中文解释在 foundations.md；实际记录写入 progress.md。打印版是便携总览，配套文件提供操作细节。")
    story.append(Spacer(1, 14))
    add("编制日期：2026-10-31  |  预算与时间依据用户确认", "caption")
    add("本手册为原创中文教学整理，不是论文全文翻译。教材编制完成不代表学习者已完成学习；所有学习关卡从未通过开始。", "caption")

    # 2. Route
    page("先知道要走到哪里", "路线总览 / 不以买了多少器材或看了多少论文计进度")
    story.append(Image(str(ROOT / "assets/roadmap.png"), width=499, height=499 * 1200 / 1800))
    story.append(Spacer(1, 16))
    add("每周的固定节奏", "h2")
    table([["环节", "建议时间", "要留下的东西"],
           ["解释与阅读", "60-90 分钟", "一个概念，用自己的话写清"],
           ["动手实验", "120-180 分钟", "输入、脚本、结果或图像"],
           ["记录", "30-45 分钟", "单位、参数、版本、异常"],
           ["闭卷复盘", "30-45 分钟", "证据链接和一个待解决问题"]], [100, 105, 294])
    add("36 周是估算工作量。需要补课就重复该周；连续排错两小时后记录问题并转预备任务。预备任务不会替代正式关卡。", "small")

    # 3. First week
    page("第一周行动单", "4-6 小时 / 不采购 / 对照 first_week.md 操作")
    table([["时段", "做什么", "完成标志"],
           ["20 分钟", "建立自己的 week01 笔记", "写出相机、IMU、时间各提供什么"],
           ["40 分钟", "手算帧间隔和原始图像数据量", "每一步带单位"],
           ["40-60 分钟", "检查 Python 3，运行示例", "保留原始输出"],
           ["60-90 分钟", "先预测，再做三次参数修改", "记录预测与结果"],
           ["60-90 分钟", "少量课程阅读与闭卷复盘", "不用复制教材也能说明结果"]], [90, 205, 204])
    add("项目根目录中的运行命令", "h2")
    box("PowerShell", "py .\\doc\\learning\\examples\\first_steps.py\n如果使用 python 命令，则把 py 替换为 python。示例只用标准库。")
    table([["修改", "预期", "关键解释"],
           ["FPS：30 → 60", "33.333 → 16.667 ms", "每秒帧数翻倍，间隔减半"],
           ["POINT_Z_M：2 → 4", "u：380 → 350 px", "深度变大，投影靠近主点"],
           ["DISPARITY_PX：30 → 15", "深度：1.2 → 2.4 m", "理想平行双目深度与视差成反比"]], [170, 160, 169])
    add("遇到报错", "h2")
    add("先确认当前目录、文件扩展名、Python 版本，再看第一条错误。保留完整命令与错误上下文。不能运行时先完成手算，运行项仍记为待补。")
    add("本周交付", "h2")
    add("一页笔记、原始输出、三次修改的预测与结果。不要覆盖教材中的行动单，把自己的记录放在个人学习目录。")

    # 4. Geometry
    page("三个数学入口", "先检查输入、输出和单位，再记公式")
    add("01  图像是数组", "h2")
    add("灰度图通常为 (height, width)，三通道图为 (height, width, 3)。像素写作 (u,v)，数组通常访问 [v,u]。OpenCV 常见输入为 BGR，三通道本身不能说明颜色顺序。")
    box("原始数据量例子", "2 × 1280 × 720 × 1 B × 30 fps = 55.296 MB/s；十分钟约 33.178 GB。只估算未压缩负载，不含传输开销，也不是摄像头实测吞吐。")
    add("02  外参必须写方向", "h2")
    add("本手册约定 T_A_B 将 B 系坐标变成 A 系坐标：p_A = R_AB p_B + t_AB。逆变换为 p_B = R_AB 的转置 × (p_A - t_AB)。别人的文件可能用相反命名，读配置时先核对。")
    add("点 (1,0) 先旋转 90° 再沿 x 平移 1 得到 (1,1)；先平移再旋转得到 (0,2)。变换次序通常不能交换。")
    add("03  投影和深度先看前提", "h2")
    table([["模型", "算例", "前提"],
           ["u = fx X/Z + cx", "600 × 0.2/2 + 320 = 380 px", "针孔、无畸变、Z>0；fx 为像素单位"],
           ["Z = f B/d", "600 × 0.06/30 = 1.2 m", "已标定并校正的平行双目，主点约定一致"]], [130, 170, 199])
    add("现在不要求推导完整滤波器。先掌握单位换算、坐标变换、投影，再逐渐补标准差、积分、最小二乘和不确定性。详解与退出题见 foundations.md。")

    # 5. IMU and clock
    page("运动与时间：最容易误解的部分", "真实采样事件、软件读取事件和主机收到事件必须分清")
    add("IMU 静止为什么不是全零", "h2")
    add("加速度计测比力。静止放置时模长通常约 1 g，各轴正负取决于方向；陀螺仪接近零但含偏置与噪声。g 转 m/s² 乘 9.80665；deg/s 转 rad/s 乘 π/180。")
    box("偏置会积累", "简化例：陀螺偏置 0.05°/s，60 秒产生 3° 积分误差；加速度偏置 0.1 m/s²，10 秒双重积分产生 5 m 位置误差。这不是推荐板卡的实测性能。")
    add("每一列时间戳都要有事件说明", "h2")
    table([["字段例子", "实际含义", "不能直接声称"],
           ["host_after_read_ns", "主机读完图像后的单调时钟", "相机曝光时间"],
           ["device_read_us", "开发板软件读取时的计时", "精确 IMU 硬件采样时间"],
           ["host_receive_ns", "主机收到串口记录的时间", "已与相机同步"]], [156, 172, 171])
    add("设备时钟原点与速率不同，不能直接相减；主机时间含缓存与传输延迟。卷帘快门还要说明逐行时间，不能用一个中心曝光时刻代表整张图。")
    add("能做的诊断与结论边界", "h2")
    add("分别在同一时钟域统计间隔、重复、倒序和长间隔。没有硬件序号时，异常间隔只是可疑丢帧证据。普通 USB 摄像头加独立 IMU 可以学习诊断，但尚未构成已同步的 VIO 传感器。")
    add("六轴 IMU 不提供长期稳定绝对偏航与位置；加速度方向估计倾斜时还要考虑快速平移的干扰。")

    # 6-11. Weekly curriculum
    for phase in course["phases"]:
        page(f"{phase['id']}  {phase['name']}", f"第 {phase['weeks']} 周 / " + phase["goal"])
        for week in (w for w in course["weeks"] if w["phase"] == phase["id"]):
            block = [p(f"{week['week']:02d}  {week['title']}", "h3"),
                     p("要点：" + week["theory"] + " 练习：" + week["practice"], "week"),
                     p("交付：" + week["evidence"] + " 检查：" + week["check"], "week")]
            story.append(KeepTogether(block))
        story.append(Spacer(1, 8))
        box("阶段验收", phase["gate"])
        add("详细步骤见 labs.md；资料编号与官方链接见 resources.md。按证据过关，实际用时可延长。", "caption")

    # 12. Hardware
    page("硬件：先买够用的", "核对 2026-10-31 / 人民币金额是采购上限，不是国内成交报价")
    add("已有 Ryzen 5 9600X 与 RTX 5070 的电脑可沿用；前半程不依赖 CUDA。相机优先用已有设备。需要购买时参考罗技 C270；IMU 参考 XIAO nRF52840 Sense，注意 Sense 后缀。")
    rows = [["项目", "上限 / 元", "采购时间"]]
    rows += [[item["item"], str(item["qty"] * item["unit_cap"]), item["stage"]] for item in course["budget"]]
    rows += [["总额：核心 520 + 可选 320 + 预留 160", "1000", "按阶段决定"]]
    table(rows, [282, 68, 149])
    add("型号核对", "h2")
    add("C270 官方列出 720p/30 fps、55° 对角视场；本次没有确认外触发能力。XIAO nRF52840 Sense（SKU 102010469）带 LSM6DS3TR-C 六轴 IMU，可先用 USB 与官方例程，不必焊接。", "small")
    add("官方海外页核对价：C270 为 29.99 美元，XIAO Sense 为 15.90 美元；不包含中国到手价与运费。超过本表上限就借用或先做公开数据，不突破总预算。来源链接及验收表见 hardware.md。", "small")

    # 13. Calibration
    page("第一次标定，如何判断做对了", "L05 / 第 10-12 周 / 对应 G2")
    table([["顺序", "动作", "必须保留"],
           ["1", "100% 打印棋盘，贴平，测横纵校验尺", "实际格长；不能直接沿用标称 20 mm"],
           ["2", "数出 8×5 内角点、9×6 方格", "角点检测图和顺序"],
           ["3", "采集约 20 张训练与 8 张留出图", "原图、分组清单、剔除原因"],
           ["4", "固定尺寸与设置，拟合内参/畸变", "K、模型、系数、尺寸、版本"],
           ["5", "计算每图误差，检查留出图与直线", "逐图误差、对照图、异常说明"]], [40, 224, 235])
    box("棋盘的数量关系", "8×5 内角点意味着 9×6 方格。配套 PDF 的设计格长为 20 mm，整块棋盘为 180×120 mm。打印选择实际大小，横纵比例错误或纸面弯曲需要重做。")
    add("误差怎么解释", "h2")
    add("本方案每图误差为二维角点欧氏距离的 RMS，即 sqrt(mean(dx²+dy²))。留出图不参与内参拟合，但其棋盘姿态仍从该图估计，因此只是额外一致性检查。")
    add("多数清晰棋盘图约 1 px 内可作为初步排查目标，不是适用于所有相机和模型的通用阈值。训练误差小不自动证明物理精度；两次参数接近只说明重复性。")
    add("先查数据，再改算法", "h2")
    add("格数、点序、格长单位、图像分辨率、棋盘平整度、模糊与边缘覆盖，都可能影响结果。分辨率、裁剪、镜头或对焦变化后，应重新检查内参适用性。")

    # 14. VIO
    page("第一次研究系统复现", "L10 / 第 25-30 周 / 对应 G5")
    add("先写环境矩阵", "h2")
    add("记录 OS、编译器、OpenCV/Eigen/Ceres、项目提交、ROS 与数据格式。OpenVINS 官方文档仍包含较旧环境；ROS Noetic 于 2025-05-31 结束官方维护。新的 ROS 版本存在，不代表项目已兼容。")
    table([["路径", "输入与产出", "结论边界"],
           ["官方教程 + 公开数据", "选一个序列，运行估计器，保存配置、日志和轨迹", "结果只代表该版本与序列"],
           ["ROS-free 模拟器", "run_simulation、模拟配置与真值、估计轨迹", "官方支持有限；属于模拟输入验证"],
           ["预备轨迹分析", "用模拟或已有轨迹练时间匹配、对齐和误差", "未实际运行 VIO，G5 不通过"]], [108, 218, 173])
    add("评测必须说明", "h2")
    add("参考来源、时间关联容差、匹配样本数、单位、对齐方式、APE/RPE 定义、失败区间与完成比例。有公制尺度的 VIO 优先报告 SE(3) 对齐；不能悄悄用尺度校正掩盖尺度误差。")
    box("G5 需要什么", "实际运行已有 VIO 估计器（公开数据或官方模拟输入均可），并保存可追溯版本、配置、运行日志、输出轨迹、参考与评测。模拟结果明确标注；本手册没有声称已经在当前电脑验证构建成功。")
    add("读两篇论文就够开始", "h2")
    add("VersaVIS：系统结构、触发与时间戳、同步如何验证。OpenVINS：输入、状态、传播、观测更新与评测条件。每篇交一页读书卡，完整推导后置。", "small")

    # 15. Reference map
    page("资料导航与教材维护", "链接可点击 / 完整周次与阅读范围见 resources.md")
    links = [
        ("R01", "Harvard CS50P：函数、变量、条件、循环", "https://cs50.harvard.edu/python/"),
        ("R02", "Python 中文教程：语法参考，先补编程概念", "https://docs.python.org/zh-cn/3/tutorial/"),
        ("R03", "NumPy：数组、形状、索引、统计", "https://numpy.org/doc/stable/user/absolute_beginners.html"),
        ("R04", "OpenCV-Python：图像、视频、特征", "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"),
        ("R05", "3Blue1Brown：向量与线性变换", "https://www.3blue1brown.com/topics/linear-algebra"),
        ("R06", "视觉 SLAM 十四讲：作者代码，书可借阅", "https://github.com/gaoxiang12/slambook2"),
        ("R07", "OpenCV 标定：角点、内参、重投影", "https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html"),
        ("R08", "XIAO 官方入门：型号与开发环境", "https://wiki.seeedstudio.com/XIAO_BLE/"),
        ("R09", "XIAO IMU：HighLevelExample 与官方库", "https://wiki.seeedstudio.com/XIAO-BLE-Sense-IMU-Usage/"),
        ("R10", "VersaVIS 作者项目：同步系统", "https://github.com/ethz-asl/versavis"),
        ("R11", "OpenVINS 官方文档：版本与教程", "https://docs.openvins.com/gs-installing.html"),
        ("R12", "OpenVINS 数据集页：EuRoC 等序列入口", "https://docs.openvins.com/gs-datasets.html"),
        ("R13", "OpenVINS ROS-free：模拟器路径", "https://docs.openvins.com/gs-installing-free.html"),
        ("R14", "evo：轨迹格式、APE/RPE、对齐", "https://github.com/MichaelGrupp/evo"),
        ("R15", "ROS 生命周期：Noetic 维护结束公告", "https://www.ros.org/blog/noetic-eol/"),
    ]
    for ref, label, url in links:
        story.append(p(f'<b>{ref}</b>  <link href="{url}" color="#276C9C">{esc(label)}</link>', "body", raw=True))
    add("每次只看当前需要的小节", "h2")
    add("先读本地中文解释，英文资料每次 30-45 分钟。官方 Python 教程不是纯零基础编程教材。原论文 PDF 继续保留；中文全文翻译状态独立维护，不把本手册当作官方译本。", "small")
    add("结构化课程位于 course.json；tools/build_materials.py 可重建周计划、路线图和两份 PDF，不覆盖 progress.md 或个人报告。每六周根据实际卡点修订一次。", "small")

    # 16. Printable learner progress
    page("我的进度：用证据勾选", "初始全部未完成 / 日期、用时和文件路径在 progress.md 中记录")
    rows = [["第 01-12 周", "第 13-24 周", "第 25-36 周"]]
    for index in range(12):
        row = []
        for offset in (0, 12, 24):
            week = course["weeks"][index + offset]
            row.append(f"[  ] {week['week']:02d}  {week['title']}")
        rows.append(row)
    table(rows, [166, 166, 167])
    add("关卡复核", "h2")
    add("[  ] G1 程序与单位    [  ] G2 真实相机标定    [  ] G3 真实 IMU 与时间", "small")
    add("[  ] G4 静态双目/样例与融合图    [  ] G5 实际 VIO 运行    [  ] G6 项目报告", "small")
    add("G6 项目交付通过不替代 G1-G5；六个关卡均通过才标记整条学习路径完成。", "small")
    add("本次最需要补的概念：________________________________", "body")
    add("下一步的一件事：____________________________________", "body")
    add("累计用时：________ 小时     实际采购：________ 元", "body")

    def decoration(c, doc):
        c.saveState()
        width, height = A4
        c.setFillColor(colors.HexColor(PAPER))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        c.setFillColor(colors.HexColor(GREEN))
        c.rect(0, height - 9, width, 9, fill=1, stroke=0)
        c.setFont("MCVS", 8)
        c.setFillColor(colors.HexColor(MUTED))
        c.drawString(48, height - 32, "MCVS  /  零基础学习手册")
        c.drawRightString(width - 48, height - 32, "36 周 · 每周 4-6 小时")
        c.setStrokeColor(colors.HexColor(LINE))
        c.line(48, 39, width - 48, 39)
        c.drawString(48, 25, "2026-10-31  |  与本地学习材料配套使用")
        c.drawRightString(width - 48, 25, f"{doc.page:02d}")
        c.restoreState()

    doc = SimpleDocTemplate(str(ROOT / "MCVS_learning_guide.pdf"), pagesize=A4,
                            rightMargin=48, leftMargin=48, topMargin=57, bottomMargin=52,
                            title="MCVS 零基础学习手册", author="MCVS Learning Materials")
    doc.build(story, onFirstPage=decoration, onLaterPages=decoration)


def checkerboard():
    target = ROOT / "assets/checkerboard_8x5_20mm.pdf"
    c = canvas.Canvas(str(target), pagesize=A4)
    c.setTitle("MCVS 8x5 inner-corner checkerboard - 20 mm nominal")
    c.setAuthor("MCVS Learning Materials")
    width, height = A4
    c.setFont("MCVS-Bold", 16)
    c.drawString(15 * mm, height - 23 * mm, "相机标定棋盘 / 8×5 内角点")
    c.setFont("MCVS", 10)
    c.drawString(15 * mm, height - 34 * mm, "9×6 方格，标称格长 20 mm；整块棋盘 180×120 mm。")
    c.drawString(15 * mm, height - 42 * mm, "打印选实际大小 100%，关闭适应页面；打印后实测格长。")
    x0, y0, square = 15 * mm, 110 * mm, 20 * mm
    c.setFillColor(colors.black)
    for row in range(6):
        for col in range(9):
            if (row + col) % 2 == 0:
                c.rect(x0 + col * square, y0 + row * square, square, square, fill=1, stroke=0)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.4)
    # Horizontal 100 mm reference, outside corner-detection region.
    x, y = 20 * mm, 84 * mm
    c.line(x, y, x + 100 * mm, y)
    for tick in range(11):
        c.line(x + tick * 10 * mm, y - 2 * mm, x + tick * 10 * mm, y + 2 * mm)
    c.setFont("MCVS", 9)
    c.drawString(x, y - 9 * mm, "横向两端距离应为 100 mm")
    # Vertical 100 mm reference in the left margin, clear of board by 7 mm.
    xv, yv = 7 * mm, 120 * mm
    c.line(xv, yv, xv, yv + 100 * mm)
    for tick in range(11):
        c.line(xv - 1.5 * mm, yv + tick * 10 * mm, xv + 1.5 * mm, yv + tick * 10 * mm)
    c.saveState()
    c.translate(4 * mm, yv)
    c.rotate(90)
    c.setFont("MCVS", 6.5)
    c.drawString(8 * mm, 0, "纵向 100 mm 校验尺")
    c.restoreState()
    c.setFont("MCVS", 10)
    for offset, text in enumerate([
        "实测连续 5 格总长度：________ mm；单格：________ mm",
        "横、纵方向都应检查；比例不同、纸面弯曲或反光时重做。",
        "贴在平整硬板上，固定分辨率与镜头设置，避免运动模糊。",
        "对象点用实测格长；OpenCV patternSize = (8, 5)。",
    ]):
        c.drawString(15 * mm, (61 - offset * 9) * mm, text)
    c.setFont("MCVS", 8)
    c.drawString(15 * mm, 17 * mm, "MCVS / 学习用标定靶 / 2026-10-31 / 详细步骤见 labs.md 的 L05")
    c.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=Path("C:/Windows/Fonts/msyh.ttc"))
    parser.add_argument("--font-bold", type=Path, default=Path("C:/Windows/Fonts/msyhbd.ttc"))
    args = parser.parse_args()
    for path in (args.font, args.font_bold):
        if not path.is_file():
            parser.error(f"CJK TrueType font not found: {path}; set --font and --font-bold")
    pdfmetrics.registerFont(TTFont("MCVS", str(args.font), subfontIndex=0))
    pdfmetrics.registerFont(TTFont("MCVS-Bold", str(args.font_bold), subfontIndex=0))
    pdfmetrics.registerFontFamily("MCVS", normal="MCVS", bold="MCVS-Bold", italic="MCVS", boldItalic="MCVS-Bold")
    course = load_course()
    (ROOT / "assets").mkdir(exist_ok=True)
    curriculum(course)
    roadmap(course, args.font, args.font_bold)
    guide(course)
    checkerboard()
    for name in ("curriculum.md", "assets/roadmap.png", "MCVS_learning_guide.pdf",
                 "assets/checkerboard_8x5_20mm.pdf"):
        print(ROOT / name)


if __name__ == "__main__":
    main()
