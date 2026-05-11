"""Illustrate Wave Function Collapse for procedural content generation.

This is a compact tiled-model WFC demonstration. It learns local adjacency
rules from a small exemplar map, then generates new maps by repeatedly:

1. Observing the cell with the smallest remaining domain.
2. Collapsing it to one tile, sampled from exemplar frequencies.
3. Propagating the consequences to neighbouring cells.

Run from the repository root:
    code/.proc-gen-examples/.venv/bin/python \
        code/.proc-gen-examples/wave-function-collapse/wfc_demo.py

The script writes PDF figures to ./figures.
"""

from __future__ import annotations

import argparse
import os
import random
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

LOCAL_CACHE = Path("/tmp/procgen-wfc-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch, Rectangle


EXEMPLAR = [
    "WWWWWSSGGGG",
    "WWWSSSGGFFF",
    "WWSSGGGFFFM",
    "SSSGGGFFMMM",
    "SSGGGGFFMMM",
    "GGGGGFFMMMM",
    "GGGFFFMMMMM",
    "GGFFMMMMMMM",
]

TILES = ("W", "S", "G", "F", "M")
NAMES = {
    "W": "water",
    "S": "sand",
    "G": "grass",
    "F": "forest",
    "M": "mountain",
}
COLORS = {
    "W": "#4f8fcf",
    "S": "#e1c66f",
    "G": "#78b159",
    "F": "#2d6a4f",
    "M": "#8d8f95",
}
DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}


@dataclass
class WFCState:
    width: int
    height: int
    domains: Dict[Tuple[int, int], Set[str]]
    history: List[Dict[Tuple[int, int], Set[str]]]

    @property
    def cells(self) -> List[Tuple[int, int]]:
        return [(x, y) for y in range(self.height) for x in range(self.width)]


def exemplar_array() -> np.ndarray:
    return np.array([[TILES.index(char) for char in row] for row in EXEMPLAR])


def learn_rules(exemplar: Sequence[str]) -> Tuple[Dict[str, Dict[str, Set[str]]], Counter]:
    rules = {tile: {direction: set() for direction in DIRECTIONS} for tile in TILES}
    counts: Counter = Counter()
    height = len(exemplar)
    width = len(exemplar[0])

    for y, row in enumerate(exemplar):
        for x, tile in enumerate(row):
            counts[tile] += 1
            for direction, (dx, dy) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    rules[tile][direction].add(exemplar[ny][nx])

    # Ensure every tile can continue next to itself when the exemplar shows it,
    # which makes large generated regions possible without adding external art.
    for tile in TILES:
        for direction in DIRECTIONS:
            if counts[tile] > 1:
                rules[tile][direction].add(tile)

    return rules, counts


def copy_domains(domains: Dict[Tuple[int, int], Set[str]]) -> Dict[Tuple[int, int], Set[str]]:
    return {cell: set(values) for cell, values in domains.items()}


def weighted_choice(values: Iterable[str], counts: Counter, rng: random.Random) -> str:
    ordered = sorted(values)
    weights = [counts[value] for value in ordered]
    total = sum(weights)
    pick = rng.uniform(0, total)
    cumulative = 0.0
    for value, weight in zip(ordered, weights):
        cumulative += weight
        if pick <= cumulative:
            return value
    return ordered[-1]


def allowed_from_neighbor(
    neighbor_domain: Set[str],
    direction_from_neighbor: str,
    rules: Dict[str, Dict[str, Set[str]]],
) -> Set[str]:
    allowed: Set[str] = set()
    for neighbor_tile in neighbor_domain:
        allowed.update(rules[neighbor_tile][direction_from_neighbor])
    return allowed


def propagate(
    state: WFCState,
    start_cells: Iterable[Tuple[int, int]],
    rules: Dict[str, Dict[str, Set[str]]],
) -> bool:
    queue = deque(start_cells)

    while queue:
        x, y = queue.popleft()
        for direction, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < state.width and 0 <= ny < state.height):
                continue

            neighbor = (nx, ny)
            allowed = allowed_from_neighbor(state.domains[(x, y)], direction, rules)
            reduced = state.domains[neighbor] & allowed

            if not reduced:
                return False
            if reduced != state.domains[neighbor]:
                state.domains[neighbor] = reduced
                queue.append(neighbor)

    return True


def observe_cell(state: WFCState, rng: random.Random) -> Optional[Tuple[int, int]]:
    undecided = [cell for cell in state.cells if len(state.domains[cell]) > 1]
    if not undecided:
        return None
    smallest = min(len(state.domains[cell]) for cell in undecided)
    candidates = [cell for cell in undecided if len(state.domains[cell]) == smallest]
    return rng.choice(candidates)


