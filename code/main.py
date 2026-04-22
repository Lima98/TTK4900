import argparse
from pathlib import Path

from melody_engine import (
    ChordTonePreferenceConstraint,
    ChoralePlan,
    DirectionChangeConstraint,
    FormPlan,
    FormSection,
    FormSectionConstraint,
    GenerationSettings,
    HarmonyPlan,
    HarmonySpan,
    Key,
    LeapRecoveryConstraint,
    LeadingToneResolutionConstraint,
    MelodyGenerator,
    Motif,
    MotifPreferenceConstraint,
    PhraseCadenceConstraint,
    RepeatedPitchConstraint,
    SingleClimaxConstraint,
    StepwiseMotionConstraint,
    StrongBeatStabilityConstraint,
    TimeSignature,
    VoiceProfile,
    export_melody,
    render_audio_from_midi,
    render_lilypond_file,
)


def build_voice_profile(name: str) -> VoiceProfile:
    profiles = {
        "melody": VoiceProfile("melody", 0, 9, 1, 8),
        "soprano": VoiceProfile("soprano", 0, 9, 1, 8),
        "alto": VoiceProfile("alto", -4, 5, -3, 4),
        "tenor": VoiceProfile("tenor", -8, 1, -7, 0),
        "bass": VoiceProfile("bass", -12, -3, -11, -4),
    }
    if name not in profiles:
        raise ValueError(f"Unsupported voice profile: {name}")
    return profiles[name]


def build_settings(args: argparse.Namespace) -> GenerationSettings:
    key = Key(args.key, args.mode, tonic_octave=args.tonic_octave)
    time_signature = TimeSignature.from_string(args.time_signature)
    voice_profile = build_voice_profile(args.voice_profile)

    range_min = voice_profile.range_min if args.range_min is None else args.range_min
    range_max = voice_profile.range_max if args.range_max is None else args.range_max
    if range_max - range_min > 9:
        raise ValueError("Melodic range may not exceed a major tenth (9 diatonic steps).")

    motif = Motif.from_steps(
        scale_steps=[int(value.strip()) for value in args.motif_steps.split(",") if value.strip()],
        durations=[float(value.strip()) for value in args.motif_durations.split(",") if value.strip()],
        name=args.motif_name,
    )
    if len(motif.events) == 0:
        raise ValueError("Motif must contain at least one note.")

    form_plan = build_form_plan(args.form, args.bars)
    harmony_plan = build_harmony_plan(args.harmony, args.mode, form_plan, args.bars)
    return GenerationSettings(
        key=key,
        time_signature=time_signature,
        bars=args.bars,
        allowed_durations=tuple(float(value.strip()) for value in args.allowed_durations.split(",") if value.strip()),
        range_min=range_min,
        range_max=range_max,
        motif=motif,
        motif_repetition_bar=args.motif_repetition_bar,
        motif_repetition_shift=args.motif_repetition_shift,
        harmonic_plan=harmony_plan,
        phrase_length_bars=args.phrase_length_bars,
        cadence_duration=args.cadence_duration,
        attempts=args.attempts,
        random_seed=args.seed,
        form_plan=form_plan,
        voice_profile=voice_profile,
        chorale_plan=build_future_chorale_plan(),
    )


def build_constraints() -> list:
    return [
        StepwiseMotionConstraint(weight=1.5),
        LeapRecoveryConstraint(weight=1.2),
        LeadingToneResolutionConstraint(weight=1.3),
        ChordTonePreferenceConstraint(weight=1.4),
        StrongBeatStabilityConstraint(weight=1.0),
        PhraseCadenceConstraint(weight=1.6),
        SingleClimaxConstraint(weight=1.5),
        MotifPreferenceConstraint(weight=1.0),
        RepeatedPitchConstraint(weight=1.0),
        DirectionChangeConstraint(weight=0.9),
        FormSectionConstraint(weight=1.0),
    ]


