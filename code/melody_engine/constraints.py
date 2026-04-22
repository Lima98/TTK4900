from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .structure import HarmonySpan, NoteCandidate, NoteEvent
from .theory import Key


@dataclass(frozen=True)
class CandidateContext:
    key: Key
    events: tuple[NoteEvent, ...]
    index: int
    bar_number: int
    beat_in_bar: float
    total_events: int
    climax_index: int
    climax_step: int
    phrase_end_bars: frozenset[int]
    current_duration: float
    harmony_span: HarmonySpan | None = None
    motif_target_step: int | None = None
    section_role: str = "free"
    section_transform: str = "free"

    @property
    def previous_event(self) -> NoteEvent | None:
        if self.index == 0:
            return None
        return self.events[self.index - 1]

    @property
    def previous_interval(self) -> int | None:
        if self.index < 2:
            return None
        return self.events[self.index - 1].scale_step - self.events[self.index - 2].scale_step

    @property
    def previous_pitched_event(self) -> NoteEvent | None:
        for event in reversed(self.events):
            if not event.is_rest:
                return event
        return None

    @property
    def previous_pitched_interval(self) -> int | None:
        pitched = [event for event in self.events if not event.is_rest]
        if len(pitched) < 2:
            return None
        return pitched[-1].scale_step - pitched[-2].scale_step

    @property
    def notes_since_last_rest(self) -> int:
        count = 0
        for event in reversed(self.events):
            if event.is_rest:
                break
            count += 1
        return count

    @property
    def candidate_is_final(self) -> bool:
        return self.index == self.total_events - 1

    @property
    def on_strong_beat(self) -> bool:
        return self.beat_in_bar in {0.0, 2.0}


class SoftConstraint(Protocol):
    name: str
    weight: float

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        ...


@dataclass(frozen=True)
class StepwiseMotionConstraint:
    weight: float = 1.0
    name: str = "stepwise_motion"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return 0.0

        previous_event = context.previous_pitched_event
        candidate_step = candidate.scale_step
        if previous_event is None:
            return 0.6 if candidate_step in {0, 2, 4} else 0.0

        distance = abs(candidate_step - previous_event.scale_step)
        if distance == 0:
            return 0.2
        if distance == 1:
            return 1.5
        if distance == 2:
            return 1.0
        if distance == 3:
            return -0.3
        if distance == 4:
            return -1.0
        return -2.3


@dataclass(frozen=True)
class LeapRecoveryConstraint:
    weight: float = 1.0
    name: str = "leap_recovery"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return -0.4 if context.previous_pitched_interval is not None and abs(context.previous_pitched_interval) >= 4 else 0.0

        previous_interval = context.previous_pitched_interval
        previous_event = context.previous_pitched_event
        candidate_step = candidate.scale_step
        if previous_interval is None or previous_event is None:
            return 0.0

        if abs(previous_interval) < 4:
            return 0.0

        current_interval = candidate_step - previous_event.scale_step
        if current_interval == 0:
            return -0.5

        if abs(current_interval) <= 2 and current_interval * previous_interval < 0:
            return 2.2

        if current_interval * previous_interval > 0:
            return -2.0

        return -0.6


@dataclass(frozen=True)
class LeadingToneResolutionConstraint:
    weight: float = 1.0
    name: str = "leading_tone_resolution"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        previous_event = context.previous_pitched_event
        candidate_step = candidate.scale_step
        if previous_event is None:
            return 0.0

        if candidate.is_rest:
            return -1.2 if previous_event.scale_step % 7 == 6 else 0.0

        if previous_event.scale_step % 7 != 6:
            return 0.0

        if candidate_step == previous_event.scale_step + 1:
            return 2.5

        if candidate_step == previous_event.scale_step:
            return -1.2

        return -2.5


@dataclass(frozen=True)
class ChordTonePreferenceConstraint:
    weight: float = 1.0
    non_chord_tone_penalty: float = -0.35
    name: str = "chord_tone_preference"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if context.harmony_span is None:
            return 0.0

        if candidate.is_rest:
            return -0.9 if context.on_strong_beat else -0.1

        chord_pitch_classes = context.key.chord_pitch_classes(context.harmony_span.roman_symbol)
        candidate_pitch_class = (
            context.key.scale_pitch_class(candidate.scale_step) + candidate.chromatic_adjustment
        ) % 12
        if candidate_pitch_class in chord_pitch_classes:
            return 1.6 * context.harmony_span.weight

        if context.on_strong_beat:
            return self.non_chord_tone_penalty * 2 * context.harmony_span.weight

        return self.non_chord_tone_penalty * context.harmony_span.weight


@dataclass(frozen=True)
class StrongBeatStabilityConstraint:
    weight: float = 1.0
    name: str = "strong_beat_stability"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if not context.on_strong_beat:
            return 0.0

        if candidate.is_rest:
            return -1.2

        candidate_step = candidate.scale_step
        degree = candidate_step % 7
        if degree in {0, 2, 4}:
            return 0.9
        if degree == 6:
            return -0.6
        return 0.1


@dataclass(frozen=True)
class PhraseCadenceConstraint:
    weight: float = 1.0
    name: str = "phrase_cadence"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if context.bar_number not in context.phrase_end_bars:
            return 0.0

        if candidate.is_rest:
            if context.candidate_is_final:
                return -6.0
            if context.beat_in_bar >= 2.0 and context.current_duration <= 0.5:
                return 0.3
            return -1.0

        candidate_step = candidate.scale_step
        if context.candidate_is_final:
            if candidate_step % 7 == 0 and candidate.chromatic_adjustment == 0:
                return 5.0
            if candidate_step % 7 == 4:
                return 1.5
            return -3.5

        if context.beat_in_bar >= 2.0:
            if candidate_step % 7 in {0, 4}:
                return 1.0
            if candidate_step % 7 == 6:
                return -1.4

        return 0.0


