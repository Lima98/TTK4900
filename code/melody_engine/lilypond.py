from __future__ import annotations

import subprocess
from pathlib import Path

from .structure import Melody

BEAT_TO_DURATION = {
    4.0: "1",
    2.0: "2",
    1.0: "4",
    0.5: "8",
    0.25: "16",
}


def lilypond_duration(duration: float) -> str:
    if duration not in BEAT_TO_DURATION:
        raise ValueError(f"Unsupported duration for LilyPond export: {duration}")
    return BEAT_TO_DURATION[duration]


def melody_to_lilypond_source(melody: Melody) -> str:
    key_name = melody.key.tonic.lower().replace("b", "f")
    note_tokens = [
        f"{melody.key.chromatic_pitch(event.scale_step, event.chromatic_adjustment)}{lilypond_duration(event.duration)}"
        for event in melody.events
    ]

    bar_length = melody.time_signature.bar_length
    bars: list[str] = []
    current_bar: list[str] = []
    beat_total = 0.0

    for token, event in zip(note_tokens, melody.events):
        current_bar.append(token)
        beat_total += event.duration
        if beat_total >= bar_length - 1e-9:
            bars.append(" ".join(current_bar))
            current_bar = []
            beat_total = 0.0

    if current_bar:
        bars.append(" ".join(current_bar))

    music_body = " |\n    ".join(bars)

    return f"""\\version "2.24.4"
\\language "english"

\\score {{
  \\new Staff {{
    \\clef "treble_8"
    \\key {key_name} \\{melody.key.mode}
    \\time {melody.time_signature}
    {music_body} \\bar "|."
  }}
  \\layout {{}}
  \\midi {{}}
}}
"""


def export_melody(melody: Melody, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(melody_to_lilypond_source(melody), encoding="utf-8")
    return path


def render_lilypond_file(
    source_path: str | Path,
    output_dir: str | Path | None = None,
    *,
    cropped: bool = False,
    lilypond_bin: str = "lilypond",
) -> list[Path]:
    source = Path(source_path)
    render_dir = Path(output_dir) if output_dir is not None else source.parent
    render_dir.mkdir(parents=True, exist_ok=True)

    command = [lilypond_bin, "-o", str(render_dir)]
    if cropped:
        command.append("-dcrop")
    command.append(str(source))

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Could not find LilyPond binary '{lilypond_bin}'. Install LilyPond or pass --lilypond-bin."
        ) from error

    base_name = source.stem
    generated = [
        render_dir / f"{base_name}.pdf",
        render_dir / f"{base_name}.midi",
    ]
    if cropped:
        generated.append(render_dir / f"{base_name}.cropped.pdf")
    return [path for path in generated if path.exists()]


def render_audio_from_midi(
    midi_path: str | Path,
    wav_path: str | Path | None = None,
    *,
    timidity_bin: str = "timidity",
) -> Path:
    midi_file = Path(midi_path)
    audio_file = Path(wav_path) if wav_path is not None else midi_file.with_suffix(".wav")

    try:
        subprocess.run(
            [timidity_bin, str(midi_file), "-Ow", "-o", str(audio_file)],
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            f"Could not find TiMidity++ binary '{timidity_bin}'. Install TiMidity++ or pass --timidity-bin."
        ) from error

    return audio_file
