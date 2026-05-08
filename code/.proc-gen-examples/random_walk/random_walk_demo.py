"""Create thesis-ready random-walk texture examples.

The script generates three walk-based textures with a consistent visual style:

- wood-like grain from vertical bias
- sand-like ripples from diagonal drift
- terrain-like density map from mostly unbiased walkers

Run from the repository root:
    code/.proc-gen-examples/.venv/bin/python \
        code/.proc-gen-examples/random_walk/random_walk_demo.py
"""

from __future__ import annotations

import os
from pathlib import Path

LOCAL_CACHE = Path("/tmp/procgen-random-walk-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def normalize(values: np.ndarray) -> np.ndarray:
    low = float(values.min())
    high = float(values.max())
    if high <= low:
        return np.zeros_like(values)
    return (values - low) / (high - low)


def biased_walk_field(
    *,
    size: int,
    walkers: int,
    steps: int,
    seed: int,
    drift: tuple[float, float],
    jitter: float = 1.0,
    restart_chance: float = 0.0,
    edge_wrap: bool = True,
) -> np.ndarray:
    """Accumulate visit density from many biased 2D random walkers."""

    rng = np.random.default_rng(seed)
    field = np.zeros((size, size), dtype=float)
    directions = np.array(
        [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
            [1, 1],
            [1, -1],
            [-1, 1],
            [-1, -1],
        ],
        dtype=float,
    )
    drift_vector = np.array(drift, dtype=float)

    for _ in range(walkers):
        x = int(rng.integers(0, size))
        y = int(rng.integers(0, size))
        for _ in range(steps):
            scores = directions @ drift_vector + rng.normal(scale=jitter, size=len(directions))
            direction = directions[int(np.argmax(scores))]
            x += int(direction[0])
            y += int(direction[1])

            if edge_wrap:
                x %= size
                y %= size
            else:
                x = max(0, min(size - 1, x))
                y = max(0, min(size - 1, y))

            field[y, x] += 1.0

            if restart_chance > 0 and rng.random() < restart_chance:
                x = int(rng.integers(0, size))
                y = int(rng.integers(0, size))

    return normalize(field)


def blur_pass(values: np.ndarray, rounds: int = 1) -> np.ndarray:
    """Lightweight neighbor blur without SciPy."""

    result = values.copy()
    for _ in range(rounds):
        result = (
            result
            + np.roll(result, 1, axis=0)
            + np.roll(result, -1, axis=0)
            + np.roll(result, 1, axis=1)
            + np.roll(result, -1, axis=1)
        ) / 5.0
    return result


def wood_texture(size: int, seed: int) -> np.ndarray:
    base = biased_walk_field(
        size=size,
        walkers=140,
        steps=1600,
        seed=seed,
        drift=(0.0, 1.8),
        jitter=0.8,
        restart_chance=0.015,
    )
    base = blur_pass(base, rounds=4)
    xs = np.linspace(0.0, 1.0, size)
    column_wave = np.sin(xs[None, :] * 34.0 + base * 11.0)
    slow_wave = np.sin(xs[None, :] * 9.0 + base * 4.0)
    grain = 0.16 * column_wave + 0.08 * slow_wave
    return normalize(base * 0.82 + grain + 0.14)


def sand_texture(size: int, seed: int) -> np.ndarray:
    base = biased_walk_field(
        size=size,
        walkers=180,
        steps=1200,
        seed=seed,
        drift=(1.3, 0.9),
        jitter=1.0,
        restart_chance=0.02,
    )
    diagonal = np.add.outer(np.linspace(0.0, 1.0, size), np.linspace(0.0, 1.0, size))
    ripples = 0.12 * np.sin(diagonal * 26.0 + base * 7.0)
    cross_ripples = 0.05 * np.sin((diagonal * 9.0) + base * 5.0)
    return normalize(blur_pass(base, rounds=3) * 0.8 + ripples + cross_ripples + 0.18)


def terrain_texture(size: int, seed: int) -> np.ndarray:
    base = biased_walk_field(
        size=size,
        walkers=220,
        steps=1500,
        seed=seed,
        drift=(0.1, 0.0),
        jitter=1.25,
        restart_chance=0.03,
    )
    base = blur_pass(base, rounds=5)
    xs = np.linspace(-1.0, 1.0, size)
    ys = np.linspace(-1.0, 1.0, size)
    falloff = 1.0 - np.sqrt(xs[None, :] ** 2 + ys[:, None] ** 2) * 0.72
    ridge = 0.08 * np.sin(xs[None, :] * 7.0) + 0.06 * np.cos(ys[:, None] * 6.0)
    return normalize(base * 0.68 + np.clip(falloff, 0.0, 1.0) * 0.38 + ridge)


WOOD_CMAP = LinearSegmentedColormap.from_list(
    "rw_wood",
    ["#1b1511", "#4f321a", "#8f5d2e", "#ba8a57", "#e0be8f"],
)

SAND_CMAP = LinearSegmentedColormap.from_list(
    "rw_sand",
    ["#3d2b1f", "#8e6a3d", "#c59b63", "#e5c68f", "#f4e7bf"],
)

TERRAIN_CMAP = ListedColormap(
    ["#315d93", "#5f9fd0", "#d8c06f", "#82b766", "#3f7f55", "#8a847e", "#f2f5f7"]
)


def terrain_classes(values: np.ndarray) -> np.ndarray:
    thresholds = [0.22, 0.34, 0.46, 0.62, 0.76, 0.88]
    return np.digitize(values, thresholds)


def save_image(
    values: np.ndarray,
    output_path: Path,
    *,
    cmap,
    title: str,
    classify: bool = False,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = terrain_classes(values) if classify else values
    fig, ax = plt.subplots(figsize=(3.2, 3.35))
    ax.imshow(image, cmap=cmap, interpolation="nearest", origin="upper")
    ax.set_title(title, fontsize=10, pad=6)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_edgecolor("#222222")
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.03, right=0.97, bottom=0.03, top=0.90)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.02, facecolor="white")
    plt.close(fig)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    thesis_dir = repo_root / "thesis" / "latex" / "Figures" / "04theory"
    save_image(wood_texture(256, seed=17), thesis_dir / "ex_wood.png", cmap=WOOD_CMAP, title="vertical bias")
    save_image(sand_texture(256, seed=29), thesis_dir / "ex_sand.png", cmap=SAND_CMAP, title="diagonal bias")
    save_image(
        terrain_texture(256, seed=41),
        thesis_dir / "ex_map.png",
        cmap=TERRAIN_CMAP,
        title="classified density map",
        classify=True,
    )
    print(f"Wrote figures to {thesis_dir}")


if __name__ == "__main__":
    main()
