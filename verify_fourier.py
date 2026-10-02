"""Check delivered video, Fourier geometry, and periodic continuity."""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image, ImageDraw
from contour_data import load_contour, deform, reconstruction_error

path = Path('media/videos/fourier_scene/1080p30/FourierDance.mp4')
targets = [6., 11., 16.3, 21.5]
frames=[]
count=0
with av.open(str(path)) as container:
    stream=container.streams.video[0]
    report=dict(width=stream.width,height=stream.height,fps=float(stream.average_rate),
                duration=container.duration/av.time_base,codec=stream.codec_context.name,
                audio_streams=len(container.streams.audio))
    for frame in container.decode(video=0):
        count+=1
        if len(frames)<len(targets) and frame.time>=targets[len(frames)]:
            frames.append(frame.to_image().resize((960,540)))
report['frames']=count
with av.open(str(path)) as container:
    sound=np.concatenate([f.to_ndarray().ravel() for f in container.decode(audio=0)])
report['audio_rms']=float(np.sqrt(np.mean(sound.astype(float)**2)))
report['fourier']=reconstruction_error(96)
z=load_contour()
report['loop_closure_error']=float(np.max(np.abs(deform(z,0)-deform(z,2))))
assert (report['width'],report['height'],report['fps'],count)==(1920,1080,30.,780)
assert abs(report['duration']-26)<.1
assert report['audio_streams']==1 and report['audio_rms']>.01
assert report['loop_closure_error']<1e-12
assert report['fourier']['max']<.04
sheet=Image.new('RGB',(1920,1140),'#030609')
draw=ImageDraw.Draw(sheet)
for i,frame in enumerate(frames):
    x,y=(i%2)*960,(i//2)*570
    sheet.paste(frame,(x,y))
    draw.text((x+20,y+548),f'{targets[i]:.2f}s',fill='white')
sheet.save('media/fourier_review.png')
frames[-1].save('media/fourier_poster.png')
Path('media/fourier_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