@dataclass(frozen=True)
class SingleClimaxConstraint:
    weight: float = 1.0
    name: str = "single_climax"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return -4.0 if context.index == context.climax_index else -0.2

        candidate_step = candidate.scale_step
        if context.index < context.climax_index:
            if candidate_step > context.climax_step:
                return -4.5
            if candidate_step == context.climax_step:
                return -2.0
            return 0.0

        if context.index == context.climax_index:
            if candidate_step == context.climax_step:
                return 6.0
            if candidate_step == context.climax_step - 1:
                return 1.5
            return -3.0

        if candidate_step >= context.climax_step:
            return -5.0
        if candidate_step == context.climax_step - 1:
            return -1.0
        return 0.0


@dataclass(frozen=True)
class MotifPreferenceConstraint:
    weight: float = 1.0
    name: str = "motif_preference"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if context.motif_target_step is None:
            return 0.0
        if candidate.is_rest:
            return -2.0
        candidate_step = candidate.scale_step
        if candidate_step == context.motif_target_step:
            return 3.5 if candidate.chromatic_adjustment == 0 else 2.0
        if abs(candidate_step - context.motif_target_step) == 1:
            return 0.4
        return -1.5


@dataclass(frozen=True)
class RepeatedPitchConstraint:
    weight: float = 1.0
    name: str = "repeated_pitch_control"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return 0.0

        previous_event = context.previous_pitched_event
        if previous_event is None:
            return 0.0

        same_pitch = (
            previous_event.scale_step == candidate.scale_step
            and previous_event.chromatic_adjustment == candidate.chromatic_adjustment
        )
        if not same_pitch:
            return 0.0

        pitched = [event for event in context.events if not event.is_rest]
        if len(pitched) >= 2:
            second_previous = pitched[-2]
            if (
                second_previous.scale_step == candidate.scale_step
                and second_previous.chromatic_adjustment == candidate.chromatic_adjustment
            ):
                return -2.2
        return -0.5


@dataclass(frozen=True)
class DirectionChangeConstraint:
    weight: float = 1.0
    name: str = "direction_change"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return 0.0

        previous_interval = context.previous_pitched_interval
        previous_event = context.previous_pitched_event
        if previous_interval is None or previous_event is None:
            return 0.0

        current_interval = candidate.scale_step - previous_event.scale_step
        if current_interval == 0:
            return -0.2

        if abs(previous_interval) <= 1:
            return 0.0

        if current_interval * previous_interval < 0:
            return 1.0
        if current_interval * previous_interval > 0 and abs(current_interval) >= 2:
            return -0.7
        return 0.0


@dataclass(frozen=True)
class LargeLeapConstraint:
    weight: float = 1.0
    name: str = "large_leap"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if candidate.is_rest:
            return 0.0

        previous_event = context.previous_pitched_event
        if previous_event is None:
            return 0.0

        distance = abs(candidate.scale_step - previous_event.scale_step)
        if distance <= 3:
            return 0.0
        if distance == 4:
            return -1.5
        if distance == 5:
            return -3.5
        if distance == 6:
            return -5.0
        return -7.0


@dataclass(frozen=True)
class RestConstraint:
    weight: float = 1.0
    name: str = "rest_usage"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        if not candidate.is_rest:
            return 0.0

        if context.index == 0 or context.candidate_is_final:
            return -5.0
        if context.current_duration > 1.0:
            return -3.5
        if context.on_strong_beat:
            return -1.8
        if context.previous_event is not None and context.previous_event.is_rest:
            return -3.0

        score = -0.5
        if context.notes_since_last_rest >= 6:
            score += 1.4
        if context.bar_number in context.phrase_end_bars and context.beat_in_bar >= 2.0:
            score += 0.7
        return score


@dataclass(frozen=True)
class FormSectionConstraint:
    weight: float = 1.0
    name: str = "form_section"

    def evaluate(self, candidate: NoteCandidate, context: CandidateContext) -> float:
        role = context.section_role
        if role == "basic_idea":
            if context.on_strong_beat and candidate.scale_step % 7 in {0, 2, 4}:
                return 0.7
            return 0.0

        if role == "repetition":
            if context.motif_target_step is not None and abs(candidate.scale_step - context.motif_target_step) <= 1:
                return 0.9
            return -0.1 if context.on_strong_beat and candidate.scale_step % 7 == 6 else 0.0

        if role == "fragmentation":
            previous_event = context.previous_event
            if previous_event is None:
                return 0.0
            interval = abs(candidate.scale_step - previous_event.scale_step)
            if interval <= 2:
                return 0.8
            return -0.4

        if role == "continuation":
            previous_event = context.previous_event
            if previous_event is None:
                return 0.0
            interval = abs(candidate.scale_step - previous_event.scale_step)
            if interval in {1, 2}:
                return 0.5
            return 0.0

        if role == "cadence":
            if context.candidate_is_final and candidate.scale_step % 7 == 0 and candidate.chromatic_adjustment == 0:
                return 1.5
            if context.on_strong_beat and candidate.scale_step % 7 in {4, 6}:
                return 0.4
            return 0.0

        return 0.0