def run_wfc(
    width: int,
    height: int,
    seed: int,
    rules: Dict[str, Dict[str, Set[str]]],
    counts: Counter,
    max_steps: int = 10_000,
) -> WFCState:
    rng = random.Random(seed)

    for attempt in range(80):
        state = WFCState(
            width=width,
            height=height,
            domains={(x, y): set(TILES) for y in range(height) for x in range(width)},
            history=[],
        )
        state.history.append(copy_domains(state.domains))

        for _ in range(max_steps):
            cell = observe_cell(state, rng)
            if cell is None:
                state.history.append(copy_domains(state.domains))
                return state

            chosen = weighted_choice(state.domains[cell], counts, rng)
            state.domains[cell] = {chosen}
            if not propagate(state, [cell], rules):
                break

            if len(state.history) < 8 or all(len(values) == 1 for values in state.domains.values()):
                state.history.append(copy_domains(state.domains))

        rng.seed(seed + attempt + 1)

    raise RuntimeError("WFC failed after several restarts. Try a different seed.")


def collapse_to_array(state: WFCState) -> np.ndarray:
    result = np.zeros((state.height, state.width), dtype=int)
    for y in range(state.height):
        for x in range(state.width):
            domain = state.domains[(x, y)]
            if len(domain) != 1:
                result[y, x] = -1
            else:
                result[y, x] = TILES.index(next(iter(domain)))
    return result


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / f"{stem}.pdf", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_grid(
    ax: plt.Axes,
    data: np.ndarray,
    title: str,
    show_letters: bool = True,
) -> None:
    cmap = ListedColormap([COLORS[tile] for tile in TILES])
    ax.imshow(data, cmap=cmap, vmin=0, vmax=len(TILES) - 1, interpolation="nearest")
    if title:
        ax.set_title(title, fontsize=11, pad=6)
    ax.set_xticks([])
    ax.set_yticks([])

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            tile = TILES[int(data[y, x])]
            if show_letters:
                color = "white" if tile in {"W", "F"} else "#171717"
                ax.text(x, y, tile, ha="center", va="center", fontsize=8.5, color=color, weight="bold")


def draw_exemplar_and_rules(
    rules: Dict[str, Dict[str, Set[str]]],
    counts: Counter,
    output_dir: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2), gridspec_kw={"width_ratios": [1.05, 1.25]})
    # fig.suptitle("WFC learns local tile rules from a small exemplar", fontsize=13, weight="bold", y=0.98)

    draw_grid(axes[0], exemplar_array(), "", show_letters=True)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(-0.55, 5.75)
    ax.set_ylim(-1.7, 3.0)

    positions = {
        "W": (0, 0.95),
        "S": (1.3, 0.95),
        "G": (2.6, 0.95),
        "F": (3.9, 0.95),
        "M": (5.2, 0.95),
    }

    for tile, (x, y) in positions.items():
        ax.add_patch(Rectangle((x - 0.38, y - 0.38), 0.76, 0.76, facecolor=COLORS[tile], edgecolor="#222222", linewidth=1.2))
        color = "white" if tile in {"W", "F"} else "#171717"
        ax.text(x, y, tile, ha="center", va="center", fontsize=13, color=color, weight="bold")
        ax.text(x, y - 0.62, f"{NAMES[tile]}\nweight {counts[tile]}", ha="center", va="top", fontsize=7.7)

    drawn = set()
    for tile in TILES:
        for direction in DIRECTIONS:
            for other in rules[tile][direction]:
                key = tuple(sorted((tile, other)))
                if key in drawn or tile == other:
                    continue
                drawn.add(key)
                x1, y1 = positions[tile]
                x2, y2 = positions[other]
                arrow = FancyArrowPatch(
                    (x1, y1),
                    (x2, y2),
                    arrowstyle="-",
                    color="#555555",
                    linewidth=1.2,
                    alpha=0.48,
                    mutation_scale=8,
                    zorder=0,
                )
                ax.add_patch(arrow)

    fig.subplots_adjust(top=0.82, bottom=0.14, wspace=0.22)
    left_box = axes[0].get_position()
    right_box = axes[1].get_position()
    title_y = left_box.y1 + 0.026
    fig.text((left_box.x0 + left_box.x1) / 2, title_y, "exemplar", ha="center", va="bottom", fontsize=11)
    fig.text((right_box.x0 + right_box.x1) / 2, title_y, "learned neighbourhoods", ha="center", va="bottom", fontsize=11)
    # fig.text(0.5, 0.02, "Edges summarize tile pairs observed next to each other in the exemplar.", ha="center", fontsize=9.2, color="#333333")
    save_figure(fig, output_dir, "01_exemplar_and_rules")


