"""Typography and measured Fourier HUD for the contour motion scene.

Everything is built from ordinary Manim Text/geometry; no TeX runtime is needed.
Spectrum columns are derived only from the coefficients passed by the caller.
"""
from __future__ import annotations

import numpy as np
from manim import (
    VGroup, Text, Line, Rectangle, RoundedRectangle, Dot,
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


def make_formula_panel(n_terms: int = 100) -> VGroup:
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

    add_line("01 / CONTOUR", 2.49, 15, CYAN)
    add_line("轮廓 → 复平面", 2.06, 21, WHITE, CN_FONT)
    add_line("z(t) = x(t) + i y(t)", 1.64, 19)
    panel.add(Line([-6.36, 1.29, 0], [-3.45, 1.29, 0],
                   stroke_color=MUTED, stroke_width=.65, stroke_opacity=.35))
    add_line("02 / FOURIER SERIES", 1.0, 15, CYAN)
    add_line("z(t) = Σ cₙ exp(i 2πnt)", .57, 21)
    add_line("cₙ = ∫₀¹ z(s)", .1, 23)
    add_line("     exp(−i 2πns) ds", -.26, 21)
    add_line("t ∈ [0, 1]", -.7, 17, MUTED)
    panel.add(Line([-6.36, -.99, 0], [-3.45, -.99, 0],
                   stroke_color=MUTED, stroke_width=.65, stroke_opacity=.35))
    add_line("03 / EPICYCLES", -1.27, 15, MAGENTA)
    add_line("圆半径 = |cₙ|", -1.69, 21, WHITE, CN_FONT)
    add_line("角速度 = 2πn", -2.08, 21, WHITE, CN_FONT)
    add_line(f"{n_terms:03d} TERMS / FFT", -2.66, 15, MUTED)
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
    spectrum.add(_text("|cₙ| / MEASURED SPECTRUM", 10, MUTED)
                 .move_to([0, -.16, 0]))
    return spectrum
