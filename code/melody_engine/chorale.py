from __future__ import annotations

"""SATB harmonization helpers built on top of the melody generator."""

from dataclasses import dataclass
from itertools import product

from .structure import ChoraleScore, GenerationSettings, Melody, NoteCandidate, NoteEvent, VoiceProfile


@dataclass(frozen=True)
class VoicePitch:
    scale_step: int
    chromatic_adjustment: int
    midi: int


@dataclass(frozen=True)
class Voicing:
    soprano_midi: int
    alto: VoicePitch
    tenor: VoicePitch
    bass: VoicePitch
    score: float


class ChoraleHarmonizer:
    """Create a first-pass SATB realization around a generated soprano melody."""

    def __init__(self, settings: GenerationSettings):
        self.settings = settings
        if len(settings.chorale_plan.voice_profiles) != 4:
            raise ValueError("Chorale harmonization requires soprano, alto, tenor, and bass profiles.")
        self.soprano_profile, self.alto_profile, self.tenor_profile, self.bass_profile = (
            settings.chorale_plan.voice_profiles
        )

    def harmonize(self, soprano: Melody) -> ChoraleScore:
        alto_events: list[NoteEvent] = []
        tenor_events: list[NoteEvent] = []
        bass_events: list[NoteEvent] = []
        previous_voicing: Voicing | None = None

        for index, soprano_event in enumerate(soprano.events):
            if soprano_event.is_rest:
                rest = NoteEvent(scale_step=0, duration=soprano_event.duration, is_rest=True)
                alto_events.append(rest)
                tenor_events.append(rest)
                bass_events.append(rest)
                previous_voicing = None
                continue

            bar_number, beat_in_bar = self._locate_event(soprano.events, index)
            harmony_span = soprano.harmony_plan.chord_for_position(
                bar_number,
                beat_in_bar,
                soprano.time_signature.bar_length,
            )
            roman_symbol = harmony_span.roman_symbol if harmony_span is not None else ("I" if self.settings.key.mode == "major" else "i")

            voicing = self._choose_voicing(
                soprano_event=soprano_event,
                roman_symbol=roman_symbol,
                previous_voicing=previous_voicing,
                beat_in_bar=beat_in_bar,
                is_phrase_end=bar_number in self._phrase_end_bars(),
            )

            alto_events.append(
                NoteEvent(
                    scale_step=voicing.alto.scale_step,
                    chromatic_adjustment=voicing.alto.chromatic_adjustment,
                    duration=soprano_event.duration,
                )
            )
            tenor_events.append(
                NoteEvent(
                    scale_step=voicing.tenor.scale_step,
                    chromatic_adjustment=voicing.tenor.chromatic_adjustment,
                    duration=soprano_event.duration,
                )
            )
            bass_events.append(
                NoteEvent(
                    scale_step=voicing.bass.scale_step,
                    chromatic_adjustment=voicing.bass.chromatic_adjustment,
                    duration=soprano_event.duration,
                )
            )
            previous_voicing = voicing

        alto = Melody(
            key=soprano.key,
            time_signature=soprano.time_signature,
            events=tuple(alto_events),
            harmony_plan=soprano.harmony_plan,
            voice_profile=self.alto_profile,
            metadata={"texture": "chorale", "role": "alto"},
        )
        tenor = Melody(
            key=soprano.key,
            time_signature=soprano.time_signature,
            events=tuple(tenor_events),
            harmony_plan=soprano.harmony_plan,
            voice_profile=self.tenor_profile,
            metadata={"texture": "chorale", "role": "tenor"},
        )
        bass = Melody(
            key=soprano.key,
            time_signature=soprano.time_signature,
            events=tuple(bass_events),
            harmony_plan=soprano.harmony_plan,
            voice_profile=self.bass_profile,
            metadata={"texture": "chorale", "role": "bass"},
        )
        revised_soprano = Melody(
            key=soprano.key,
            time_signature=soprano.time_signature,
            events=soprano.events,
            harmony_plan=soprano.harmony_plan,
            clef=soprano.clef,
            voice_profile=self.soprano_profile,
            metadata={**soprano.metadata, "texture": "chorale", "role": "soprano"},
        )
        return ChoraleScore(
            key=soprano.key,
            time_signature=soprano.time_signature,
            soprano=revised_soprano,
            alto=alto,
            tenor=tenor,
            bass=bass,
            harmony_plan=soprano.harmony_plan,
            metadata={"texture": "chorale"},
        )

    def _choose_voicing(
        self,
        *,
        soprano_event: NoteEvent,
        roman_symbol: str,
        previous_voicing: Voicing | None,
        beat_in_bar: float,
        is_phrase_end: bool,
    ) -> Voicing:
        chord_targets = self.settings.key.chord_scale_targets(roman_symbol)
        soprano_midi = self.settings.key.absolute_midi(
            soprano_event.scale_step,
            soprano_event.chromatic_adjustment,
        )
        alto_candidates = self._voice_candidates(self.alto_profile, chord_targets)
        tenor_candidates = self._voice_candidates(self.tenor_profile, chord_targets)
        bass_candidates = self._voice_candidates(self.bass_profile, chord_targets)

        voicings = self._collect_voicings(
            soprano_event=soprano_event,
            soprano_midi=soprano_midi,
            alto_candidates=alto_candidates,
            tenor_candidates=tenor_candidates,
            bass_candidates=bass_candidates,
            chord_targets=chord_targets,
            roman_symbol=roman_symbol,
            previous_voicing=previous_voicing,
            beat_in_bar=beat_in_bar,
            is_phrase_end=is_phrase_end,
            relaxed=False,
        )
        if not voicings:
            voicings = self._collect_voicings(
                soprano_event=soprano_event,
                soprano_midi=soprano_midi,
                alto_candidates=alto_candidates,
                tenor_candidates=tenor_candidates,
                bass_candidates=bass_candidates,
                chord_targets=chord_targets,
                roman_symbol=roman_symbol,
                previous_voicing=previous_voicing,
                beat_in_bar=beat_in_bar,
                is_phrase_end=is_phrase_end,
                relaxed=True,
            )

        if not voicings:
            raise ValueError(f"Could not find a valid SATB voicing for harmony {roman_symbol}")
        return max(voicings, key=lambda voicing: voicing.score)

    def _collect_voicings(
        self,
        *,
        soprano_event: NoteEvent,
        soprano_midi: int,
        alto_candidates: list[VoicePitch],
        tenor_candidates: list[VoicePitch],
        bass_candidates: list[VoicePitch],
        chord_targets: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
        roman_symbol: str,
        previous_voicing: Voicing | None,
        beat_in_bar: float,
        is_phrase_end: bool,
        relaxed: bool,
    ) -> list[Voicing]:
        voicings: list[Voicing] = []
        soprano_gap = 16 if relaxed else 12
        alto_gap = 14 if relaxed else 12
        bass_gap = 24 if relaxed else 19
        for alto_pitch, tenor_pitch, bass_pitch in product(alto_candidates, tenor_candidates, bass_candidates):
            if relaxed:
                if not (bass_pitch.midi < tenor_pitch.midi <= alto_pitch.midi <= soprano_midi):
                    continue
            else:
                if not (bass_pitch.midi < tenor_pitch.midi < alto_pitch.midi < soprano_midi):
                    continue
            if soprano_midi - alto_pitch.midi > soprano_gap:
                continue
            if alto_pitch.midi - tenor_pitch.midi > alto_gap:
                continue
            if tenor_pitch.midi - bass_pitch.midi > bass_gap:
                continue

            score = self._score_voicing(
                soprano_event=soprano_event,
                soprano_midi=soprano_midi,
                alto_pitch=alto_pitch,
                tenor_pitch=tenor_pitch,
                bass_pitch=bass_pitch,
                chord_targets=chord_targets,
                roman_symbol=roman_symbol,
                previous_voicing=previous_voicing,
                beat_in_bar=beat_in_bar,
                is_phrase_end=is_phrase_end,
            )
            if relaxed:
                score -= 0.8
            voicings.append(
                Voicing(
                    soprano_midi=soprano_midi,
                    alto=alto_pitch,
                    tenor=tenor_pitch,
                    bass=bass_pitch,
                    score=score,
                )
            )
        return voicings

    def _voice_candidates(
        self,
        profile: VoiceProfile,
        chord_targets: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    ) -> list[VoicePitch]:
        candidates: list[VoicePitch] = []
        for scale_step in range(profile.range_min, profile.range_max + 1):
            for chord_degree, adjustment in chord_targets:
                if scale_step % 7 != chord_degree:
                    continue
                midi = self.settings.key.absolute_midi(scale_step, adjustment)
                candidates.append(
                    VoicePitch(
                        scale_step=scale_step,
                        chromatic_adjustment=adjustment,
                        midi=midi,
                    )
                )
        candidates.sort(key=lambda pitch: pitch.midi)
        return candidates

    def _score_voicing(
        self,
        *,
        soprano_event: NoteEvent,
        soprano_midi: int,
        alto_pitch: VoicePitch,
        tenor_pitch: VoicePitch,
        bass_pitch: VoicePitch,
        chord_targets: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
        roman_symbol: str,
        previous_voicing: Voicing | None,
        beat_in_bar: float,
        is_phrase_end: bool,
    ) -> float:
        root_degree, third_degree, fifth_degree = [degree for degree, _ in chord_targets]
        chord_degrees = [
            soprano_event.scale_step % 7,
            alto_pitch.scale_step % 7,
            tenor_pitch.scale_step % 7,
            bass_pitch.scale_step % 7,
        ]

        score = 0.0
        if root_degree in chord_degrees and third_degree in chord_degrees and fifth_degree in chord_degrees:
            score += 3.0
        else:
            score -= 2.5

        root_count = chord_degrees.count(root_degree)
        if root_count >= 2:
            score += 1.2
        if bass_pitch.scale_step % 7 == root_degree:
            score += 1.4
        elif beat_in_bar == 0.0 or is_phrase_end:
            score -= 1.0

        if roman_symbol.strip().lower().startswith("v") and bass_pitch.scale_step % 7 == root_degree:
            score += 0.5

        upper_midis = [alto_pitch.midi, tenor_pitch.midi, bass_pitch.midi]
        preferred_centers = [
            self.settings.key.absolute_midi(self.alto_profile.tessitura_min),
            self.settings.key.absolute_midi(self.tenor_profile.tessitura_min),
            self.settings.key.absolute_midi(self.bass_profile.tessitura_min),
        ]
        for midi, center in zip(upper_midis, preferred_centers):
            score -= abs(midi - center) * 0.04

        if len({soprano_midi, alto_pitch.midi, tenor_pitch.midi, bass_pitch.midi}) < 4:
            score -= 1.5

        if previous_voicing is not None:
            score += self._score_motion(
                soprano_event=soprano_event,
                soprano_midi=soprano_midi,
                alto_pitch=alto_pitch,
                tenor_pitch=tenor_pitch,
                bass_pitch=bass_pitch,
                previous_voicing=previous_voicing,
            )

        return score

    def _score_motion(
        self,
        *,
        soprano_event: NoteEvent,
        soprano_midi: int,
        alto_pitch: VoicePitch,
        tenor_pitch: VoicePitch,
        bass_pitch: VoicePitch,
        previous_voicing: Voicing,
    ) -> float:
        score = 0.0
        current_pitches = [
            (soprano_event.scale_step, soprano_event.chromatic_adjustment, soprano_midi),
            (alto_pitch.scale_step, alto_pitch.chromatic_adjustment, alto_pitch.midi),
            (tenor_pitch.scale_step, tenor_pitch.chromatic_adjustment, tenor_pitch.midi),
            (bass_pitch.scale_step, bass_pitch.chromatic_adjustment, bass_pitch.midi),
        ]
        previous_pitches = [
            (0, 0, previous_voicing.soprano_midi),
            (previous_voicing.alto.scale_step, previous_voicing.alto.chromatic_adjustment, previous_voicing.alto.midi),
            (previous_voicing.tenor.scale_step, previous_voicing.tenor.chromatic_adjustment, previous_voicing.tenor.midi),
            (previous_voicing.bass.scale_step, previous_voicing.bass.chromatic_adjustment, previous_voicing.bass.midi),
        ]

        for index in range(1, 4):
            current = current_pitches[index]
            previous = previous_pitches[index]
            if previous is None:
                continue
            leap = current[2] - previous[2]
            score -= abs(leap) * 0.08
            if abs(leap) > 7:
                score -= 1.5
            elif abs(leap) <= 2:
                score += 0.7

            if self._is_leading_tone(previous[0], previous[1]):
                if current[0] % 7 == 0 and current[1] == 0:
                    score += 1.4
                else:
                    score -= 1.8

        previous_soprano = previous_voicing.soprano_midi
        soprano_motion = soprano_midi - previous_soprano
        for current_voice, previous_voice in (
            (alto_pitch.midi, previous_voicing.alto.midi),
            (tenor_pitch.midi, previous_voicing.tenor.midi),
            (bass_pitch.midi, previous_voicing.bass.midi),
        ):
            motion = current_voice - previous_voice
            if motion == 0:
                score += 0.3
            elif soprano_motion * motion < 0:
                score += 0.5
            else:
                score -= 0.2

        voice_pairs = [
            (soprano_midi, previous_soprano, alto_pitch.midi, previous_voicing.alto.midi),
            (soprano_midi, previous_soprano, tenor_pitch.midi, previous_voicing.tenor.midi),
            (soprano_midi, previous_soprano, bass_pitch.midi, previous_voicing.bass.midi),
            (alto_pitch.midi, previous_voicing.alto.midi, tenor_pitch.midi, previous_voicing.tenor.midi),
            (alto_pitch.midi, previous_voicing.alto.midi, bass_pitch.midi, previous_voicing.bass.midi),
            (tenor_pitch.midi, previous_voicing.tenor.midi, bass_pitch.midi, previous_voicing.bass.midi),
        ]
        for current_upper, previous_upper, current_lower, previous_lower in voice_pairs:
            score += self._parallel_penalty(current_upper, previous_upper, current_lower, previous_lower)

        return score

    def _parallel_penalty(
        self,
        current_upper: int,
        previous_upper: int,
        current_lower: int,
        previous_lower: int,
    ) -> float:
        previous_interval = abs(previous_upper - previous_lower) % 12
        current_interval = abs(current_upper - current_lower) % 12
        upper_motion = current_upper - previous_upper
        lower_motion = current_lower - previous_lower

        if upper_motion == 0 and lower_motion == 0:
            return 0.0
        if upper_motion * lower_motion <= 0:
            return 0.2 if current_interval in {0, 7} else 0.0
        if previous_interval == current_interval == 7:
            return -3.0
        if previous_interval == current_interval == 0:
            return -3.5
        return 0.0

    def _is_leading_tone(self, scale_step: int, chromatic_adjustment: int) -> bool:
        pitch_class = (self.settings.key.scale_pitch_class(scale_step) + chromatic_adjustment) % 12
        leading_tone = (self.settings.key.tonic_pitch_class - 1) % 12
        return pitch_class == leading_tone

    def _locate_event(self, events: tuple[NoteEvent, ...], target_index: int) -> tuple[int, float]:
        bar_length = self.settings.time_signature.bar_length
        bar_number = 1
        beat_in_bar = 0.0
        for index, event in enumerate(events):
            if index == target_index:
                return bar_number, beat_in_bar
            beat_in_bar += event.duration
            if beat_in_bar >= bar_length - 1e-9:
                beat_in_bar = 0.0
                bar_number += 1
        return bar_number, beat_in_bar

    def _phrase_end_bars(self) -> frozenset[int]:
        bars = {
            bar_number
            for bar_number in range(
                self.settings.phrase_length_bars,
                self.settings.bars + 1,
                self.settings.phrase_length_bars,
            )
        }
        bars.add(self.settings.bars)
        return frozenset(bars)
