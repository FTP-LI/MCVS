# 重建学习材料

学习本身不需要运行本目录。维护教材时才安装 [requirements.txt](requirements.txt)，然后从任意目录运行：

```powershell
python doc/learning/tools/build_materials.py
```

上面相对路径的命令应在项目根目录执行；也可将脚本替换为绝对路径。输入为 `doc/learning/course.json`，输出固定为：

- `doc/learning/curriculum.md`
- `doc/learning/assets/roadmap.png`
- `doc/learning/MCVS_learning_guide.pdf`
- `doc/learning/assets/checkerboard_8x5_20mm.pdf`

不会读取或覆盖学习者的 `progress.md`、个人实验记录和报告。更新课程后，应同时检查文字说明是否一致。

默认使用 Windows 微软雅黑字体。其他系统可以用 `--font` 和 `--font-bold` 指向支持中文的 TrueType 字体（TTF，或有 TrueType 轮廓的 TTC；不保证支持 CFF 轮廓）。示例：

```text
python build_materials.py --font /path/to/cjk.ttf --font-bold /path/to/cjk-bold.ttf
```

生成后检查 PDF 页数和中文文本，再用 Poppler 渲染所有页面进行视觉检查。棋盘采用矢量绘制，A4 纵向、9×6 个 20 mm 方格、8×5 内角点；打印后的实际尺寸仍需测量，屏幕显示比例不能代替打印校验。
