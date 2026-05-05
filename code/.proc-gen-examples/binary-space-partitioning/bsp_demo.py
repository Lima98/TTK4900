"""Illustrate binary space partitioning for procedural content generation.

The example recursively splits a rectangular map into smaller regions, places
one room inside each final partition, and connects sibling partitions with
corridors. This is a common constructive technique for dungeon and level
generation because it gives a designer direct control over hierarchy, density,
and spatial scale.

Run from the repository root:
    code/.proc-gen-examples/.venv/bin/python \
        code/.proc-gen-examples/binary-space-partitioning/bsp_demo.py

The script writes PNG and PDF figures to ./figures.
"""

from __future__ import annotations

import argparse
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

LOCAL_CACHE = Path("/tmp/procgen-bsp-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle


WALL = 0
FLOOR = 1
ROOM = 2
CORRIDOR = 3


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> Tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2


@dataclass
class Node:
    rect: Rect
    depth: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    room: Optional[Rect] = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def split_node(
    node: Node,
    rng: random.Random,
    max_depth: int,
    min_leaf_size: int,
) -> None:
    """Recursively split the node into two subregions."""

    rect = node.rect
    if node.depth >= max_depth or (rect.w < min_leaf_size * 2 and rect.h < min_leaf_size * 2):
        return

    if rect.w / rect.h >= 1.25:
        split_vertical = True
    elif rect.h / rect.w >= 1.25:
        split_vertical = False
    else:
        split_vertical = rng.choice([True, False])

    if split_vertical and rect.w >= min_leaf_size * 2:
        split_at = rng.randint(min_leaf_size, rect.w - min_leaf_size)
        first = Rect(rect.x, rect.y, split_at, rect.h)
        second = Rect(rect.x + split_at, rect.y, rect.w - split_at, rect.h)
    elif rect.h >= min_leaf_size * 2:
        split_at = rng.randint(min_leaf_size, rect.h - min_leaf_size)
        first = Rect(rect.x, rect.y, rect.w, split_at)
        second = Rect(rect.x, rect.y + split_at, rect.w, rect.h - split_at)
    else:
        return

    node.left = Node(first, node.depth + 1)
    node.right = Node(second, node.depth + 1)
    split_node(node.left, rng, max_depth, min_leaf_size)
    split_node(node.right, rng, max_depth, min_leaf_size)


def leaves(node: Node) -> List[Node]:
    if node.is_leaf:
        return [node]
    result = []
    if node.left is not None:
        result.extend(leaves(node.left))
    if node.right is not None:
        result.extend(leaves(node.right))
    return result


def internal_nodes(node: Node) -> List[Node]:
    if node.is_leaf:
        return []
    result = [node]
    if node.left is not None:
        result.extend(internal_nodes(node.left))
    if node.right is not None:
        result.extend(internal_nodes(node.right))
    return result


def create_rooms(root: Node, rng: random.Random, margin: int = 1) -> List[Rect]:
    rooms = []
    for leaf in leaves(root):
        max_w = max(3, leaf.rect.w - margin * 2)
        max_h = max(3, leaf.rect.h - margin * 2)
        room_w = rng.randint(max(3, int(max_w * 0.55)), max_w)
        room_h = rng.randint(max(3, int(max_h * 0.55)), max_h)
        room_x = rng.randint(leaf.rect.x + margin, leaf.rect.x + leaf.rect.w - room_w - margin)
        room_y = rng.randint(leaf.rect.y + margin, leaf.rect.y + leaf.rect.h - room_h - margin)
        leaf.room = Rect(room_x, room_y, room_w, room_h)
        rooms.append(leaf.room)
    return rooms


def representative_room(node: Node) -> Rect:
    if node.room is not None:
        return node.room
    if node.left is not None:
        return representative_room(node.left)
    if node.right is not None:
        return representative_room(node.right)
    raise ValueError("Node has no room.")


def corridor_between(a: Rect, b: Rect) -> List[Tuple[int, int]]:
    ax, ay = a.center
    bx, by = b.center
    cells = []
    step_x = 1 if bx >= ax else -1
    for x in range(ax, bx + step_x, step_x):
        cells.append((x, ay))
    step_y = 1 if by >= ay else -1
    for y in range(ay, by + step_y, step_y):
        cells.append((bx, y))
    return cells


def create_corridors(root: Node) -> List[List[Tuple[int, int]]]:
    corridors = []
    for node in internal_nodes(root):
        if node.left is None or node.right is None:
            continue
        left_room = representative_room(node.left)
        right_room = representative_room(node.right)
        corridors.append(corridor_between(left_room, right_room))
    return corridors


def rasterize(
    width: int,
    height: int,
    rooms: List[Rect],
    corridors: List[List[Tuple[int, int]]],
) -> List[List[int]]:
    grid = [[WALL for _ in range(width)] for _ in range(height)]

    for room in rooms:
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                grid[y][x] = ROOM

    for corridor in corridors:
        for x, y in corridor:
            if 0 <= x < width and 0 <= y < height and grid[y][x] != ROOM:
                grid[y][x] = CORRIDOR

    for y in range(height):
        for x in range(width):
            if grid[y][x] in {ROOM, CORRIDOR}:
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    for ny in range(max(0, y - 1), min(height, y + 2)):
                        if grid[ny][nx] == WALL:
                            grid[ny][nx] = FLOOR

    for room in rooms:
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                grid[y][x] = ROOM

    for corridor in corridors:
        for x, y in corridor:
            if 0 <= x < width and 0 <= y < height and grid[y][x] != ROOM:
                grid[y][x] = CORRIDOR

    return grid


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"{stem}.{suffix}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def draw_partition_tree(root: Node, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Binary space partitioning recursively divides the map", fontsize=13, weight="bold", pad=12)

    palette = ["#e9c46a", "#90be6d", "#43aa8b", "#577590", "#f4a261", "#b56576"]
    for leaf in leaves(root):
        color = palette[leaf.depth % len(palette)]
        ax.add_patch(
            Rectangle(
                (leaf.rect.x, leaf.rect.y),
                leaf.rect.w,
                leaf.rect.h,
                facecolor=color,
                edgecolor="#202020",
                linewidth=1.2,
                alpha=0.58,
            )
        )
        cx, cy = leaf.rect.center
        ax.text(cx, cy, f"{leaf.rect.w}x{leaf.rect.h}", ha="center", va="center", fontsize=8.5)

    for node in internal_nodes(root):
        ax.add_patch(
            Rectangle(
                (node.rect.x, node.rect.y),
                node.rect.w,
                node.rect.h,
                facecolor="none",
                edgecolor="#111111",
                linewidth=max(0.8, 2.0 - node.depth * 0.22),
            )
        )

    ax.set_xlim(0, root.rect.w)
    ax.set_ylim(root.rect.h, 0)
    ax.text(
        0,
        root.rect.h + 2,
        "Each leaf partition becomes a local design space for a room.",
        fontsize=9.5,
        color="#333333",
    )
    save_figure(fig, output_dir, "01_bsp_partitions")


