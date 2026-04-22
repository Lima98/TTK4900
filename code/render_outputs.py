import argparse
from pathlib import Path

from melody_engine import render_audio_from_midi, render_lilypond_file


DEFAULT_TARGET = Path(__file__).resolve().parent / "output" / "iter3"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render LilyPond files to PDF/MIDI and optionally WAV using TiMidity++."
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
    parser.add_argument("--audio", action="store_true", help="Also convert generated MIDI files to WAV.")
    parser.add_argument("--cropped", action="store_true", help="Ask LilyPond to also emit cropped PDFs.")
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

    rendered_assets: list[Path] = []
    for source in sources:
        output_dir = args.output_dir or source.parent
        rendered_assets.extend(
            render_lilypond_file(
                source,
                output_dir=output_dir,
                cropped=args.cropped,
                lilypond_bin=args.lilypond_bin,
            )
        )
        if args.audio:
            midi_path = output_dir / f"{source.stem}.midi"
            if midi_path.exists():
                rendered_assets.append(
                    render_audio_from_midi(midi_path, timidity_bin=args.timidity_bin)
                )

    print(f"Processed {len(sources)} LilyPond file(s).")
    for asset in rendered_assets:
        print(f"  - {asset.resolve()}")


if __name__ == "__main__":
    main()
