"""Illustrate seed-based random noise for procedural generation.

The example builds terrain-like maps from deterministic pseudo-random noise.
It uses value noise and fractal Brownian motion (fBm): coarse random grids are
smoothly interpolated, then multiple octaves are layered to create structure at
several scales. A seed makes the result reproducible while still allowing many
different outputs.

Run from the repository root:
    code/.proc-gen-examples/.venv/bin/python \
        code/.proc-gen-examples/noise-and-seeds/noise_seed_demo.py

The script writes PNG and PDF figures to ./figures.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, Tuple

LOCAL_CACHE = Path("/tmp/procgen-noise-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle


TERRAIN = [
    ("deep water", "#2c5aa0"),
    ("shallow water", "#4f8fcf"),
    ("beach", "#e0c36d"),
    ("grassland", "#7cb35d"),
    ("forest", "#2d6a4f"),
    ("mountain", "#8d8f95"),
    ("snow", "#f2f5f7"),
]


def smoothstep(t: np.ndarray) -> np.ndarray:
    return t * t * (3.0 - 2.0 * t)


def normalize(values: np.ndarray) -> np.ndarray:
    low = values.min()
    high = values.max()
    if high == low:
        return np.zeros_like(values)
    return (values - low) / (high - low)


def value_noise(width: int, height: int, frequency: int, seed: int) -> np.ndarray:
    """Generate smooth 2D value noise by interpolating a random lattice."""

    rng = np.random.default_rng(seed)
    lattice_w = frequency + 1
    lattice_h = frequency + 1
    lattice = rng.random((lattice_h, lattice_w))

    x = np.linspace(0, frequency, width, endpoint=False)
    y = np.linspace(0, frequency, height, endpoint=False)
    xi = np.floor(x).astype(int)
    yi = np.floor(y).astype(int)
    xf = smoothstep(x - xi)
    yf = smoothstep(y - yi)

    xi1 = np.minimum(xi + 1, frequency)
    yi1 = np.minimum(yi + 1, frequency)

    top = lattice[yi[:, None], xi] * (1 - xf) + lattice[yi[:, None], xi1] * xf
    bottom = lattice[yi1[:, None], xi] * (1 - xf) + lattice[yi1[:, None], xi1] * xf
    return top * (1 - yf[:, None]) + bottom * yf[:, None]


def fbm_noise(
    width: int,
    height: int,
    seed: int,
    octaves: int = 5,
    base_frequency: int = 3,
    persistence: float = 0.55,
    lacunarity: int = 2,
) -> np.ndarray:
    """Layer value-noise octaves to produce fractal Brownian motion."""

    total = np.zeros((height, width))
    amplitude = 1.0
    amplitude_sum = 0.0
    frequency = base_frequency

    for octave in range(octaves):
        total += value_noise(width, height, frequency, seed + octave * 101) * amplitude
        amplitude_sum += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    return normalize(total / amplitude_sum)


def radial_falloff(width: int, height: int, strength: float = 0.75) -> np.ndarray:
    """Create an island-shaped mask that lowers terrain near the edges."""

    xs = np.linspace(-1, 1, width)
    ys = np.linspace(-1, 1, height)
    distance = np.sqrt(xs[None, :] ** 2 + ys[:, None] ** 2)
    return np.clip(1.0 - distance * strength, 0.0, 1.0)


def classify_terrain(heightmap: np.ndarray) -> np.ndarray:
    thresholds = [0.26, 0.34, 0.43, 0.61, 0.76, 0.88]
    return np.digitize(heightmap, thresholds)


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"{stem}.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_seed_comparison(width: int, height: int, seeds: Iterable[int], output_dir: Path) -> None:
    seed_list = list(seeds)
    fig, axes = plt.subplots(1, len(seed_list), figsize=(9.6, 3.0))
    fig.suptitle("A seed makes random generation reproducible", fontsize=13, weight="bold", y=0.96)

    for ax, seed in zip(axes, seed_list):
        noise = fbm_noise(width, height, seed=seed)
        island = normalize(noise * 0.72 + radial_falloff(width, height) * 0.42)
        ax.imshow(island, cmap="terrain", interpolation="nearest")
        ax.set_title(f"seed = {seed}", fontsize=11, pad=6)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.text(
        0.5,
        0.02,
        "Same algorithm and parameters, different seeds: repeatable variation.",
        ha="center",
        fontsize=9.5,
        color="#333333",
    )
    fig.subplots_adjust(top=0.78, bottom=0.16, wspace=0.2)
    save_figure(fig, output_dir, "01_seed_variation")


def draw_octave_layers(width: int, height: int, seed: int, output_dir: Path) -> None:
    layers = [
        ("1 octave", fbm_noise(width, height, seed=seed, octaves=1, base_frequency=3)),
        ("3 octaves", fbm_noise(width, height, seed=seed, octaves=3, base_frequency=3)),
        ("6 octaves", fbm_noise(width, height, seed=seed, octaves=6, base_frequency=3)),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.5))

    for ax, (title, layer) in zip(axes, layers):
        ax.imshow(layer, cmap="viridis", interpolation="nearest")
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.subplots_adjust(top=0.95, bottom=0.06, left=0.03, right=0.97, wspace=0.12)
    save_figure(fig, output_dir, "02_noise_octaves")


def draw_terrain_pipeline(width: int, height: int, seed: int, output_dir: Path) -> None:
    noise = fbm_noise(width, height, seed=seed, octaves=6, base_frequency=3)
    falloff = radial_falloff(width, height)
    heightmap = normalize(noise * 0.74 + falloff * 0.42)
    terrain = classify_terrain(heightmap)

    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.2))

    axes[0].imshow(noise, cmap="viridis", interpolation="nearest")
    axes[0].set_title("layered noise", fontsize=11)

    axes[1].imshow(heightmap, cmap="terrain", interpolation="nearest")
    axes[1].set_title("height map + falloff", fontsize=11)

    terrain_cmap = ListedColormap([color for _, color in TERRAIN])
    axes[2].imshow(terrain, cmap=terrain_cmap, vmin=0, vmax=len(TERRAIN) - 1, interpolation="nearest")
    axes[2].set_title("classified terrain", fontsize=11)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    legend = [
        Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="#222222", label=name)
        for name, color in TERRAIN
    ]
    axes[2].legend(
        handles=legend,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=False,
        fontsize=14,
    )

    fig.subplots_adjust(top=0.95, bottom=0.12, left=0.03, right=0.97, wspace=0.16)
    save_figure(fig, output_dir, "03_noise_to_terrain")


def draw_octaves_to_terrain_story(width: int, height: int, seed: int, output_dir: Path) -> None:
    """Recreate the full octave-layering and terrain-classification thesis figure."""

    octave_layers = [
        ("1 octave", fbm_noise(width, height, seed=seed, octaves=1, base_frequency=3)),
        ("3 octaves", fbm_noise(width, height, seed=seed, octaves=3, base_frequency=3)),
        ("6 octaves", fbm_noise(width, height, seed=seed, octaves=6, base_frequency=3)),
    ]

    noise = octave_layers[-1][1]
    falloff = radial_falloff(width, height)
    heightmap = normalize(noise * 0.74 + falloff * 0.42)
    terrain = classify_terrain(heightmap)
    terrain_cmap = ListedColormap([color for _, color in TERRAIN])

    fig = plt.figure(figsize=(10.6, 7.0))
    grid = GridSpec(
        5,
        3,
        figure=fig,
        height_ratios=[0.35, 2.35, 0.35, 2.55, 0.9],
        hspace=0.22,
        wspace=0.08,
    )

    title_ax_top = fig.add_subplot(grid[0, :])
    title_ax_top.axis("off")
    title_ax_top.text(
        0.5,
        0.4,
        "layering different octaves",
        ha="center",
        va="center",
        fontsize=12,
        style="italic",
    )

    for column, (title, layer) in enumerate(octave_layers):
        ax = fig.add_subplot(grid[1, column])
        ax.imshow(layer, cmap="viridis", interpolation="nearest")
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xticks([])
        ax.set_yticks([])

    title_ax_bottom = fig.add_subplot(grid[2, :])
    title_ax_bottom.axis("off")
    title_ax_bottom.text(
        0.5,
        0.4,
        "classifying the noise",
        ha="center",
        va="center",
        fontsize=12,
        style="italic",
    )

    pipeline_titles = ["layered noise", "height map + falloff", "classified terrain"]
    pipeline_data = [
        (noise, {"cmap": "viridis"}),
        (heightmap, {"cmap": "terrain"}),
        (terrain, {"cmap": terrain_cmap, "vmin": 0, "vmax": len(TERRAIN) - 1}),
    ]

    for column, (title, (data, kwargs)) in enumerate(zip(pipeline_titles, pipeline_data)):
        ax = fig.add_subplot(grid[3, column])
        ax.imshow(data, interpolation="nearest", **kwargs)
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xticks([])
        ax.set_yticks([])

    legend_ax = fig.add_subplot(grid[4, :])
    legend_ax.axis("off")
    legend_handles = [
        Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="#222222", label=name)
        for name, color in TERRAIN
    ]
    legend_ax.legend(
        handles=legend_handles,
        loc="center",
        ncol=4,
        frameon=False,
        fontsize=14,
        columnspacing=1.4,
        handlelength=1.4,
        handletextpad=0.55,
        borderaxespad=0.0,
    )

    fig.subplots_adjust(left=0.04, right=0.96, top=0.97, bottom=0.05)
    save_figure(fig, output_dir, "03_noise_to_terrain_story")


def draw_parameter_control(width: int, height: int, seed: int, output_dir: Path) -> None:
    configs = [
        ("smooth", {"octaves": 3, "base_frequency": 2, "persistence": 0.45}),
        ("balanced", {"octaves": 5, "base_frequency": 3, "persistence": 0.55}),
        ("rugged", {"octaves": 7, "base_frequency": 5, "persistence": 0.68}),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.5))

    for ax, (title, kwargs) in zip(axes, configs):
        noise = fbm_noise(width, height, seed=seed, **kwargs)
        heightmap = normalize(noise * 0.74 + radial_falloff(width, height) * 0.42)
        ax.imshow(heightmap, cmap="terrain", interpolation="nearest")
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.subplots_adjust(top=0.95, bottom=0.06, left=0.03, right=0.97, wspace=0.12)
    save_figure(fig, output_dir, "04_parameter_control")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=128, help="Generated image width.")
    parser.add_argument("--height", type=int, default=96, help="Generated image height.")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("figures"))
    args = parser.parse_args()

    draw_seed_comparison(args.width, args.height, [12, 42, 77], args.output_dir)
    draw_octave_layers(args.width, args.height, args.seed, args.output_dir)
    draw_terrain_pipeline(args.width, args.height, args.seed, args.output_dir)
    draw_octaves_to_terrain_story(args.width, args.height, args.seed, args.output_dir)
    draw_parameter_control(args.width, args.height, args.seed, args.output_dir)

    print(f"Wrote figures to {args.output_dir}")


if __name__ == "__main__":
    main()