def domain_snapshot_array(state: WFCState, domains: Dict[Tuple[int, int], Set[str]]) -> np.ndarray:
    data = np.zeros((state.height, state.width))
    for y in range(state.height):
        for x in range(state.width):
            data[y, x] = len(domains[(x, y)])
    return data


def readable_text_color(value: float, cmap_name: str = "viridis_r", vmin: float = 1, vmax: float = len(TILES)) -> str:
    cmap = plt.get_cmap(cmap_name)
    normalized = (value - vmin) / (vmax - vmin)
    red, green, blue, _ = cmap(np.clip(normalized, 0, 1))
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    if luminance < 0.46:
        return "white"
    return "#111111"


def selected_wfc_snapshots(state: WFCState) -> List[Tuple[str, Dict[Tuple[int, int], Set[str]]]]:
    if len(state.history) < 4:
        labels = ["initial_wave", "after_first_collapse", "after_propagation", "complete_collapse"]
        return list(zip(labels[: len(state.history)], state.history))

    return [
        ("initial_wave", state.history[0]),
        ("after_first_collapse", state.history[1]),
        ("after_propagation", state.history[min(4, len(state.history) - 2)]),
        ("complete_collapse", state.history[-1]),
    ]


def draw_wfc_snapshot(
    ax: plt.Axes,
    state: WFCState,
    domains: Dict[Tuple[int, int], Set[str]],
    text_scale: float = 1.0,
) -> None:
    sizes = domain_snapshot_array(state, domains)
    ax.imshow(sizes, cmap="viridis_r", vmin=1, vmax=len(TILES), interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])

    for y in range(state.height):
        for x in range(state.width):
            domain = domains[(x, y)]
            text_color = readable_text_color(len(domain))
            if len(domain) == 1:
                tile = next(iter(domain))
                ax.text(
                    x,
                    y,
                    tile,
                    ha="center",
                    va="center",
                    fontsize=8.7 * text_scale,
                    color=text_color,
                    weight="bold",
                )
            else:
                ax.text(
                    x,
                    y,
                    str(len(domain)),
                    ha="center",
                    va="center",
                    fontsize=7.8 * text_scale,
                    color=text_color,
                )


def draw_wfc_steps(state: WFCState, output_dir: Path) -> None:
    for label, domains in selected_wfc_snapshots(state):
        fig, ax = plt.subplots(figsize=(4.8, 3.5))
        draw_wfc_snapshot(ax, state, domains, text_scale=1.08)
        save_figure(fig, output_dir, f"02_{label}")


def draw_final_output(state: WFCState, output_dir: Path, stem: str = "03_generated_wfc_map") -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    draw_grid(ax, collapse_to_array(state), "", show_letters=True)

    legend = [
        Rectangle((0, 0), 1, 1, facecolor=COLORS[tile], edgecolor="#222222", label=f"{tile} {NAMES[tile]}")
        for tile in TILES
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3, frameon=False, fontsize=14)
    save_figure(fig, output_dir, stem)


def draw_seed_variations(
    width: int,
    height: int,
    seeds: Sequence[int],
    rules: Dict[str, Dict[str, Set[str]]],
    counts: Counter,
    output_dir: Path,
) -> None:
    fig, axes = plt.subplots(1, len(seeds), figsize=(10.0, 3.7))
    # fig.suptitle("The learned rules stay fixed while the seed changes the output", fontsize=13, weight="bold", y=0.98)

    for ax, seed in zip(axes, seeds):
        state = run_wfc(width, height, seed, rules, counts)
        draw_grid(ax, collapse_to_array(state), f"seed = {seed}", show_letters=False)

    fig.subplots_adjust(top=0.8, bottom=0.08, wspace=0.18)
    save_figure(fig, output_dir, "04_seed_variations")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=18, help="Generated output width.")
    parser.add_argument("--height", type=int, default=12, help="Generated output height.")
    parser.add_argument("--seed", type=int, default=19, help="Random seed.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("figures"))
    args = parser.parse_args()

    rules, counts = learn_rules(EXEMPLAR)
    state = run_wfc(args.width, args.height, args.seed, rules, counts)

    draw_exemplar_and_rules(rules, counts, args.output_dir)
    draw_wfc_steps(state, args.output_dir)
    draw_final_output(state, args.output_dir)
    draw_seed_variations(args.width, args.height, [3, 19, 41], rules, counts, args.output_dir)

    print(f"Wrote figures to {args.output_dir}")


if __name__ == "__main__":
    main()
