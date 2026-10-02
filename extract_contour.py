"""Reproduce a closed, single-line silhouette from the supplied pose image.

The landmarks follow the *centre* of the magenta stroke, including the folded
arm. They are calibrated in normalized image coordinates, snapped to the local
magenta stroke centroid, interpolated periodically, and resampled by arc length.
This deliberately avoids tracing both edges of the thick raster stroke.
Usage: python extract_contour.py INPUT_IMAGE [--output assets/pose_contour.npy]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.interpolate import CubicSpline

# Pixel landmarks for the 614 x 710 reference, listed along the pink centreline.
# The narrow arm fold is a real part of the closed path, not a separate contour.
REFERENCE_SIZE = np.array([614.0, 710.0])
LANDMARKS = np.array([
    [291, 81], [291, 53], [304, 28], [326, 18], [347, 21],
    [378, 33], [390, 49], [394, 66], [390, 81], [379, 79],
    [368, 102], [359, 130], [365, 146], [381, 170], [386, 194],
    [388, 211], [399, 239], [398, 264], [394, 292], [387, 306],
    [365, 318], [361, 329], [374, 348], [389, 374], [397, 407],
    [411, 443], [436, 494], [448, 540], [463, 601], [472, 634],
    [489, 654], [496, 669], [479, 676], [448, 676], [435, 670],
    [437, 641], [433, 622], [414, 584], [400, 547], [390, 516],
    [373, 490], [346, 458], [320, 421], [305, 402], [288, 390],
    [272, 389], [257, 404], [229, 436], [203, 466], [179, 492],
    [173, 516], [168, 557], [162, 585], [148, 624], [150, 649],
    [150, 668], [139, 676], [110, 676], [81, 674], [87, 664],
    [106, 647], [115, 630], [118, 605], [120, 576], [123, 541],
    [123, 504], [130, 470], [145, 435], [168, 390], [190, 351],
    [208, 320], [215, 293], [209, 267], [208, 239], [211, 209],
    [216, 180], [224, 170], [224, 190], [216, 211], [208, 227],
    [207, 249], [205, 268], [191, 252], [174, 233], [162, 219],
    [161, 201], [169, 180], [187, 153], [202, 125], [224, 96],
    [242, 79], [259, 78], [277, 84],
], dtype=float)


def extract(image_path: str | Path, count: int = 2048) -> np.ndarray:
    """Trace the reference pose's stroke centre with 2048 equal-length samples."""
    rgb = np.asarray(Image.open(image_path).convert("RGB"), dtype=float)
    height, width = rgb.shape[:2]
    # Magenta is well separated from the red/green mathematical overlays.
    mask = ((rgb[..., 0] > 105) & (rgb[..., 2] > 90)
            & (rgb[..., 0] > rgb[..., 1] * 1.55)
            & (rgb[..., 2] > rgb[..., 1] * 1.45))
    if mask.sum() < 300:
        raise ValueError("Expected a reference image with a magenta pose contour")
    points = LANDMARKS / REFERENCE_SIZE * [width, height]
    # Snap each hand-audited landmark to the local ink centre; a small radius
    # prevents nearby parts of the hairpin from pulling each other together.
    radius = max(3, round(width / 614 * 4))
    for i, (x, y) in enumerate(points):
        x0, x1 = max(0, round(x) - radius), min(width, round(x) + radius + 1)
        y0, y1 = max(0, round(y) - radius), min(height, round(y) + radius + 1)
        ys, xs = np.where(mask[y0:y1, x0:x1])
        if len(xs):
            points[i] = [xs.mean() + x0, ys.mean() + y0]
    closed = np.vstack([points, points[0]])
    knots = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(closed, axis=0), axis=1))]
    spline = CubicSpline(knots, closed, bc_type="periodic")
    dense = spline(np.linspace(0, knots[-1], 24000))
    distance = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(dense, axis=0), axis=1))]
    target = np.linspace(0, distance[-1], count, endpoint=False)
    xy = np.column_stack([np.interp(target, distance, dense[:, j]) for j in range(2)])
    z = xy[:, 0] - 1j * xy[:, 1]
    z *= 6.1 / np.ptp(z.imag)
    z -= (z.real.max() + z.real.min()) / 2 + 1j * (z.imag.max() + z.imag.min()) / 2
    # Bounding-box centering preserves the intuitive position of head and feet.
    # Fourier reconstruction includes the nonzero centroid as its DC term.
    return z.astype(np.complex128)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path, default=Path("assets/pose_contour.npy"))
    parser.add_argument("--samples", type=int, default=2048)
    args = parser.parse_args()
    z = extract(args.image, args.samples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.output, z)
    print(f"Saved {len(z)} complex centreline samples to {args.output}; height={np.ptp(z.imag):.6f}")


if __name__ == "__main__":
    main()
