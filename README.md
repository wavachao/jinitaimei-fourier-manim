# 鸡你太美 · Manim 篮球舞梗

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
