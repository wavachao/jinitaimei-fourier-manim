"""Generate an original 120 BPM instrumental groove (no sampled music)."""
from pathlib import Path
import wave
import numpy as np


def create_beat(path="media/original_beat.wav", duration=22):
    sr = 44100
    audio = np.zeros(int(sr * duration))
    rng = np.random.default_rng(42)

    def add(start, sound, gain=1):
        index = int(start * sr)
        end = min(index + len(sound), len(audio))
        if end > index:
            audio[index:end] += sound[:end-index] * gain

    for n in range(int(duration * 2)):
        start = n / 2
        t = np.arange(int(sr * .27)) / sr
        kick = np.sin(2*np.pi*(48*t + 9*(1-np.exp(-22*t)))) * np.exp(-17*t)
        add(start, kick, .52)
        if n % 2:
            t = np.arange(int(sr*.16))/sr
            snare = rng.normal(size=len(t))*np.exp(-28*t)
            add(start, snare, .16)
        for offset in (0, .25):
            t = np.arange(int(sr*.055))/sr
            noise = rng.normal(size=len(t))
            noise = np.diff(noise, prepend=0)
            add(start+offset, noise*np.exp(-80*t), .045)
        # Original bass sequence and short pentatonic accent.
        freq = [65.406, 65.406, 77.782, 87.307, 65.406, 98., 87.307, 77.782][n % 8]
        t = np.arange(int(sr*.36))/sr
        env = (1-np.exp(-100*t))*np.exp(-8*t)
        add(start, (np.sin(2*np.pi*freq*t)+.25*np.sin(4*np.pi*freq*t))*env, .22)
        if n % 2 == 0:
            freq = [261.63, 311.13, 349.23, 392.][(n//2) % 4]
            t = np.arange(int(sr*.22))/sr
            add(start+.125, np.sin(2*np.pi*freq*t)*np.exp(-19*t), .11)
    fade = np.minimum(np.arange(len(audio))/sr/.25, 1)
    fade *= np.minimum((len(audio)-np.arange(len(audio)))/sr/.7, 1)
    audio *= fade
    audio = np.tanh(audio*1.25)*.85
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((audio*32767).astype('<i2').tobytes())
    return str(path)


if __name__ == '__main__':
    print(create_beat())
