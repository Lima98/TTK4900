"""Demonstrate procedural generation as a constraint satisfaction problem.

The example generates a small terrain map by treating every grid cell as a CSP
variable. Each variable has a domain of possible tile types, and local
constraints restrict which tiles may be adjacent. The script visualizes:

1. The tile adjacency rules.
2. How unary constraints and AC-3 propagation shrink cell domains.
3. A complete generated map found by backtracking search.

Run from this directory:
    python constraint_satisfaction_demo.py

The script writes PNG and PDF figures to ./figures.
"""

from __future__ import annotations

import argparse
import random
import os
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

LOCAL_CACHE = Path("/tmp/procgen-constraint-satisfaction-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Rectangle


TILES = ("water", "sand", "grass", "forest", "mountain", "settlement", "path")

COLORS = {
    "water": "#4f8fcf",
    "sand": "#e2c66f",
    "grass": "#77b255",
    "forest": "#2d6a4f",
    "mountain": "#8d8f95",
    "settlement": "#c85d4d",
    "path": "#8b6f47",
}

LABELS = {
    "water": "W",
    "sand": "S",
    "grass": "G",
    "forest": "F",
    "mountain": "M",
    "settlement": "H",
    "path": "P",
}

DOMAIN_SIZE_COLORS = {
    1: "#f7df4f",
    2: "#99d45a",
    3: "#42bf83",
    4: "#2199a8",
    5: "#2f6fa3",
    6: "#473b8f",
    7: "#2b185f",
}

# Local compatibility relation. These are intentionally simple, because the
# figures are meant to explain CSP mechanics rather than optimize map quality.
ALLOWED_NEIGHBORS = {
    "water": {"water", "sand"},
    "sand": {"water", "sand", "grass", "path"},
    "grass": {"sand", "grass", "forest", "mountain", "settlement", "path"},
    "forest": {"grass", "forest", "mountain", "path"},
    "mountain": {"grass", "forest", "mountain"},
    "settlement": {"grass", "path"},
    "path": {"sand", "grass", "forest", "settlement", "path"},
}


@dataclass(frozen=True)
class Problem:
    width: int
    height: int
    domains: dict[tuple[int, int], set[str]]

    @property
    def cells(self) -> list[tuple[int, int]]:
        return [(x, y) for y in range(self.height) for x in range(self.width)]


def neighbors(cell: tuple[int, int], width: int, height: int) -> Iterable[tuple[int, int]]:
    x, y = cell
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            yield nx, ny


def make_problem(width: int, height: int) -> Problem:
    """Create a small map-design problem with boundary and landmark constraints."""

    domains = {(x, y): set(TILES) for y in range(height) for x in range(width)}

    for values in domains.values():
        values.discard("settlement")

    for x in range(width):
        domains[(x, 0)] = {"water", "sand"}
        domains[(x, height - 1)] -= {"water"}

    for y in range(height):
        domains[(0, y)] = {"water", "sand"}
        domains[(width - 1, y)] -= {"water"}

    # A few non-random design intentions: mountain highlands in the north-east,
    # a settlement near the center, and a path outlet in the south-west.
    domains[(width - 2, 2)] = {"mountain"}
    domains[(width - 3, 2)] &= {"grass", "forest", "mountain"}
    settlement = (width // 2, height // 2)
    outlet = (1, height - 2)
    domains[settlement] = {"settlement"}
    domains[outlet] = {"path"}

    # Pin a simple road from the outlet to the settlement. It keeps the example
    # deterministic and lets the remaining tiles demonstrate local constraint
    # propagation instead of spending time searching for a rare connected path.
    for x in range(outlet[0] + 1, settlement[0] + 1):
        if (x, outlet[1]) != settlement:
            domains[(x, outlet[1])] = {"path"}
    for y in range(settlement[1] + 1, outlet[1]):
        domains[(settlement[0], y)] = {"path"}

    return Problem(width, height, domains)


def compatible(left: str, right: str) -> bool:
    return right in ALLOWED_NEIGHBORS[left] and left in ALLOWED_NEIGHBORS[right]


def revise(
    domains: dict[tuple[int, int], set[str]],
    cell: tuple[int, int],
    other: tuple[int, int],
) -> bool:
    removed = {
        tile
        for tile in domains[cell]
        if not any(compatible(tile, candidate) for candidate in domains[other])
    }
    if removed:
        domains[cell] -= removed
    return bool(removed)


def ac3(problem: Problem, domains: dict[tuple[int, int], set[str]] | None = None) -> bool:
    """Arc consistency for the grid adjacency constraints."""

    current = {cell: set(values) for cell, values in (domains or problem.domains).items()}
    queue = deque(
        (cell, other)
        for cell in problem.cells
        for other in neighbors(cell, problem.width, problem.height)
    )

    while queue:
        cell, other = queue.popleft()
        if revise(current, cell, other):
            if not current[cell]:
                return False
            for adjacent in neighbors(cell, problem.width, problem.height):
                if adjacent != other:
                    queue.append((adjacent, cell))

    domains.clear()
    domains.update(current)
    return True


def count_tiles(assignment: dict[tuple[int, int], str], tile: str) -> int:
    return sum(value == tile for value in assignment.values())


def global_constraints_ok(
    assignment: dict[tuple[int, int], str],
    problem: Problem,
    complete: bool,
) -> bool:
    """Keep the generated artifact readable as a map, not only locally valid."""

    settlement = (problem.width // 2, problem.height // 2)
    outlet = (1, problem.height - 2)

    if settlement in assignment and assignment[settlement] != "settlement":
        return False
    if outlet in assignment and assignment[outlet] != "path":
        return False

    if complete:
        return has_path_connection(assignment, outlet, settlement)

    return True


def has_path_connection(
    assignment: dict[tuple[int, int], str],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> bool:
    walkable = {"path", "settlement"}
    frontier = [start]
    seen = {start}

    while frontier:
        cell = frontier.pop()
        if cell == goal:
            return True
        x, y = cell
        for other in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if other in assignment and other not in seen and assignment[other] in walkable:
                seen.add(other)
                frontier.append(other)

    return False


def select_unassigned(
    domains: dict[tuple[int, int], set[str]],
    assignment: dict[tuple[int, int], str],
) -> tuple[int, int]:
    candidates = [cell for cell in domains if cell not in assignment]
    return min(candidates, key=lambda cell: (len(domains[cell]), cell[1], cell[0]))


def ordered_values(
    cell: tuple[int, int],
    domains: dict[tuple[int, int], set[str]],
    assignment: dict[tuple[int, int], str],
    rng: random.Random,
) -> list[str]:
    values = list(domains[cell])

    def score(tile: str) -> tuple[int, float]:
        support = 0
        for other in neighbors(cell, max(x for x, _ in domains) + 1, max(y for _, y in domains) + 1):
            if other not in assignment:
                support += sum(compatible(tile, candidate) for candidate in domains[other])
        return -support, rng.random()

    return sorted(values, key=score)


def consistent_with_assignment(
    cell: tuple[int, int],
    tile: str,
    assignment: dict[tuple[int, int], str],
    problem: Problem,
) -> bool:
    for other in neighbors(cell, problem.width, problem.height):
        if other in assignment and not compatible(tile, assignment[other]):
            return False
    return True


def solve(
    problem: Problem,
    domains: dict[tuple[int, int], set[str]],
    rng: random.Random,
) -> dict[tuple[int, int], str] | None:
    assignment: dict[tuple[int, int], str] = {}

    def backtrack(current_domains: dict[tuple[int, int], set[str]]) -> dict[tuple[int, int], str] | None:
        if len(assignment) == len(problem.cells):
            return dict(assignment) if global_constraints_ok(assignment, problem, complete=True) else None

        cell = select_unassigned(current_domains, assignment)
        for tile in ordered_values(cell, current_domains, assignment, rng):
            if not consistent_with_assignment(cell, tile, assignment, problem):
                continue

            assignment[cell] = tile
            next_domains = {key: set(value) for key, value in current_domains.items()}
            next_domains[cell] = {tile}

            if ac3(problem, next_domains) and global_constraints_ok(assignment, problem, complete=False):
                result = backtrack(next_domains)
                if result is not None:
                    return result

            del assignment[cell]

        return None

    return backtrack(domains)


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"{stem}.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_adjacency_rules(output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")

    positions = {
        "water": (0.0, 1.7),
        "sand": (1.5, 1.7),
        "grass": (3.0, 1.7),
        "forest": (4.5, 1.7),
        "mountain": (6.0, 1.7),
        "path": (3.0, 0.35),
        "settlement": (4.5, 0.35),
    }

    for tile, allowed in ALLOWED_NEIGHBORS.items():
        for other in allowed:
            if TILES.index(tile) <= TILES.index(other) and compatible(tile, other):
                x1, y1 = positions[tile]
                x2, y2 = positions[other]
                ax.plot([x1, x2], [y1, y2], color="#646464", linewidth=1.2, alpha=0.55, zorder=1)

    for tile, (x, y) in positions.items():
        ax.add_patch(Circle((x, y), 0.34, facecolor=COLORS[tile], edgecolor="#222222", linewidth=1.1, zorder=2))
        text_color = "white" if tile in {"water", "forest", "path", "settlement"} else "#1f1f1f"
        ax.text(x, y, LABELS[tile], ha="center", va="center", fontsize=14, color=text_color, weight="bold", zorder=3)
        ax.text(x, y - 0.55, tile, ha="center", va="center", fontsize=9, color="#222222")

    # ax.text(0, 2.45, "Allowed neighbouring tile pairs", fontsize=13, weight="bold", ha="left")
    # ax.text(
    #     0,
    #     2.22,
    #     "Edges encode binary CSP constraints; generation searches for a grid assignment satisfying all edges.",
    #     fontsize=9.5,
    #     color="#333333",
    #     ha="left",
    # )
    save_figure(fig, output_dir, "01_adjacency_constraints")


def domain_text_color(hex_color: str) -> str:
    red = int(hex_color[1:3], 16) / 255
    green = int(hex_color[3:5], 16) / 255
    blue = int(hex_color[5:7], 16) / 255
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return "white" if luminance < 0.45 else "#181818"


def draw_domain_grid(
    problem: Problem,
    before: dict[tuple[int, int], set[str]],
    after: dict[tuple[int, int], set[str]],
    output_dir: Path,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.3))

    for ax, domains, title in zip(axes, (before, after), ("Initial domains", "After AC-3 propagation")):
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=12, pad=8)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, problem.width)
        ax.set_ylim(problem.height, 0)

        for y in range(problem.height):
            for x in range(problem.width):
                cell = (x, y)
                size = len(domains[cell])
                color = DOMAIN_SIZE_COLORS[size]
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor="white", linewidth=1.4))
                if size == 1:
                    label = LABELS[next(iter(domains[cell]))]
                    label_size = 10
                    weight = "bold"
                else:
                    label = str(size)
                    label_size = 9
                    weight = "normal"
                ax.text(
                    x + 0.5,
                    y + 0.5,
                    label,
                    ha="center",
                    va="center",
                    fontsize=label_size,
                    color=domain_text_color(color),
                    weight=weight,
                )

    # fig.suptitle("Constraint propagation reduces the search space", fontsize=13, weight="bold", y=1.02)
    # fig.text(
    #     0.5,
    #     0.02,
    #     "Cell number = remaining domain size; letters mark fixed cells",
    #     ha="center",
    #     fontsize=9,
    #     color="#333333",
    # )
    fig.subplots_adjust(bottom=0.12, wspace=0.2)
    save_figure(fig, output_dir, "02_domain_propagation")


