@dataclass(frozen=True)
class VoiceProfile:
    name: str
    range_min: int
    range_max: int
    tessitura_min: int
    tessitura_max: int
    clef_hint: str | None = None


@dataclass(frozen=True)
class FormSection:
    label: str
    start_bar: int
    end_bar: int
    role: str
    source_bar: int | None = None
    transform: str = "free"


@dataclass(frozen=True)
class Motif:
    events: tuple[NoteEvent, ...]
    name: str = "motif"
