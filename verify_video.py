"""Inspect the rendered media and create a four-frame visual review sheet."""
import json
from pathlib import Path
import av
import numpy as np
from PIL import Image, ImageDraw


path = Path("media/videos/main/1080p30/BasketballDance.mp4")
targets = [0.5, 8.25, 14.25, 20.5]
frames = []
count = 0
with av.open(str(path)) as container:
    stream = container.streams.video[0]
    report = dict(width=stream.width, height=stream.height, fps=float(stream.average_rate),
                  duration=float(container.duration / av.time_base), video_codec=stream.codec_context.name,
                  audio_streams=len(container.streams.audio))
    for frame in container.decode(video=0):
        count += 1
        if len(frames) < len(targets) and frame.time >= targets[len(frames)]:
            frames.append(frame.to_image().resize((768,432)))
report['decoded_frames'] = count
with av.open(str(path)) as container:
    samples = [f.to_ndarray().astype(float) for f in container.decode(audio=0)]
report['audio_rms'] = float(np.sqrt(np.mean(np.concatenate([s.ravel() for s in samples])**2)))
assert report['width'] == 1920 and report['height'] == 1080
assert report['fps'] == 30 and count == 660
assert abs(report['duration']-22) < .1
assert report['audio_streams'] == 1 and report['audio_rms'] > .01
sheet = Image.new('RGB', (1536, 924), '#080C1C')
draw = ImageDraw.Draw(sheet)
for i,frame in enumerate(frames):
    x,y = (i%2)*768,(i//2)*462
    sheet.paste(frame,(x,y))
    draw.text((x+16,y+438), f'{targets[i]:.2f}s', fill='white')
sheet.save('media/review.png')
Path('media/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
