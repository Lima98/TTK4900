from __future__ import annotations

"""Core immutable data structures for melody generation, form, harmony, and voice ranges."""

from dataclasses import dataclass, field, replace

from .theory import Key


@dataclass(frozen=True)
class TimeSignature:
    beats_per_bar: int
    beat_unit: int

    @classmethod
    def from_string(cls, value: str) -> "TimeSignature":
        beats_per_bar, beat_unit = value.split("/")
        return cls(beats_per_bar=int(beats_per_bar), beat_unit=int(beat_unit))

    @property
    def bar_length(self) -> float:
        return self.beats_per_bar * (4 / self.beat_unit)

    def __str__(self) -> str:
        return f"{self.beats_per_bar}/{self.beat_unit}"


@dataclass(frozen=True)
class NoteEvent:
    scale_step: int
    duration: float
    chromatic_adjustment: int = 0
    is_rest: bool = False

    def transpose_diatonic(self, step_shift: int) -> "NoteEvent":
        if self.is_rest:
            return self
        return replace(self, scale_step=self.scale_step + step_shift)


@dataclass(frozen=True)
class NoteCandidate:
    scale_step: int
    chromatic_adjustment: int = 0
    is_rest: bool = False


@dataclass(frozen=True)
class VoiceProfile:
    name: str
    range_min: int
    range_max: int
    tessitura_min: int
    tessitura_max: int
    clef_hint: str | None = None

    @property
    def melodic_span(self) -> int:
        return self.range_max - self.range_min


@dataclass(frozen=True)
class FormSection:
    label: str
    start_bar: int
    end_bar: int
    role: str
    source_bar: int | None = None
    transform: str = "free"


@dataclass(frozen=True)
class FormPlan:
    kind: str
    sections: tuple[FormSection, ...] = ()

    def section_for_bar(self, bar_number: int) -> FormSection | None:
        for section in self.sections:
            if section.start_bar <= bar_number <= section.end_bar:
                return section
        return None


@dataclass(frozen=True)
class ChoralePlan:
    voice_profiles: tuple[VoiceProfile, ...] = ()


@dataclass(frozen=True)
class Motif:
    events: tuple[NoteEvent, ...]
    name: str = "motif"

    @classmethod
    def from_steps(cls, scale_steps: list[int], durations: list[float], name: str = "motif") -> "Motif":
        if len(scale_steps) != len(durations):
            raise ValueError("Motif scale steps and durations must have equal length")
        return cls(
            events=tuple(
                NoteEvent(scale_step=scale_step, duration=duration)
                for scale_step, duration in zip(scale_steps, durations)
            ),
            name=name,
        )

    @property
    def length(self) -> float:
        return sum(event.duration for event in self.events)

    def transpose_diatonic(self, step_shift: int) -> "Motif":
        return Motif(
            events=tuple(event.transpose_diatonic(step_shift) for event in self.events),
            name=self.name,
        )


@dataclass(frozen=True)
class HarmonySpan:
    start_bar: int
    end_bar: int
    roman_symbol: str
    weight: float = 1.0

    def covers(self, bar_number: int) -> bool:
        return self.start_bar <= bar_number <= self.end_bar


@dataclass(frozen=True)
class HarmonyPlan:
    spans: tuple[HarmonySpan, ...] = ()

    def chord_for_bar(self, bar_number: int) -> HarmonySpan | None:
        for span in self.spans:
            if span.covers(bar_number):
                return span
        return None


@dataclass(frozen=True)
class Melody:
    key: Key
    time_signature: TimeSignature
    events: tuple[NoteEvent, ...]
    harmony_plan: HarmonyPlan = HarmonyPlan()
    clef: str | None = None
    voice_profile: VoiceProfile = VoiceProfile(
        name="melody",
        range_min=0,
        range_max=9,
        tessitura_min=1,
        tessitura_max=8,
    )
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def pitched_events(self) -> tuple[NoteEvent, ...]:
        return tuple(event for event in self.events if not event.is_rest)

    def transpose_diatonic(self, step_shift: int) -> "Melody":
        return Melody(
            key=self.key,
            time_signature=self.time_signature,
            events=tuple(event.transpose_diatonic(step_shift) for event in self.events),
            harmony_plan=self.harmony_plan,
            clef=self.clef,
            voice_profile=self.voice_profile,
            metadata=dict(self.metadata),
        )

    def transpose_parallel(self, new_key: Key) -> "Melody":
        return Melody(
            key=new_key,
            time_signature=self.time_signature,
            events=self.events,
            harmony_plan=self.harmony_plan,
            clef=self.clef,
            voice_profile=self.voice_profile,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class GenerationSettings:
    key: Key
    time_signature: TimeSignature
    bars: int
    allowed_durations: tuple[float, ...] = (0.5, 1.0, 2.0)
    range_min: int = 0
    range_max: int = 9
    motif: Motif | None = None
    motif_repetition_bar: int | None = None
    motif_repetition_shift: int = 1
    harmonic_plan: HarmonyPlan = HarmonyPlan()
    phrase_length_bars: int = 4
    cadence_duration: float = 2.0
    attempts: int = 48
    random_seed: int = 7
    form_plan: FormPlan = FormPlan(kind="free")
    clef: str | None = None
    voice_profile: VoiceProfile = VoiceProfile(
        name="melody",
        range_min=0,
        range_max=9,
        tessitura_min=1,
        tessitura_max=8,
    )
    chorale_plan: ChoralePlan = ChoralePlan()
