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


def choose_clef(melody: Melody) -> str:
    if melody.clef is not None:
        return melody.clef

    voice_name = melody.voice_profile.name.lower()
    if voice_name.startswith("tenor"):
        return "treble_8"
    if voice_name.startswith("bass"):
        return "bass"
    if voice_name.startswith("alto") or voice_name.startswith("soprano"):
        return "treble"
    if melody.voice_profile.clef_hint is not None:
        return melody.voice_profile.clef_hint

    pitched = melody.pitched_events
    if not pitched:
        return "treble"

    midi_values = [
        melody.key.absolute_midi(event.scale_step, event.chromatic_adjustment)
        for event in pitched
    ]
    average_midi = sum(midi_values) / len(midi_values)
    lowest_midi = min(midi_values)
    highest_midi = max(midi_values)
    low_share = sum(1 for value in midi_values if value < 60) / len(midi_values)

    if average_midi < 50 or highest_midi <= 59:
        return "bass"
    if melody.key.tonic_octave <= 3 and low_share >= 0.5 and highest_midi <= 69:
        return "treble_8"
    return "treble"


def melody_to_lilypond_source(melody: Melody) -> str:
    key_name = melody.key.tonic.lower().replace("b", "f")
    note_tokens = [
        (
            f"r{lilypond_duration(event.duration)}"
            if event.is_rest
            else f"{melody.key.chromatic_pitch(event.scale_step, event.chromatic_adjustment)}{lilypond_duration(event.duration)}"
        )
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
    \\clef "{choose_clef(melody)}"
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


def render_sources(
    sources: list[Path],
    *,
    output_dir: Path | None = None,
    pdf: bool = False,
    wav: bool = False,
    lilypond_bin: str = "lilypond",
    timidity_bin: str = "timidity",
) -> list[Path]:
    rendered_assets: list[Path] = []
    if not pdf and not wav:
        return rendered_assets

    for source in sources:
        source_output_dir = output_dir or source.parent
        rendered_assets.extend(
            render_lilypond_file(
                source,
                output_dir=source_output_dir,
                cropped=True,
                lilypond_bin=lilypond_bin,
            )
        )
        if wav:
            midi_path = source_output_dir / f"{source.stem}.midi"
            if midi_path.exists():
                rendered_assets.append(
                    render_audio_from_midi(midi_path, timidity_bin=timidity_bin)
                )
    return rendered_assets
