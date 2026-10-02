"""Reference-based neon contour drawn by actual complex Fourier vectors."""
from functools import lru_cache
import numpy as np
from manim import *
from contour_data import load_contour, deform
from math_hud import make_math_stage, make_formula_panel, make_spectrum
from make_audio import create_beat


class FourierDance(Scene):
    def construct(self):
        self.camera.background_color = '#030609'
        base = load_contour()
        n = len(base)
        all_freq = np.fft.fftfreq(n, d=1/n).astype(int)
        initial = np.fft.fft(base)/n
        indices = np.argsort(np.abs(initial))[::-1][:96]
        freq = all_freq[indices]
        u = np.linspace(0, 1, 1201)
        basis = np.exp(TAU*1j*freq[:,None]*u[None,:])
        origin = np.array([1.4, -.05, 0.])
        progress = ValueTracker(0)
        motion = ValueTracker(0)
        mode = {'dance':False}

        def point(z):
            return origin + np.array([z.real,z.imag,0.])

        @lru_cache(maxsize=2)
        def snapshot(p,m):
            contour = deform(base,m) if mode['dance'] else base
            coef = (np.fft.fft(contour)/n)[indices]
            vectors = coef*np.exp(TAU*1j*freq*p)
            chain = np.concatenate(([0j],np.cumsum(vectors)))
            curve = np.sum(coef[:,None]*basis,axis=0)
            return coef,chain,curve

        def data():
            return snapshot(float(progress.get_value()),float(motion.get_value()))

        self.add(make_math_stage())
        self.add_sound(create_beat('media/fourier_beat.wav', duration=26))
        panel = make_formula_panel(n_terms=96).set_z_index(10)
        spectrum = make_spectrum(np.abs(initial[indices])).scale(.88).move_to([-4.91,-3.43,0]).set_z_index(11)
        self.add(panel,spectrum)
        status = Text('01 / CONTOUR SAMPLING', font='Consolas',font_size=17,color='#7BDAD9').move_to([-4.9,-2.88,0]).set_z_index(12)
        self.add(status)

        def wheels_frame():
            coef,chain,_ = data()
            group = VGroup()
            for k,c in enumerate(coef):
                r = abs(c)
                a,b = point(chain[k]),point(chain[k+1])
                if r > .025:
                    color = '#54CDD2' if k%2 == 0 else '#8E85BD'
                    wheel = Circle(radius=r, stroke_color=color, stroke_width=.9, stroke_opacity=.38).move_to(a)
                    group.add(wheel)
                    if k < 5:
                        for j in range(12):
                            angle=TAU*j/12
                            v=np.array([np.cos(angle),np.sin(angle),0])
                            group.add(Line(a+v*r*.96,a+v*r,color=color,stroke_width=.7,stroke_opacity=.4))
                group.add(Line(a,b,stroke_color='#BDEAE7',stroke_width=1.3 if k<12 else .7,stroke_opacity=.65 if k<12 else .24))
            return group

        wheels = always_redraw(wheels_frame)

        def curve_frame():
            _,_,curve = data()
            end = len(curve) if mode['dance'] else max(2,int(progress.get_value()*1200)+1)
            pts = np.array([point(z) for z in curve[:end]])
            result=VGroup()
            for width,opacity in [(15,.035),(8,.12),(3,.95)]:
                result.add(VMobject(stroke_color='#FF53D1',stroke_width=width,stroke_opacity=opacity).set_points_as_corners(pts))
            return result

        trace = always_redraw(curve_frame)
        tip = always_redraw(lambda: VGroup(Dot(point(data()[1][-1]), radius=.10,color='#FFFFFF',fill_opacity=.12),Dot(point(data()[1][-1]),radius=.035,color='#FFFFFF')))
        self.add(wheels,trace,tip)
        coords = DecimalNumber(0,num_decimal_places=3,font_size=20,mob_class=MathTex,color='#FF70D9').move_to([-4.9,-2.4,0]).set_z_index(12)
        coords.add_updater(lambda m: m.set_value(progress.get_value()%1).set_color('#FF70D9').set_z_index(12))
        self.add(coords)
        self.add(MathTex('t =',font_size=20,color='#7BDAD9').move_to([-5.48,-2.4,0]).set_z_index(12))
        caption = Text('从一个舞姿，到一条闭合曲线',font='Microsoft YaHei',font_size=23,color='#99AEB9').move_to([1.4,-3.58,0]).set_z_index(12)
        self.add(caption)
        self.wait(2)
        new_status=Text('02 / FOURIER SYNTHESIS',font='Consolas',font_size=17,color='#7BDAD9').move_to(status).set_z_index(12)
        self.play(FadeTransform(status,new_status),run_time=.5)
        status=new_status
        self.play(progress.animate.set_value(1),run_time=13.5,rate_func=linear)
        # The same coefficients drive both the moving endpoint and the contour.
        mode['dance']=True
        snapshot.cache_clear()
        next_caption=Text('周期形变 · 旋转向量 · 经典律动',font='Microsoft YaHei',font_size=23,color='#99AEB9').move_to(caption).set_z_index(12)
        next_status=Text('03 / PERIODIC MOTION',font='Consolas',font_size=17,color='#7BDAD9').move_to(status).set_z_index(12)
        self.play(FadeTransform(caption,next_caption),FadeTransform(status,next_status),motion.animate.set_value(.5),progress.animate.set_value(1.0625),run_time=.5,rate_func=linear)
        caption=next_caption
        status=next_status
        self.play(motion.animate.set_value(8),progress.animate.set_value(2),run_time=7.5,rate_func=linear)
        for obj in (wheels,trace,tip,coords):
            obj.clear_updaters()
        final_caption=Text('鸡你太美  /  THE BEAUTY OF MATHEMATICS',font='Microsoft YaHei',font_size=21,color='#D5E7EC').move_to(caption).set_z_index(12)
        self.play(FadeTransform(caption,final_caption),wheels.animate.set_stroke(opacity=.10),FadeOut(tip),run_time=.7)
        self.wait(1.3)