def draw_rooms_and_corridors(
    root: Node,
    rooms: List[Rect],
    corridors: List[List[Tuple[int, int]]],
    output_dir: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Rooms are placed in leaves and sibling regions are connected", fontsize=13, weight="bold", pad=12)

    for leaf in leaves(root):
        ax.add_patch(
            Rectangle(
                (leaf.rect.x, leaf.rect.y),
                leaf.rect.w,
                leaf.rect.h,
                facecolor="#f8f9fa",
                edgecolor="#b8b8b8",
                linewidth=1,
            )
        )

    for corridor in corridors:
        xs = [cell[0] + 0.5 for cell in corridor]
        ys = [cell[1] + 0.5 for cell in corridor]
        ax.plot(xs, ys, color="#7f5539", linewidth=4.2, solid_capstyle="round", zorder=2)

    for room in rooms:
        ax.add_patch(
            Rectangle(
                (room.x, room.y),
                room.w,
                room.h,
                facecolor="#8ecae6",
                edgecolor="#023047",
                linewidth=1.4,
                zorder=3,
            )
        )

    ax.set_xlim(0, root.rect.w)
    ax.set_ylim(root.rect.h, 0)
    ax.text(
        0,
        root.rect.h + 2,
        "The hierarchy gives a simple recipe for connectivity: connect rooms across each split.",
        fontsize=9.5,
        color="#333333",
    )
    save_figure(fig, output_dir, "02_rooms_and_corridors")


def draw_final_dungeon(grid: List[List[int]], output_dir: Path) -> None:
    colors = ["#1f2933", "#495057", "#d8b26e", "#8b6f47"]
    cmap = ListedColormap(colors)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Rasterized BSP dungeon layout", fontsize=13, weight="bold", pad=12)

    legend = [
        Rectangle((0, 0), 1, 1, facecolor=colors[0], edgecolor="#111111", label="solid wall"),
        Rectangle((0, 0), 1, 1, facecolor=colors[1], edgecolor="#111111", label="wall boundary"),
        Rectangle((0, 0), 1, 1, facecolor=colors[2], edgecolor="#111111", label="room"),
        Rectangle((0, 0), 1, 1, facecolor=colors[3], edgecolor="#111111", label="corridor"),
    ]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=4, frameon=False, fontsize=8.5)
    save_figure(fig, output_dir, "03_final_bsp_dungeon")


def build_bsp(
    width: int,
    height: int,
    seed: int,
    max_depth: int,
    min_leaf_size: int,
) -> Tuple[Node, List[Rect], List[List[Tuple[int, int]]], List[List[int]]]:
    rng = random.Random(seed)
    root = Node(Rect(0, 0, width, height), depth=0)
    split_node(root, rng, max_depth=max_depth, min_leaf_size=min_leaf_size)
    rooms = create_rooms(root, rng)
    corridors = create_corridors(root)
    grid = rasterize(width, height, rooms, corridors)
    return root, rooms, corridors, grid


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=64, help="Map width in tiles.")
    parser.add_argument("--height", type=int, default=42, help="Map height in tiles.")
    parser.add_argument("--seed", type=int, default=12, help="Random seed.")
    parser.add_argument("--max-depth", type=int, default=4, help="Maximum BSP recursion depth.")
    parser.add_argument("--min-leaf-size", type=int, default=10, help="Minimum partition size before splitting.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("figures"))
    args = parser.parse_args()

    root, rooms, corridors, grid = build_bsp(
        width=args.width,
        height=args.height,
        seed=args.seed,
        max_depth=args.max_depth,
        min_leaf_size=args.min_leaf_size,
    )

    draw_partition_tree(root, args.output_dir)
    draw_rooms_and_corridors(root, rooms, corridors, args.output_dir)
    draw_final_dungeon(grid, args.output_dir)

    print(f"Wrote figures to {args.output_dir}")


if __name__ == "__main__":
    main()
