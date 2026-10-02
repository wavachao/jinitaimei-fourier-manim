"""Render with: uv run manim -qh main.py BasketballDance"""
from manim import *
import numpy as np
from cartoon import make_dancer, make_basketball
from choreography import make_stage, dance_phase
from make_audio import create_beat

FONT = "Microsoft YaHei"


def label(text, size=32, color=WHITE):
    return Text(text, font=FONT, font_size=size, color=color)


def make_chicken():
    body = Ellipse(width=.85, height=.95, fill_color="#FFF3D6", fill_opacity=1, stroke_width=0)
    head = Circle(.31, fill_color="#FFF3D6", fill_opacity=1, stroke_width=0).move_to([.18,.46,0])
    comb = VGroup(*[Circle(.09, fill_color="#FF5F72", fill_opacity=1, stroke_width=0).move_to([x,.76,0]) for x in (.02,.16,.3)])
    beak = Triangle(fill_color="#FFB547", fill_opacity=1, stroke_width=0).scale(.12).rotate(-PI/2).move_to([.51,.43,0])
    eye = Dot([.28,.52,0], radius=.035, color="#101327")
    wing = Arc(radius=.27, start_angle=PI/2, angle=PI, color="#E7BF79").shift([.05,-.02,0])
    legs = VGroup(*[Line([x,-.4,0],[x,-.66,0], color="#FFB547", stroke_width=4) for x in (-.18,.18)])
    return VGroup(body,head,comb,beak,eye,wing,legs)


class BasketballDance(Scene):
    def construct(self):
        self.add(make_stage())
        time = ValueTracker(0)
        self.add_sound(create_beat())
        title = label("鸡 你 太 美", 58).move_to([0,2.9,0])
        title.set_color_by_gradient("#F8FAFF", "#ACB8FF")
        eyebrow = label("蔡徐坤 · 篮球舞梗", 20, "#A3ADC9").move_to([0,3.62,0])
        underline = Line([-1.6,2.4,0],[1.6,2.4,0], color="#FFB547", stroke_width=3)
        self.add(eyebrow, title, underline)

        def parameters():
            return dance_phase(max(0,time.get_value()-2))

        def actor_frame():
            p = parameters()
            dancer = make_dancer(pose=p['pose'], phase=p['phase'])
            dancer.rotate(p.get('lean',0)*.3)
            dancer.shift([p.get('body_sway',0),-.35+p.get('bounce',0),0])
            return dancer

        actor = always_redraw(actor_frame)
        def ball_frame():
            p = parameters()
            ball = make_basketball(.3)
            ball.rotate(p.get('ball_rotation',0))
            ball.move_to(p['ball_position'])
            return ball
        ball = always_redraw(ball_frame)
        self.add(actor,ball)

        # Rhythm indicator creates an easily readable visual beat.
        dots = VGroup(*[Dot(radius=.045, color="#637091").move_to([x,-3.68,0]) for x in np.linspace(-.55,.55,8)])
        dots.add_updater(lambda group: [d.set_color("#FFB547" if i == int(time.get_value()*2)%8 else "#637091") for i,d in enumerate(group)])
        self.add(dots)
        caption = label("全民制作人们，准备好了吗？", 29, "#DCE3FA").move_to([0,-3.08,0])
        self.add(caption)
        self.play(time.animate.set_value(2), run_time=2, rate_func=linear)

        def segment(text, end):
            nonlocal caption
            replacement = label(text, 29, "#DCE3FA").move_to([0,-3.08,0])
            duration = end-time.get_value()
            self.play(Succession(Transform(caption,replacement, run_time=.25), Wait(duration-.25)), time.animate.set_value(end), run_time=duration, rate_func=linear)

        segment("练习时长：两年半", 6)
        segment("唱 · 跳 · 篮球", 12)
        left = label("鸡", 76, "#FFB547").move_to([-4.15,.8,0])
        right = label("你太美", 48, "#B9ADFF").move_to([4.1,.8,0])
        self.add(left,right)
        segment("肩膀一抖，节奏就有", 18)
        chicken = make_chicken().move_to([-4.1,-1.25,0])
        self.add(chicken)
        chicken.add_updater(lambda m: m.move_to([-4.1,-1.25+.12*np.sin(TAU*2*time.get_value()),0]))
        segment("鸡你太美！", 21)
        actor.clear_updaters()
        ball.clear_updaters()
        chicken.clear_updaters()
        dots.clear_updaters()
        self.play(time.animate.set_value(22), Flash(ball.get_center(), color="#FFB547", flash_radius=.55), run_time=1, rate_func=linear)
