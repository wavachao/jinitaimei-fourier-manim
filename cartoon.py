"""Vector-only cartoon dancer and basketball, with no font/TeX dependencies."""

from manim import *
import numpy as np


def _point(x, y):
    return np.array([x, y, 0.0])


def _stroke(points, color, width=12):
    return VMobject().set_points_as_corners(points).set_stroke(
        color, width=width, joint_type=LineJointType.ROUND
    )


def make_basketball(radius=0.32):
    """Return an orange basketball centred at the origin."""
    ball = Circle(radius, stroke_color="#502C27", stroke_width=2.2,
                  fill_color="#EE8838", fill_opacity=1)
    shade = Circle(radius * 0.77, stroke_width=0, fill_color="#FFAC50",
                   fill_opacity=0.65).shift(UP * radius * 0.12 + LEFT * radius * 0.09)
    horizontal = Line(LEFT * radius, RIGHT * radius, color="#63392C", stroke_width=2)
    vertical = Line(DOWN * radius, UP * radius, color="#63392C", stroke_width=2)
    seam_l = CubicBezier(_point(-radius * 0.58, radius * 0.81),
                         _point(radius * 0.05, radius * 0.35),
                         _point(radius * 0.05, -radius * 0.35),
                         _point(-radius * 0.58, -radius * 0.81),
                         stroke_color="#63392C", stroke_width=2)
    seam_r = seam_l.copy().flip(UP)
    highlight = Arc(radius=radius * 0.82, start_angle=0.65, angle=0.72,
                    stroke_color="#FFD599", stroke_width=3)
    return VGroup(ball, shade, horizontal, vertical, seam_l, seam_r, highlight)


