"""Typography and measured Fourier HUD for the contour motion scene.

Mathematical notation is typeset through TeX Live and Manim MathTex.
Spectrum columns are derived only from the coefficients passed by the caller.
"""
from __future__ import annotations

import numpy as np
from manim import (
    VGroup, Text, MathTex, Line, Rectangle, RoundedRectangle, Dot,
    LEFT, RIGHT, UP, DOWN, WHITE,
)

CYAN = "#65E8F5"
MAGENTA = "#F567CB"
MUTED = "#73929D"
GRID = "#14303A"
CN_FONT = "Microsoft YaHei"
MONO_FONT = "Consolas"


def _text(content, size=20, color=WHITE, font=MONO_FONT):
    return Text(content, font=font, font_size=size, color=color)


def make_math_stage() -> VGroup:
    """Quiet full-frame grid and labels surrounding a clear drawing area."""
    stage = VGroup()
    for x in np.arange(-7, 7.1, .5):
        stage.add(Line([x, -3.65, 0], [x, 3.65, 0],
                       stroke_color=GRID, stroke_width=.45,
                       stroke_opacity=.28 if x % 1 else .48))
    for y in np.arange(-3.5, 3.6, .5):
        stage.add(Line([-7, y, 0], [7, y, 0],
                       stroke_color=GRID, stroke_width=.45,
                       stroke_opacity=.28 if y % 1 else .48))

    title_cn = _text("鸡你太美", 25, font=CN_FONT).move_to([-5.52, 3.48, 0])
    title_en = _text("/ FOURIER MOTION", 22, CYAN).next_to(title_cn, RIGHT, buff=.25)
    title = VGroup(title_cn, title_en)
    stage.add(title)
    stage.add(_text("A CONTOUR IN COMPLEX SPACE", 12, MUTED).move_to([4.69, 3.48, 0]))
    stage.add(Line([-6.65, 3.12, 0], [6.65, 3.12, 0], stroke_color=CYAN,
                   stroke_width=.75, stroke_opacity=.36))
    # Tiny corner brackets frame the rendering area, without drawing a box.
    for x, direction in [(-2.65, 1), (6.55, -1)]:
        for y, vertical in [(2.86, -1), (-3.14, 1)]:
            stage.add(Line([x, y, 0], [x + direction * .2, y, 0],
                           stroke_color=MUTED, stroke_width=1, stroke_opacity=.6))
            stage.add(Line([x, y, 0], [x, y + vertical * .2, 0],
                           stroke_color=MUTED, stroke_width=1, stroke_opacity=.6))
    stage.add(_text("RECONSTRUCTION / COMPLEX PLANE", 12, MUTED)
              .move_to([1.65, -3.2, 0]))
    return stage


def make_formula_panel(n_terms: int = 96) -> VGroup:
    """A narrow left column explaining exactly the computed Fourier series."""
    panel = VGroup()
    border = RoundedRectangle(width=3.35, height=5.85, corner_radius=.12,
                              stroke_color=CYAN, stroke_width=.7,
                              stroke_opacity=.32, fill_color="#071218",
                              fill_opacity=.88).move_to([-4.91, -.08, 0])
    panel.add(border)

    def add_line(content, y, size=18, color=WHITE, font=MONO_FONT):
        label = _text(content, size, color, font)
        if label.width > 2.91:
            label.scale_to_fit_width(2.91)
        label.move_to([-6.36 + label.width / 2, y, 0])
        panel.add(label)
        return label

    def add_math(expression, y, height=.38, color=WHITE):
        label = MathTex(expression, color=color, font_size=30)
        label.scale_to_fit_height(height)
        if label.width > 2.91:
            label.scale_to_fit_width(2.91)
        label.move_to([-6.36 + label.width / 2, y, 0])
        panel.add(label)
        return label

    def add_mixed(caption, expression, y):
        caption_label = _text(caption, 21, WHITE, CN_FONT)
        math_label = MathTex(expression, color=WHITE, font_size=28)
        row = VGroup(caption_label, math_label).arrange(RIGHT, buff=.10)
        if row.width > 2.91:
            row.scale_to_fit_width(2.91)
        row.move_to([-6.36 + row.width / 2, y, 0])
        panel.add(row)
        return row

    add_line("01 / CONTOUR", 2.49, 15, CYAN)
    add_line("轮廓 → 复平面", 2.06, 21, WHITE, CN_FONT)
    add_math(r"z(t)=x(t)+i\,y(t)", 1.64, .35)
    panel.add(Line([-6.36, 1.29, 0], [-3.45, 1.29, 0],
                   stroke_color=MUTED, stroke_width=.65, stroke_opacity=.35))
    add_line("02 / FOURIER SERIES", 1.0, 15, CYAN)
    add_math(r"z_N(t)=\sum_{n\in K}c_n e^{2\pi i n t}", .54, .55)
    add_math(r"c_n=\int_0^1 z(s)e^{-2\pi i n s}\,ds", -.12, .50)
    add_math(r"t\in[0,1]", -.70, .27, MUTED)
    panel.add(Line([-6.36, -.99, 0], [-3.45, -.99, 0],
                   stroke_color=MUTED, stroke_width=.65, stroke_opacity=.35))
    add_line("03 / EPICYCLES", -1.27, 15, MAGENTA)
    add_mixed("圆半径", r"=|c_n|", -1.69)
    add_mixed("角速度", r"=2\pi n", -2.08)
    add_math(rf"n\in K,\quad |K|={n_terms}", -2.65, .25, MUTED)
    return panel


def make_spectrum(amplitudes) -> VGroup:
    """Create a small measured magnitude plot, located below the drawing.

    The plot uses the first up to 48 supplied magnitudes, normalized by their
    maximum for display. Input order is retained and values are not invented.
    Caller may move/scale the returned group to suit the scene.
    """
    values = np.abs(np.asarray(amplitudes).reshape(-1))[:48]
    if not np.all(np.isfinite(values)):
        raise ValueError("Spectrum magnitudes must be finite")
    spectrum = VGroup()
    spectrum.add(Line([-1.7, 0, 0], [1.7, 0, 0],
                      stroke_color=MUTED, stroke_width=.6, stroke_opacity=.5))
    maximum = float(values.max()) if len(values) else 0.0
    for j, value in enumerate(values):
        x = -1.66 + 3.32 * (j + .5) / len(values)
        height = .42 * float(value) / maximum if maximum else 0.0
        if height > 0:
            spectrum.add(Line([x, 0, 0], [x, height, 0],
                              stroke_color=CYAN if j % 2 == 0 else MAGENTA,
                              stroke_width=2, stroke_opacity=.75))
    magnitude = MathTex(r"|c_n|", font_size=15, color=MUTED)
    caption = _text("/ MEASURED SPECTRUM", 10, MUTED)
    spectrum.add(VGroup(magnitude, caption).arrange(RIGHT, buff=.08)
                 .move_to([0, -.16, 0]))
    return spectrum
