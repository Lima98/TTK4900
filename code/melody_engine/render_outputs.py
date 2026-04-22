from __future__ import annotations

import argparse
from pathlib import Path

from .lilypond import render_sources

DEFAULT_TARGET = Path(__file__).resolve().parents[1] / "output"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render LilyPond files to cropped PDF/MIDI and optional WAV."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=DEFAULT_TARGET,
        type=Path,
        help="A .ly file or a directory containing .ly files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional output directory. Defaults to the same directory as the source files.",
    )
    parser.add_argument("--pdf", action="store_true", help="Render cropped PDF output with LilyPond.")
    parser.add_argument("--wav", action="store_true", help="Render WAV output with TiMidity++.")
    parser.add_argument("--lilypond-bin", default="lilypond", help="Path or command name for LilyPond.")
    parser.add_argument("--timidity-bin", default="timidity", help="Path or command name for TiMidity++.")
    return parser


def collect_sources(target: Path) -> list[Path]:
    if target.is_file():
        if target.suffix != ".ly":
            raise ValueError(f"Expected a .ly file, got {target}")
        return [target]
    if not target.exists():
        raise FileNotFoundError(f"Target does not exist: {target}")
    return sorted(target.glob("*.ly"))


def main() -> None:
    args = build_parser().parse_args()
    sources = collect_sources(args.target)
    if not sources:
        raise FileNotFoundError(f"No LilyPond files found in {args.target}")

    rendered_assets = render_sources(
        sources,
        output_dir=args.output_dir,
        pdf=args.pdf,
        wav=args.wav,
        lilypond_bin=args.lilypond_bin,
        timidity_bin=args.timidity_bin,
    )

    print(f"Processed {len(sources)} LilyPond file(s).")
    for asset in rendered_assets:
        print(f"  - {asset.resolve()}")


if __name__ == "__main__":
    main()