def build_harmony_plan(specification: str, mode: str, form_plan: FormPlan, bars: int) -> HarmonyPlan:
    if specification.strip().lower() in {"", "auto", "none"}:
        return build_default_harmony_plan(mode, form_plan, bars)

    spans: list[HarmonySpan] = []
    for raw_span in specification.split(","):
        chunk = raw_span.strip()
        if not chunk:
            continue

        range_part, roman_symbol, *weight_part = [part.strip() for part in chunk.split(":")]
        start_bar_text, end_bar_text = [part.strip() for part in range_part.split("-")]
        weight = float(weight_part[0]) if weight_part else 1.0
        spans.append(
            HarmonySpan(
                start_bar=int(start_bar_text),
                end_bar=int(end_bar_text),
                roman_symbol=roman_symbol,
                weight=weight,
            )
        )
    if not spans:
        raise ValueError("Harmony plan must contain at least one span.")
    return HarmonyPlan(spans=tuple(spans))


def build_default_harmony_plan(mode: str, form_plan: FormPlan, bars: int) -> HarmonyPlan:
    symbols = default_function_symbols(mode)
    bar_symbols: list[str] = []

    if form_plan.kind == "sentence":
        template = [
            symbols["tonic"],
            symbols["tonic_alt"],
            symbols["predominant"],
            symbols["dominant"],
            symbols["sequence"],
            symbols["predominant"],
            symbols["dominant"],
            symbols["tonic"],
        ]
    elif form_plan.kind == "period":
        template = [
            symbols["tonic"],
            symbols["predominant"],
            symbols["dominant"],
            symbols["dominant"],
            symbols["tonic_alt"],
            symbols["predominant"],
            symbols["dominant"],
            symbols["tonic"],
        ]
    else:
        template = [
            symbols["tonic"],
            symbols["tonic_alt"],
            symbols["predominant"],
            symbols["dominant"],
        ]

    while len(bar_symbols) < bars:
        remaining = bars - len(bar_symbols)
        if remaining >= len(template):
            bar_symbols.extend(template)
        else:
            fallback = [
                symbols["tonic"],
                symbols["predominant"],
                symbols["dominant"],
                symbols["tonic"],
            ]
            bar_symbols.extend(fallback[:remaining])

    spans: list[HarmonySpan] = []
    start_bar = 1
    current_symbol = bar_symbols[0]
    for bar_number in range(2, bars + 1):
        symbol = bar_symbols[bar_number - 1]
        if symbol != current_symbol:
            spans.append(HarmonySpan(start_bar=start_bar, end_bar=bar_number - 1, roman_symbol=current_symbol))
            start_bar = bar_number
            current_symbol = symbol
    spans.append(HarmonySpan(start_bar=start_bar, end_bar=bars, roman_symbol=current_symbol))
    return HarmonyPlan(spans=tuple(spans))


def default_function_symbols(mode: str) -> dict[str, str]:
    if mode.lower() == "minor":
        return {
            "tonic": "i",
            "tonic_alt": "VI",
            "sequence": "III",
            "predominant": "iv",
            "dominant": "V",
        }
    return {
        "tonic": "I",
        "tonic_alt": "vi",
        "sequence": "iii",
        "predominant": "IV",
        "dominant": "V",
    }


