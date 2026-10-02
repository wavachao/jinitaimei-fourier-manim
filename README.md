# 鸡你太美 · Manim 篮球舞梗

## 数学轮廓版（最新）

以参考图经典舞姿为轮廓，2048 个等弧长采样点通过 FFT 计算系数，按幅值保留 96 项。每个旋转向量对应一个复数指数项，圆半径为系数模长；末端与荧光曲线使用相同系数计算。13.5 秒逐笔绘制后，进行 8 秒周期肩胯形变。黑底青色网格、洋红轮廓及实时旋转圆轮，配原创节奏。

```powershell
uv sync --locked
uv run manim -qh --fps 30 --disable_caching fourier_scene.py FourierDance
uv run python verify_fourier.py
```

新成片：`media/videos/fourier_scene/1080p30/FourierDance.mp4`（26 秒、1080p30）。

`extract_contour.py` 以参考图人工审定中心线关键点为基础，局部洋红像素质心校准后进行周期插值与等弧长采样。`contour_data.py` 提供曲线、系数、重建误差和两秒周期形变。轮廓数据已保存在 `assets/pose_contour.npy`，正常渲染无需原图片。两秒形变是依据参考姿态制作的数学动画，并非从真人视频逐帧提取。

轮廓与数学界面由 subagent 在 `.worktrees/fourier-contour`、`.worktrees/math-hud` 独立制作并提交，再由主代理合并、渲染、验收。新计划见 `PLAN_FOURIER.md`。

## 初版卡通动画

22 秒卡通动画，1920×1080、30 fps，包含银灰中分、背带裤、运球、肩部舞蹈与小鸡彩蛋。配乐为程序合成的原创 120 BPM 节奏，无原歌曲录音。

## 运行

Windows，Python 3.12，安装 uv 后：

```powershell
uv sync --locked
uv run manim -qh --fps 30 --disable_caching main.py BasketballDance
```

输出：`media/videos/main/1080p30/BasketballDance.mp4`。

中文字体使用 Microsoft YaHei（Windows 自带），不需要 LaTeX。

## 文件

- `PLAN.md`：执行前的制作计划。
- `main.py`：22 秒完整场景与字幕。
- `cartoon.py`：矢量人物、篮球。
- `choreography.py`：舞台、连续动作参数。
- `make_audio.py`：原创音轨生成器。
- `uv.lock`：可复现依赖版本。

## 并行制作

人物与舞台分别由两个 subagent 在 `.worktrees/character` 和 `.worktrees/choreography` 中制作，各自使用 `feat/character`、`feat/choreography` 分支提交，随后合并到主分支。导出媒体与环境缓存不进入 Git。