def draw_solution(
    problem: Problem,
    assignment: dict[tuple[int, int], str],
    output_dir: Path,
) -> None:
    cmap = ListedColormap([COLORS[tile] for tile in TILES])
    data = [[TILES.index(assignment[(x, y)]) for x in range(problem.width)] for y in range(problem.height)]

    fig, ax = plt.subplots(figsize=(5.4, 5.2))
    ax.imshow(data, cmap=cmap, vmin=0, vmax=len(TILES) - 1)
    ax.set_xticks([])
    ax.set_yticks([])

    for y in range(problem.height):
        for x in range(problem.width):
            tile = assignment[(x, y)]
            color = "white" if tile in {"water", "forest", "path", "settlement"} else "#1f1f1f"
            ax.text(x, y, LABELS[tile], ha="center", va="center", fontsize=12, color=color, weight="bold")

    for edge in range(problem.width + 1):
        ax.axvline(edge - 0.5, color="white", linewidth=1.4)
    for edge in range(problem.height + 1):
        ax.axhline(edge - 0.5, color="white", linewidth=1.4)

    legend_handles = [
        Rectangle((0, 0), 1, 1, facecolor=COLORS[tile], edgecolor="#222222", label=f"{LABELS[tile]} {tile}")
        for tile in TILES
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=4,
        frameon=False,
        fontsize=8.5,
    )
    # ax.set_title("Generated map satisfying local and global constraints", fontsize=12, weight="bold", pad=10)
    save_figure(fig, output_dir, "03_generated_solution")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=8, help="Grid width.")
    parser.add_argument("--height", type=int, default=8, help="Grid height.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for value ordering.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("figures"))
    args = parser.parse_args()

    rng = random.Random(args.seed)
    problem = make_problem(args.width, args.height)
    initial_domains = {cell: set(values) for cell, values in problem.domains.items()}
    propagated_domains = {cell: set(values) for cell, values in problem.domains.items()}

    if not ac3(problem, propagated_domains):
        raise RuntimeError("The initial constraints are inconsistent.")

    assignment = solve(problem, propagated_domains, rng)
    if assignment is None:
        raise RuntimeError("No solution found. Try a different seed or larger grid.")

    draw_adjacency_rules(args.output_dir)
    draw_domain_grid(problem, initial_domains, propagated_domains, args.output_dir)
    draw_solution(problem, assignment, args.output_dir)

    print(f"Wrote figures to {args.output_dir}")


if __name__ == "__main__":
    main()