def make_dancer(pose="idle", phase=0.0):
    """Return a stylized silver-haired dancer, about 4.3 units tall.

    phase is an angle in radians; rebuild at successive phases to animate.
    Poses supported: idle, dribble, dance, finale.
    """
    skin, skin_shadow = "#F2C9B0", "#DDA38C"
    ink, denim, seam = "#182033", "#27324A", "#64748C"
    beat = float(np.sin(phase))
    energy = 1.0 if pose in ("dance", "finale") else 0.3
    sway = 0.12 * energy * beat
    bounce = 0.055 * energy * np.cos(2 * phase)
    shoulder_l = _point(-0.47 + sway, 0.45 + bounce)
    shoulder_r = _point(0.47 + sway, 0.45 + bounce)
    hip_l, hip_r = _point(-0.24, -0.58), _point(0.24, -0.58)
    if pose == "dance":
        elbow_l = _point(-0.84 + sway, 0.08 + 0.28 * beat)
        hand_l = _point(-0.48 + sway, 0.37 + 0.38 * beat)
        elbow_r = _point(0.82 + sway, 0.15 - 0.28 * beat)
        hand_r = _point(0.48 + sway, 0.48 - 0.38 * beat)
        knee_l = _point(-0.29 - 0.16 * beat, -1.19)
        knee_r = _point(0.30 - 0.10 * beat, -1.18)
    elif pose == "dribble":
        elbow_l, hand_l = _point(-0.75, 0.06), _point(-0.55, -0.37)
        elbow_r = _point(0.88, 0.07)
        hand_r = _point(1.02, -0.25 + 0.26 * beat)
        knee_l, knee_r = _point(-0.39, -1.16), _point(0.45, -1.18)
    elif pose == "finale":
        elbow_l, hand_l = _point(-0.91, 0.80), _point(-1.12, 1.35)
        elbow_r, hand_r = _point(0.91, 0.80), _point(1.12, 1.35)
        knee_l, knee_r = _point(-0.33, -1.19), _point(0.33, -1.19)
    else:
        elbow_l, hand_l = _point(-0.67, -0.06), _point(-0.66, -0.55)
        elbow_r, hand_r = _point(0.67, -0.06), _point(0.66, -0.55)
        knee_l, knee_r = _point(-0.26, -1.19), _point(0.27, -1.19)

    ankle_l, ankle_r = _point(-0.36, -1.75), _point(0.38, -1.75)
    legs = VGroup()
    for hip, knee, ankle in [(hip_l, knee_l, ankle_l), (hip_r, knee_r, ankle_r)]:
        legs.add(_stroke([hip, knee, ankle], ink, 23))
        legs.add(_stroke([hip + RIGHT * 0.045, knee + RIGHT * 0.045,
                          ankle + RIGHT * 0.045], denim, 12))
        shoe = RoundedRectangle(width=0.52, height=0.23, corner_radius=0.09,
                                stroke_color=ink, stroke_width=2,
                                fill_color="#F7F3EE", fill_opacity=1)
        shoe.move_to(ankle + _point(-0.04 if ankle[0] < 0 else 0.04, -0.11))
        sole = Line(shoe.get_left() + DOWN * 0.06, shoe.get_right() + DOWN * 0.06,
                    color="#AFB6C5", stroke_width=2)
        legs.add(shoe, sole)

    arms = VGroup()
    for shoulder, elbow, hand in [(shoulder_l, elbow_l, hand_l),
                                 (shoulder_r, elbow_r, hand_r)]:
        sleeve_end = shoulder + (elbow - shoulder) * 0.43
        arms.add(_stroke([shoulder, elbow, hand], skin_shadow, 17))
        arms.add(_stroke([shoulder, elbow, hand], skin, 13))
        arms.add(_stroke([shoulder, sleeve_end], "#D9DFE6", 22))
        arms.add(Circle(radius=0.11, stroke_color=skin_shadow, stroke_width=1.5,
                        fill_color=skin, fill_opacity=1).move_to(hand))

    torso = RoundedRectangle(width=1.05, height=1.15, corner_radius=0.22,
                             stroke_color="#A9B3C4", stroke_width=2,
                             fill_color="#E7EBF1", fill_opacity=1)
    torso.move_to(_point(sway, -0.02 + bounce))
    bib = RoundedRectangle(width=0.78, height=0.81, corner_radius=0.12,
                           stroke_color=ink, stroke_width=2,
                           fill_color=denim, fill_opacity=1)
    bib.move_to(_point(sway, -0.24 + bounce))
    straps = VGroup()
    for x in [-0.31, 0.31]:
        strap = Line(_point(x + sway, 0.54 + bounce),
                     _point(x + sway, -0.13 + bounce), color=ink, stroke_width=9)
        button = Circle(0.037, stroke_width=0, fill_color="#D8C8A5", fill_opacity=1)
        button.move_to(_point(x + sway, 0.01 + bounce))
        straps.add(strap, button)
    pocket = RoundedRectangle(width=0.36, height=0.24, corner_radius=0.045,
                              stroke_color=seam, stroke_width=1.3,
                              fill_color=ink, fill_opacity=0.4)
    pocket.move_to(_point(sway, -0.30 + bounce))
    neck = RoundedRectangle(width=0.27, height=0.30, corner_radius=0.09,
                            stroke_width=0, fill_color=skin_shadow, fill_opacity=1)
    neck.move_to(_point(sway, 0.63 + bounce))
    collar = Arc(radius=0.19, start_angle=PI, angle=PI,
                 stroke_color="#ADB7C7", stroke_width=3).move_to(_point(sway, 0.50 + bounce))

    head = VGroup()
    for x in [-0.52, 0.52]:
        head.add(Ellipse(width=0.20, height=0.31, stroke_color=skin_shadow,
                         stroke_width=1.5, fill_color=skin, fill_opacity=1)
                 .move_to(_point(x, 1.27)))
    face = Ellipse(width=1.03, height=1.24, stroke_color=skin_shadow,
                   stroke_width=2, fill_color=skin, fill_opacity=1).move_to(_point(0, 1.34))
    head.add(face)
    for x in [-0.25, 0.25]:
        head.add(Ellipse(width=0.14, height=0.075, stroke_width=0,
                         fill_color="#EFA897", fill_opacity=0.6).move_to(_point(x * 1.5, 1.16)))
        head.add(Line(_point(x - 0.10, 1.48), _point(x + 0.075, 1.49),
                      stroke_color="#5F5862", stroke_width=2.4))
        eye = Ellipse(width=0.085, height=0.13, stroke_width=0,
                      fill_color=ink, fill_opacity=1).move_to(_point(x, 1.36))
        head.add(eye, Dot(_point(x - 0.012, 1.39), radius=0.018, color=WHITE))
    head.add(Arc(radius=0.15, start_angle=PI * 1.15, angle=PI * 0.7,
                 stroke_color="#9E655C", stroke_width=2.2).move_to(_point(0, 1.07)))
    head.add(Line(_point(0.01, 1.28), _point(-0.015, 1.21),
                  stroke_color=skin_shadow, stroke_width=1.5))
    hair_back = Ellipse(width=1.16, height=0.79, stroke_color="#69727F",
                        stroke_width=2, fill_color="#8C96A5", fill_opacity=1)
    hair_back.move_to(_point(0, 1.80))
    # Separate swept locks leave a clear middle part above the forehead.
    hair_l = VMobject(stroke_color="#69727F", stroke_width=1.6,
                      fill_color="#C1CBD5", fill_opacity=1)
    hair_l.set_points_smoothly([_point(-0.02, 2.08), _point(-0.37, 2.06),
                               _point(-0.58, 1.82), _point(-0.50, 1.46),
                               _point(-0.28, 1.69), _point(-0.02, 1.92),
                               _point(-0.02, 2.08)])
    hair_r = hair_l.copy().flip(UP).set_fill("#AAB5C3")
    hair_lines = VGroup()
    for side in [-1, 1]:
        for offset in [0.0, 0.10, 0.20]:
            hair_lines.add(CubicBezier(_point(side * (0.07 + offset), 2.04 - offset * 0.2),
                                      _point(side * 0.30, 1.98 - offset),
                                      _point(side * 0.43, 1.83 - offset),
                                      _point(side * (0.46 - offset * 0.2), 1.69 - offset * 0.5),
                                      stroke_color="#E6EDF2", stroke_width=1.8,
                                      stroke_opacity=0.65))
    head.add(hair_back, hair_l, hair_r, hair_lines)
    head.shift(_point(sway * 1.2, bounce))
    return VGroup(legs, arms, neck, torso, bib, straps, pocket, collar, head)
