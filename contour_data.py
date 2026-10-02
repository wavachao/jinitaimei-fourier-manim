"""Mathematical silhouette, Fourier coefficients, and periodic pose deformation."""
from __future__ import annotations

from pathlib import Path
import numpy as np

DATA_PATH = Path(__file__).resolve().parent / "assets" / "pose_contour.npy"


def load_contour() -> np.ndarray:
    """Return 2048 equal-arc-length complex points; bbox centered, height 6.1."""
    return np.load(DATA_PATH).copy()


def fourier_terms(n: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """Return frequency integers and coefficients, in descending amplitude.

    Includes DC when selected: bounding-box centering is visually preferable
    for this pose and does not imply a zero centroid. Keeping DC makes the
    displayed complex sum reconstruct the precise supplied coordinates.
    """
    z = load_contour()
    coefficients = np.fft.fft(z) / len(z)
    frequencies = np.rint(np.fft.fftfreq(len(z)) * len(z)).astype(int)
    chosen = np.argsort(np.abs(coefficients))[::-1][:n]
    return frequencies[chosen], coefficients[chosen]


def evaluate(t: float | np.ndarray, freq: np.ndarray, coeff: np.ndarray) -> np.ndarray:
    """Evaluate sum c_k exp(2 pi i k t), where one circuit is t in [0,1]."""
    phase = np.exp(2j * np.pi * np.asarray(t)[..., None] * freq)
    return np.sum(phase * coeff, axis=-1)


def deform(z: np.ndarray, t: float) -> np.ndarray:
    """A two-second shoulder/hip dance loop; t is elapsed time in seconds.

    The feet stay planted while the upper torso leans and shoulders twist.
    Smooth spatial weights preserve a continuous closed Fourier contour;
    t=0,2,4,... exactly reproduce the reference pose.
    """
    x, y = z.real, z.imag
    phase = np.pi * t
    shoulder = np.exp(-((y - 1.45) / 1.20) ** 2)
    hip = np.exp(-((y + .50) / .70) ** 2)
    planted = np.clip((y + 3.00) / 1.20, 0, 1)
    planted = planted * planted * (3 - 2 * planted)
    sway = np.sin(phase)
    twist = np.sin(2 * phase)
    dx = planted * (.16 * sway * shoulder + .065 * twist * hip)
    # A small shoulder compression emphasizes the recognizable body turn.
    dx += .055 * twist * x * shoulder * planted
    dy = planted * (-.045 * np.sin(phase) ** 2 * shoulder + .035 * twist * x * shoulder)
    return z + dx + 1j * dy


def reconstruction_error(n: int = 96) -> dict[str, float]:
    """Report RMS/max geometric deviation in scene units."""
    z = load_contour()
    freq, coeff = fourier_terms(n)
    error = np.abs(evaluate(np.arange(len(z)) / len(z), freq, coeff) - z)
    return {"terms": n, "rms": float(np.sqrt(np.mean(error ** 2))),
            "max": float(error.max()), "height": float(np.ptp(z.imag))}


if __name__ == "__main__":
    import json
    print(json.dumps(reconstruction_error(), indent=2))
