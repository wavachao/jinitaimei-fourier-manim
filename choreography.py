"""Basketball dance scenery and deterministic choreography, without text assets.

``make_stage()`` returns a back-to-front VGroup sized for Manim's default
14.22 by 8 frame. Keep a dancer around (0, -0.4), a title at y=2.9, and a
caption at y=-3.0. ``dance_phase(t)`` accepts seconds in a 20-second routine
at 120 BPM and returns pose labels and smoothly varying movement cues.
"""

from math import cos, pi, sin

import numpy as np
from manim import Arc, Circle, Dot, Line, Polygon, Rectangle, VGroup


def make_stage():
    """Return layered court scenery; no fonts, TeX, or external files needed."""
    stage = VGroup()
    stage.add(Rectangle(width=14.24, height=8.02, stroke_width=0,
                        fill_color="#080C1C", fill_opacity=1))

    # Broad, softly stepped overhead glows create depth with vector primitives.
    for radius, opacity in [(4.7, .025), (3.8, .035), (2.9, .045)]:
        stage.add(Circle(radius=radius, stroke_width=0, fill_color="#6254DF",
                         fill_opacity=opacity).move_to([0, 2.1, 0]))
    for sign, color in [(-1, "#6A60FF"), (1, "#28C7DC")]:
        stage.add(Polygon([sign * 5.6, 3.5, 0], [sign * 6.9, -2.2, 0],
                          [sign * 1.8, -2.2, 0], stroke_width=0,
                          fill_color=color, fill_opacity=.07))
        stage.add(Line([sign * 5.6, 3.5, 0], [sign * 5.6, 3.7, 0],
                       color=color, stroke_width=10, stroke_opacity=.65))

    # A perspective court leaves the lower caption band visually quiet.
    stage.add(Polygon([-7.12, -1.85, 0], [7.12, -1.85, 0],
                      [7.12, -4.01, 0], [-7.12, -4.01, 0],
                      stroke_width=0, fill_color="#10172A", fill_opacity=1))
    stage.add(Line([-7.1, -1.85, 0], [7.1, -1.85, 0],
                   stroke_color="#6B6BA7", stroke_width=1.5,
                   stroke_opacity=.4))
    stage.add(Polygon([-5.6, -2.05, 0], [5.6, -2.05, 0],
                      [6.9, -3.78, 0], [-6.9, -3.78, 0],
                      stroke_color="#6A7399", stroke_width=1.2,
                      stroke_opacity=.3, fill_opacity=0))
    # Broken end-court marks are confined to the outer edges, away from captions.
    for sign in [-1, 1]:
        stage.add(Line([sign * 4.35, -2.05, 0], [sign * 4.9, -3.78, 0],
                       stroke_color="#8A7FCB", stroke_width=1.2,
                       stroke_opacity=.3))
        stage.add(Arc(radius=.72, start_angle=-pi / 2, angle=pi,
                      stroke_color="#8A7FCB", stroke_width=1.2,
                      stroke_opacity=.3).stretch(.4, 0)
                  .move_to([sign * 5.75, -2.55, 0]))
    stage.add(Circle(radius=1.35, stroke_width=0, fill_color="#060811",
                     fill_opacity=.5).stretch(.13, 1).move_to([0, -2.04, 0]))

    # Reproducible sparse star dust; deliberately clear title and dancer areas.
    rng = np.random.default_rng(120)
    for _ in range(42):
        x = rng.uniform(-6.7, 6.7)
        y = rng.uniform(-1.3, 3.65)
        if abs(x) < 3.2:
            continue
        stage.add(Dot([x, y, 0], radius=rng.uniform(.012, .029),
                      color="#A5B5E5", fill_opacity=rng.uniform(.15, .5)))
    for sign in [-1, 1]:
        for i in range(5):
            stage.add(Rectangle(width=.045, height=.17 + .11 * i,
                                fill_color="#756CEE", fill_opacity=.45,
                                stroke_width=0)
                      .move_to([sign * (6.2 - i * .14), .15, 0]))
    return stage


def dance_phase(t):
    """Return repeatable movement cues for a 20-second, 120-BPM routine.

    Keys: ``beat`` (continuous count), ``phase`` (continuous radians),
    ``section`` (0..3), ``pose`` (string),
    ``body_sway`` / ``bounce`` (scene units), ``lean`` / ``arm_swing``
    (radians), ``ball_position`` (absolute xyz ndarray), ``ball_rotation``
    (radians). Ball positions assume the dancer's feet are near y=-2.5.
    All numbers are analytic: callers can sample any timestamp independently.
    """
    t = float(np.clip(t, 0, 20))
    beat = 2 * t
    rhythm = 2 * pi * beat
    if t < 4:
        section, pose = 0, "idle"
        sway = .12 * sin(rhythm / 2)
        lean = .07 * sin(rhythm / 2)
        ball_x = 1.05 + sway
        ball_y = -.9 + .12 * sin(rhythm / 2)
    elif t < 10:
        section, pose = 1, "dribble"
        sway = .2 * sin(rhythm / 2)
        lean = -.09 + .04 * cos(rhythm)
        ball_x = 1.12 + sway
        ball_y = -2.15 + 1.55 * abs(cos(rhythm / 2))
    elif t < 16:
        section, pose = 2, "dance"
        sway = .31 * sin(rhythm / 2)
        lean = .16 * sin(rhythm / 2)
        ball_x = 1.02 + .22 * sin(rhythm / 2)
        ball_y = -.88 + .19 * sin(rhythm)
    else:
        section, pose = 3, "finale"
        # Ease into a clean held finishing pose during the last two seconds.
        fade = max(0., min(1., (18.5 - t) / 2.5))
        sway = .24 * sin(rhythm / 2) * fade
        lean = .11 * sin(rhythm / 2) * fade
        ball_x = 1.15 + .12 * sin(rhythm / 2) * fade
        ball_y = -.75 + .13 * cos(rhythm) * fade
    return dict(beat=beat, phase=rhythm / 2, section=section, pose=pose, body_sway=sway,
                bounce=.075 * (1 - cos(rhythm)), lean=lean,
                arm_swing=.25 * sin(rhythm / 2),
                ball_position=np.array([ball_x, ball_y, 0.]),
                ball_rotation=-2 * pi * t)