def build_form_plan(form_name: str, bars: int) -> FormPlan:
    normalized = form_name.lower()
    if normalized == "auto":
        normalized = "sentence" if bars >= 8 else "phrase"

    sections: list[FormSection] = []

    if normalized == "sentence" and bars >= 8:
        for offset in range(0, bars, 8):
            chunk_start = offset + 1
            chunk_end = min(offset + 8, bars)
            if chunk_end - chunk_start + 1 < 8:
                break
            sections.extend(
                [
                    FormSection(f"basic_idea_{chunk_start}", chunk_start, chunk_start + 1, "basic_idea", source_bar=chunk_start, transform="literal"),
                    FormSection(f"repetition_{chunk_start}", chunk_start + 2, chunk_start + 3, "repetition", source_bar=chunk_start, transform="harmonic_transpose"),
                    FormSection(f"fragmentation_{chunk_start}", chunk_start + 4, chunk_start + 5, "fragmentation", source_bar=chunk_start, transform="fragment"),
                    FormSection(f"cadence_{chunk_start}", chunk_start + 6, chunk_start + 7, "cadence", source_bar=chunk_start, transform="free"),
                ]
            )
        if sections:
            return FormPlan(kind="sentence", sections=tuple(sections))

    if normalized == "period" and bars >= 8:
        for offset in range(0, bars, 8):
            chunk_start = offset + 1
            chunk_end = min(offset + 8, bars)
            if chunk_end - chunk_start + 1 < 8:
                break
            sections.extend(
                [
                    FormSection(f"antecedent_basic_{chunk_start}", chunk_start, chunk_start + 1, "basic_idea", source_bar=chunk_start, transform="literal"),
                    FormSection(f"antecedent_response_{chunk_start}", chunk_start + 2, chunk_start + 3, "continuation", source_bar=chunk_start, transform="period_response"),
                    FormSection(f"consequent_return_{chunk_start}", chunk_start + 4, chunk_start + 5, "repetition", source_bar=chunk_start, transform="harmonic_transpose"),
                    FormSection(f"consequent_cadence_{chunk_start}", chunk_start + 6, chunk_start + 7, "cadence", source_bar=chunk_start, transform="free"),
                ]
            )
        if sections:
            return FormPlan(kind="period", sections=tuple(sections))

    return FormPlan(
        kind="phrase",
        sections=(
            FormSection("opening", 1, min(2, bars), "basic_idea", source_bar=1, transform="literal"),
            FormSection("continuation", min(3, bars), bars, "continuation", source_bar=1, transform="period_response"),
        ),
    )


