from __future__ import annotations

"""Generate iteration comparison figures from git history."""

import os
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

LOCAL_CACHE = Path("/tmp/iteration-history-cache")
LOCAL_CACHE.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(LOCAL_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(LOCAL_CACHE))

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = Path(__file__).resolve().parent
END_DATE = date(2026, 5, 8)


@dataclass(frozen=True)
class Snapshot:
    commit: str
    when: date
    label: str
    files: tuple[str, ...] = ()
    prefixes: tuple[str, ...] = ()


ITERATIONS: dict[str, dict[str, object]] = {
    "Iteration 1": {
        "color": "#8c5a2b",
        "done": date(2026, 3, 9),
        "snapshots": (
            Snapshot("ceaab9d", date(2026, 2, 11), "initial proof of concept", files=("code/main.py", "code/melody.py")),
            Snapshot(
                "a40d3cf",
                date(2026, 2, 20),
                "multi-voice version",
                files=("code/main.py", "code/music.py", "code/generator.py", "code/lilyconvert.py", "code/test.py"),
            ),
            Snapshot(
                "6f8eab7",
                date(2026, 2, 24),
                "object refactor",
                files=("code/main.py", "code/core/music.py", "code/generators/generator.py", "code/out/lilypond.py"),
            ),
            Snapshot("0316667", date(2026, 3, 9), "archived as iter1", prefixes=("code/.old_iter1/",)),
        ),
    },
    "Iteration 2": {
        "color": "#2d6a4f",
        "done": date(2026, 4, 6),
        "snapshots": (
            Snapshot(
                "f41ea44",
                date(2026, 3, 19),
                "new motif-based branch",
                files=("code/main.py", "code/music.py", "code/generators.py", "code/constraints.py", "code/lilypond.py"),
            ),
            Snapshot(
                "83425ea",
                date(2026, 3, 29),
                "phrase generator works",
                files=("code/main.py", "code/music.py", "code/generators.py", "code/constraints.py", "code/lilypond.py"),
            ),
            Snapshot(
                "41947da",
                date(2026, 4, 6),
                "output fixes",
                files=("code/main.py", "code/music.py", "code/generators.py", "code/constraints.py", "code/lilypond.py"),
            ),
            Snapshot(
                "6736110",
                date(2026, 4, 6),
                "iteration frozen",
                prefixes=("code/.old_iter2/",),
            ),
        ),
    },
    "Iteration 3": {
        "color": "#3a6ea5",
        "done": END_DATE,
        "snapshots": (
            Snapshot(
                "c071786",
                date(2026, 4, 22),
                "constraint-based engine",
                files=("code/main.py", "code/render_outputs.py"),
                prefixes=("code/melody_engine/",),
            ),
            Snapshot(
                "a1a5339",
                date(2026, 4, 22),
                "voice and clef expansion",
                files=("code/main.py", "code/render_outputs.py"),
                prefixes=("code/melody_engine/",),
            ),
            Snapshot(
                "c480f57",
                date(2026, 5, 5),
                "chorale support",
                files=("code/main.py",),
                prefixes=("code/melody_engine/",),
            ),
            Snapshot(
                "dd680df",
                date(2026, 5, 8),
                "current thesis snapshot",
                files=("code/main.py",),
                prefixes=("code/melody_engine/",),
            ),
        ),
    },
}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def existing_paths(commit: str, paths: Iterable[str]) -> list[str]:
    existing: list[str] = []
    for path in paths:
        try:
            object_type = run_git("cat-file", "-t", f"{commit}:{path}").strip()
        except subprocess.CalledProcessError:
            continue
        if object_type == "blob":
            existing.append(path)
    return existing


def prefixed_paths(commit: str, prefixes: Iterable[str]) -> list[str]:
    tree_paths = run_git("ls-tree", "-r", "--name-only", commit, "code").splitlines()
    matched: list[str] = []
    for path in tree_paths:
        if not path.endswith(".py"):
            continue
        if any(path.startswith(prefix) for prefix in prefixes):
            matched.append(path)
    return matched


def count_nonempty_lines(commit: str, path: str) -> int:
    content = run_git("show", f"{commit}:{path}")
    return sum(1 for line in content.splitlines() if line.strip())


def snapshot_loc(snapshot: Snapshot) -> int:
    paths = existing_paths(snapshot.commit, snapshot.files)
    paths.extend(prefixed_paths(snapshot.commit, snapshot.prefixes))
    unique_paths = sorted(set(paths))
    return sum(count_nonempty_lines(snapshot.commit, path) for path in unique_paths)


def build_history() -> dict[str, list[tuple[date, int, str]]]:
    history: dict[str, list[tuple[date, int, str]]] = {}
    for name, config in ITERATIONS.items():
        points: list[tuple[date, int, str]] = []
        for snapshot in config["snapshots"]:  # type: ignore[index]
            assert isinstance(snapshot, Snapshot)
            points.append((snapshot.when, snapshot_loc(snapshot), snapshot.label))
        history[name] = points
    return history


def plot_iteration_history() -> None:
    history = build_history()
    fig, ax = plt.subplots(figsize=(8.8, 4.8))

    for name, config in ITERATIONS.items():
        color = config["color"]  # type: ignore[index]
        done = config["done"]  # type: ignore[index]
        points = history[name]
        xs = [datetime.combine(day, datetime.min.time()) for day, _, _ in points]
        ys = [value for _, value, _ in points]

        ax.plot(xs, ys, color=color, linewidth=2.2, marker="o", markersize=5, label=name)

        last_day, last_value, _ = points[-1]
        if done < END_DATE:
            ax.plot(
                [
                    datetime.combine(done, datetime.min.time()),
                    datetime.combine(END_DATE, datetime.min.time()),
                ],
                [last_value, last_value],
                color=color,
                linewidth=2.0,
                linestyle="--",
            )

    # ax.set_title("Growth of the three iterations over time", fontsize=12, pad=10)
    ax.set_ylabel("Non-empty Python LOC",fontsize=14)
    ax.set_xlabel("Date", fontsize=14)
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=14)
    fig.autofmt_xdate()
    fig.tight_layout(rect=(0, 0, 0.86, 1))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / "iteration_loc_history.pdf", bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "iteration_loc_history.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    lines = ["Iteration comparison data:"]
    for name, points in history.items():
        summary = ", ".join(f"{day.isoformat()}={value}" for day, value, _ in points)
        lines.append(f"{name}: {summary}")
    (OUTPUT_DIR / "iteration_loc_history.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    plot_iteration_history()
