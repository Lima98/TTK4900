from __future__ import annotations

import random
from dataclasses import dataclass
from math import exp

from .constraints import CandidateContext, SoftConstraint
from .structure import FormPlan, FormSection, GenerationSettings, Melody, Motif, NoteCandidate, NoteEvent


@dataclass(frozen=True)
class GenerationAttempt:
    events: tuple[NoteEvent, ...]
    score: float


class MelodyGenerator:
    def __init__(self, settings: GenerationSettings, constraints: list[SoftConstraint]):
        self.settings = settings
        self.constraints = constraints
        self.random = random.Random(settings.random_seed)

    def generate(self) -> Melody:
        rhythm = self._build_rhythm()
        motif_targets = self._build_motif_targets(rhythm)
        climax_index = self._select_climax_index(rhythm)
        climax_step = min(self.settings.range_max, max(self.settings.range_min + 4, 7))

        attempts: list[GenerationAttempt] = []
        for _ in range(self.settings.attempts):
            events, score = self._generate_attempt(rhythm, motif_targets, climax_index, climax_step)
            attempts.append(GenerationAttempt(events=events, score=score))

        best_attempt = max(attempts, key=lambda attempt: attempt.score)
        metadata = {
            "climax_index": climax_index,
            "climax_step": climax_step,
            "motif_targets": motif_targets,
            "form_kind": self.settings.form_plan.kind,
            "form_sections": self.settings.form_plan.sections,
        }
        return Melody(
            key=self.settings.key,
            time_signature=self.settings.time_signature,
            events=best_attempt.events,
            harmony_plan=self.settings.harmonic_plan,
            voice_profile=self.settings.voice_profile,
            metadata=metadata,
        )

    def _generate_attempt(
        self,
        rhythm: list[float],
        motif_targets: dict[int, int],
        climax_index: int,
        climax_step: int,
    ) -> tuple[tuple[NoteEvent, ...], float]:
        events: list[NoteEvent] = []
        total_score = 0.0
        beat_positions = self._beat_positions(rhythm)
        phrase_end_bars = self._phrase_end_bars()

        for index, duration in enumerate(rhythm):
            bar_number, beat_in_bar = beat_positions[index]
            harmony_span = self.settings.harmonic_plan.chord_for_bar(bar_number)
            motif_target_step = motif_targets.get(index)
            section = self.settings.form_plan.section_for_bar(bar_number)
            context = CandidateContext(
                key=self.settings.key,
                events=tuple(events),
                index=index,
                bar_number=bar_number,
                beat_in_bar=beat_in_bar,
                total_events=len(rhythm),
                climax_index=climax_index,
                climax_step=climax_step,
                phrase_end_bars=phrase_end_bars,
                harmony_span=harmony_span,
                motif_target_step=motif_target_step,
                section_role=section.role if section is not None else "free",
                section_transform=section.transform if section is not None else "free",
            )
            candidate_steps = self._candidate_steps(
                events,
                index,
                climax_index,
                climax_step,
                motif_target_step,
                context,
            )
            chosen_note, chosen_score = self._choose_candidate(candidate_steps, context)
            events.append(
                NoteEvent(
                    scale_step=chosen_note.scale_step,
                    duration=duration,
                    chromatic_adjustment=chosen_note.chromatic_adjustment,
                )
            )
            total_score += chosen_score

        return tuple(events), total_score

    def _build_rhythm(self) -> list[float]:
        rhythm: list[float] = []
        bar_length = self.settings.time_signature.bar_length
        cadence_duration = min(self.settings.cadence_duration, bar_length)
        phrase_end_bars = self._phrase_end_bars()

        for bar_number in range(1, self.settings.bars + 1):
            bar_rhythm: list[float] = []
            remaining = bar_length
            reserve_cadence = cadence_duration if bar_number in phrase_end_bars else 0.0

            while remaining - reserve_cadence > 0:
                choices = [
                    duration
                    for duration in self.settings.allowed_durations
                    if duration <= remaining - reserve_cadence + 1e-9
                ]
                chosen_duration = self.random.choice(choices)
                bar_rhythm.append(chosen_duration)
                remaining -= chosen_duration

            if reserve_cadence:
                bar_rhythm.append(reserve_cadence)
                remaining -= reserve_cadence

            if abs(remaining) > 1e-9:
                raise ValueError(f"Bar {bar_number} could not be filled exactly")

            rhythm.extend(bar_rhythm)

        return rhythm

    def _build_motif_targets(self, rhythm: list[float]) -> dict[int, int]:
        motif = self.settings.motif or self._default_motif()
        motif_targets: dict[int, int] = {}

        for section in self.settings.form_plan.sections:
            transformed_motif = self._motif_for_section(motif, section)
            start_index = self._first_index_of_bar(rhythm, section.start_bar)
            if start_index is None:
                continue
            self._write_motif_targets(rhythm, motif_targets, start_index, transformed_motif)

            if section.role == "fragmentation":
                repeat_bar = section.start_bar + 1
                if repeat_bar <= section.end_bar:
                    repeat_index = self._first_index_of_bar(rhythm, repeat_bar)
                    if repeat_index is not None:
                        repeated_fragment = self._motif_for_section(
                            motif,
                            FormSection(
                                label=section.label,
                                start_bar=repeat_bar,
                                end_bar=repeat_bar,
                                role=section.role,
                                source_bar=section.source_bar,
                                transform="sequence_fragment",
                            ),
                        )
                        self._write_motif_targets(rhythm, motif_targets, repeat_index, repeated_fragment)

        return motif_targets

    def _default_motif(self) -> Motif:
        return Motif.from_steps(
            scale_steps=[0, 1, 2, 1],
            durations=[1.0, 1.0, 1.0, 1.0],
            name="default_motif",
        )

    def _motif_for_section(self, motif: Motif, section: FormSection) -> Motif:
        transform = section.transform
        if transform == "literal":
            return motif

        if transform == "diatonic_transpose":
            return motif.transpose_diatonic(self.settings.motif_repetition_shift)

        if transform == "harmonic_transpose":
            span = self.settings.harmonic_plan.chord_for_bar(section.start_bar)
            if span is None:
                return motif
            target_degree = self.settings.key.chord_tones(span.roman_symbol)[0]
            anchor = self._nearest_step_with_degree(motif.events[0].scale_step, target_degree)
            return motif.transpose_diatonic(anchor - motif.events[0].scale_step)

        if transform in {"fragment", "sequence_fragment"}:
            count = max(2, len(motif.events) // 2)
            fragment = Motif(events=motif.events[:count], name=f"{motif.name}_fragment")
            if transform == "sequence_fragment":
                shift = self.random.choice((-2, -1, 1, 2))
                return fragment.transpose_diatonic(shift)
            return fragment

        if transform == "period_response":
            shift = self.random.choice((0, 1, -1, 2))
            return motif.transpose_diatonic(shift)

        return motif

    def _write_motif_targets(
        self,
        rhythm: list[float],
        motif_targets: dict[int, int],
        start_index: int,
        motif: Motif,
    ) -> None:
        for offset, event in enumerate(motif.events):
            event_index = start_index + offset
            if event_index >= len(rhythm):
                break
            if abs(rhythm[event_index] - event.duration) < 1e-9:
                motif_targets[event_index] = event.scale_step

    def _nearest_step_with_degree(self, reference_step: int, target_degree: int) -> int:
        octave_base = reference_step // 7
        candidates = [target_degree + 7 * octave for octave in range(octave_base - 1, octave_base + 2)]
        valid = [
            candidate
            for candidate in candidates
            if self.settings.range_min <= candidate <= self.settings.range_max
        ]
        if not valid:
            return min(
                max(target_degree + 7 * octave_base, self.settings.range_min),
                self.settings.range_max,
            )
        return min(valid, key=lambda candidate: abs(candidate - reference_step))

    def _first_index_of_bar(self, rhythm: list[float], target_bar: int) -> int | None:
        bar_length = self.settings.time_signature.bar_length
        running = 0.0
        current_bar = 1

        for index, duration in enumerate(rhythm):
            if current_bar == target_bar and abs(running) < 1e-9:
                return index
            running += duration
            if running >= bar_length - 1e-9:
                running = 0.0
                current_bar += 1

        return None

    def _select_climax_index(self, rhythm: list[float]) -> int:
        lower_bound = max(2, int(len(rhythm) * 0.55))
        upper_bound = max(lower_bound + 1, int(len(rhythm) * 0.75))
        strong_beats = [
            index
            for index, (_, beat_in_bar) in enumerate(self._beat_positions(rhythm))
            if index >= lower_bound and index <= upper_bound and beat_in_bar in {0.0, 1.0, 2.0}
        ]
        if strong_beats:
            return self.random.choice(strong_beats)
        return min(len(rhythm) - 2, upper_bound)

    def _phrase_end_bars(self) -> frozenset[int]:
        phrase_end_bars = {
            bar_number
            for bar_number in range(self.settings.phrase_length_bars, self.settings.bars + 1, self.settings.phrase_length_bars)
        }
        phrase_end_bars.add(self.settings.bars)
        return frozenset(phrase_end_bars)

    def _beat_positions(self, rhythm: list[float]) -> list[tuple[int, float]]:
        positions: list[tuple[int, float]] = []
        bar_length = self.settings.time_signature.bar_length
        bar_number = 1
        beat_in_bar = 0.0

        for duration in rhythm:
            positions.append((bar_number, beat_in_bar))
            beat_in_bar += duration
            if beat_in_bar >= bar_length - 1e-9:
                beat_in_bar = 0.0
                bar_number += 1

        return positions

    def _candidate_steps(
        self,
        events: list[NoteEvent],
        index: int,
        climax_index: int,
        climax_step: int,
        motif_target_step: int | None,
        context: CandidateContext,
    ) -> list[NoteCandidate]:
        if index == 0:
            seed_steps = [0, 2, 4]
        else:
            previous_step = events[-1].scale_step
            seed_steps = [
                previous_step + interval
                for interval in (-4, -3, -2, -1, 0, 1, 2, 3, 4)
            ]

        if motif_target_step is not None:
            seed_steps.extend([motif_target_step - 1, motif_target_step, motif_target_step + 1])

        if index == climax_index:
            seed_steps.extend([climax_step - 1, climax_step, climax_step + 1])

        seed_steps.append(self.settings.range_min)
        seed_steps.append(self.settings.range_max)

        diatonic_steps = sorted({
            step
            for step in seed_steps
            if self.settings.range_min <= step <= self.settings.range_max
        })

        candidates = {NoteCandidate(scale_step=step, chromatic_adjustment=0) for step in diatonic_steps}

        if context.harmony_span is not None:
            chord_targets = self.settings.key.chord_scale_targets(context.harmony_span.roman_symbol)
            for step in diatonic_steps:
                step_degree = step % 7
                for chord_degree, adjustment in chord_targets:
                    if step_degree == chord_degree:
                        candidates.add(NoteCandidate(scale_step=step, chromatic_adjustment=adjustment))

        return sorted(candidates, key=lambda candidate: (candidate.scale_step, candidate.chromatic_adjustment))

    def _choose_candidate(
        self,
        candidate_steps: list[NoteCandidate],
        context: CandidateContext,
    ) -> tuple[NoteCandidate, float]:
        scored_candidates = []

        for candidate_step in candidate_steps:
            total = 0.0
            for constraint in self.constraints:
                total += constraint.weight * constraint.evaluate(candidate_step, context)
            scored_candidates.append((candidate_step, total))

        best_score = max(score for _, score in scored_candidates)
        temperature = 1.15
        weights = [exp((score - best_score) / temperature) for _, score in scored_candidates]
        chosen_step, chosen_score = self.random.choices(scored_candidates, weights=weights, k=1)[0]
        return chosen_step, chosen_score