def build_future_chorale_plan() -> ChoralePlan:
    return ChoralePlan(
        voice_profiles=(
            build_voice_profile("soprano"),
            build_voice_profile("alto"),
            build_voice_profile("tenor"),
            build_voice_profile("bass"),
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate iteration three melodies and optionally render LilyPond/PDF/MIDI/WAV assets."
    )
    parser.add_argument("--key", default="C", help="Tonic note, for example C, Eb, F#.")
    parser.add_argument("--mode", default="major", help="Mode, for example major, minor, dorian.")
    parser.add_argument("--tonic-octave", type=int, default=4, help="Base octave for LilyPond export.")
    parser.add_argument("--voice-profile", default="melody", help="Voice profile: melody, soprano, alto, tenor, bass.")
    parser.add_argument("--time-signature", default="4/4", help="Time signature, for example 4/4 or 3/4.")
    parser.add_argument("--bars", type=int, default=8, help="Number of bars to generate.")
    parser.add_argument(
        "--allowed-durations",
        default="0.5,1.0,2.0",
        help="Comma-separated beat durations that may be used when generating rhythm.",
    )
    parser.add_argument("--range-min", type=int, default=None, help="Lowest allowed diatonic scale step.")
    parser.add_argument("--range-max", type=int, default=None, help="Highest allowed diatonic scale step.")
    parser.add_argument("--phrase-length-bars", type=int, default=4, help="Phrase length in bars.")
    parser.add_argument("--cadence-duration", type=float, default=2.0, help="Cadential note length in beats.")
    parser.add_argument("--attempts", type=int, default=64, help="Number of generation attempts to score.")
    parser.add_argument("--seed", type=int, default=11, help="Random seed for reproducible melodies.")
    parser.add_argument("--form", default="auto", help="Form plan: auto, sentence, period, phrase.")
    parser.add_argument("--motif-steps", default="0,1,2,1", help="Comma-separated motif scale steps.")
    parser.add_argument("--motif-durations", default="1,1,1,1", help="Comma-separated motif durations in beats.")
    parser.add_argument("--motif-name", default="opening_cell", help="Name used for the motif metadata.")
    parser.add_argument(
        "--motif-repetition-bar",
        type=int,
        default=5,
        help="Bar where the motif is reintroduced. Use 0 to let the generator choose.",
    )
    parser.add_argument(
        "--motif-repetition-shift",
        type=int,
        default=1,
        help="Diatonic transposition applied to the repeated motif.",
    )
    parser.add_argument(
        "--harmony",
        default="auto",
        help="Harmony plan as start-end:roman[:weight], separated by commas, or 'auto' for thesis-based progression.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for generated LilyPond and rendered assets. Defaults to code/output/<seed>/.",
    )
    parser.add_argument("--base-name", default="melody", help="Base filename for exported material.")
    parser.add_argument("--with-variants", action="store_true", help="Also export transposed augmentation variants.")
    parser.add_argument("--render", action="store_true", help="Run LilyPond after exporting .ly files.")
    parser.add_argument("--audio", action="store_true", help="Run TiMidity++ to produce .wav files.")
    parser.add_argument("--cropped", action="store_true", help="Ask LilyPond to also emit cropped PDFs.")
    parser.add_argument("--lilypond-bin", default="lilypond", help="Path or command name for LilyPond.")
    parser.add_argument("--timidity-bin", default="timidity", help="Path or command name for TiMidity++.")
    return parser


def describe_melody(settings: GenerationSettings, melody) -> str:
    climax_index = int(melody.metadata.get("climax_index", -1))
    climax_step = int(melody.metadata.get("climax_step", 0))
    motif_targets = melody.metadata.get("motif_targets", {})
    motif_target_count = len(motif_targets) if isinstance(motif_targets, dict) else 0
    section_labels = ", ".join(section.role for section in settings.form_plan.sections) or "free"
    return (
        f"Generated {len(melody.events)} events across {settings.bars} bars in "
        f"{settings.key.tonic} {settings.key.mode} ({settings.time_signature}).\n"
        f"Seed {settings.random_seed}, attempts {settings.attempts}, melodic range "
        f"{settings.range_min}..{settings.range_max}, phrase length {settings.phrase_length_bars} bars, "
        f"voice profile '{settings.voice_profile.name}', form '{settings.form_plan.kind}'.\n"
        f"Motif '{settings.motif.name}' has {len(settings.motif.events)} notes, influenced {motif_target_count} events, "
        f"and form roles are: {section_labels}.\n"
        f"Climax target is event {climax_index} at scale step {climax_step}.\n"
        f"Harmony plan: {', '.join(span.roman_symbol for span in settings.harmonic_plan.spans)}."
    )


def maybe_render(paths: list[Path], args: argparse.Namespace) -> list[Path]:
    if not args.render and not args.audio:
        return []

    generated_assets: list[Path] = []
    for path in paths:
        generated_assets.extend(
            render_lilypond_file(
                path,
                output_dir=path.parent,
                cropped=args.cropped,
                lilypond_bin=args.lilypond_bin,
            )
        )
        if args.audio:
            midi_path = path.with_suffix(".midi")
            if midi_path.exists():
                generated_assets.append(
                    render_audio_from_midi(midi_path, timidity_bin=args.timidity_bin)
                )
    return generated_assets


def main() -> None:
    args = build_parser().parse_args()
    if args.motif_repetition_bar == 0:
        args.motif_repetition_bar = None
    if args.output_dir is None:
        args.output_dir = Path(__file__).resolve().parent / "output" / str(args.seed)

    settings = build_settings(args)
    generator = MelodyGenerator(settings=settings, constraints=build_constraints())
    melody = generator.generate()

    transposed_up = melody.transpose_diatonic(1)
    parallel_in_d = melody.transpose_parallel(Key("D", "major", tonic_octave=4))

    output_directory = args.output_dir
    written_files = [export_melody(melody, output_directory / f"{args.base_name}.ly")]

    if args.with_variants:
        written_files.append(export_melody(transposed_up, output_directory / f"{args.base_name}_diatonic_up.ly"))
        written_files.append(
            export_melody(parallel_in_d, output_directory / f"{args.base_name}_parallel_in_d.ly")
        )

    generated_assets = maybe_render(written_files, args)

    print(describe_melody(settings, melody))
    print(f"Output written to {output_directory.resolve()}")
    print("LilyPond sources:")
    for path in written_files:
        print(f"  - {path.resolve()}")
    if generated_assets:
        print("Rendered assets:")
        for path in generated_assets:
            print(f"  - {path.resolve()}")


if __name__ == "__main__":
    main()
