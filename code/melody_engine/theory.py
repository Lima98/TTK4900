from __future__ import annotations

from dataclasses import dataclass

LETTERS = ("c", "d", "e", "f", "g", "a", "b")
NATURAL_PITCH_CLASSES = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}

MODE_INTERVALS = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "locrian": (0, 1, 3, 5, 6, 8, 10),
}

ROMAN_TO_DEGREE = {
    "i": 0,
    "ii": 1,
    "iii": 2,
    "iv": 3,
    "v": 4,
    "vi": 5,
    "vii": 6,
}

TRIAD_QUALITIES = {
    "major": (0, 4, 7),
    "minor": (0, 3, 7),
    "diminished": (0, 3, 6),
    "augmented": (0, 4, 8),
}


def parse_pitch_class(note_name: str) -> int:
    normalized = note_name.strip().lower()
    letter = normalized[0]
    pitch_class = NATURAL_PITCH_CLASSES[letter]

    for accidental in normalized[1:]:
        if accidental in {"s", "#"}:
            pitch_class += 1
        elif accidental in {"f", "b"}:
            pitch_class -= 1
        else:
            raise ValueError(f"Unsupported accidental in note name: {note_name}")

    return pitch_class % 12


def accidental_suffix(accidental: int) -> str:
    accidental_map = {
        -2: "ff",
        -1: "f",
        0: "",
        1: "s",
        2: "ss",
    }
    if accidental not in accidental_map:
        raise ValueError(f"Unsupported accidental distance: {accidental}")
    return accidental_map[accidental]


def accidental_value(symbol: str) -> int:
    value = 0
    for accidental in symbol:
        if accidental in {"s", "#"}:
            value += 1
        elif accidental in {"f", "b"}:
            value -= 1
        else:
            raise ValueError(f"Unsupported accidental marker: {symbol}")
    return value


def lilypond_octave(octave: int) -> str:
    if octave >= 3:
        return "'" * (octave - 3)
    return "," * (3 - octave)


def normalize_roman_symbol(symbol: str) -> str:
    stripped = symbol.strip()
    lowered = stripped.lower().replace("°", "")
    cleaned = lowered.lstrip("b#sf")
    if cleaned not in ROMAN_TO_DEGREE:
        raise ValueError(f"Unsupported roman numeral: {symbol}")
    return cleaned


def roman_symbol_accidental(symbol: str) -> int:
    stripped = symbol.strip()
    accidental_text = []
    for char in stripped:
        if char in {"b", "#", "s", "f"}:
            accidental_text.append(char)
            continue
        break
    return accidental_value("".join(accidental_text))


def roman_symbol_quality(symbol: str) -> str:
    stripped = symbol.strip()
    if "+" in stripped:
        return "augmented"
    if "°" in stripped or "o" in stripped:
        return "diminished"
    if any(char.isalpha() and char.isupper() for char in stripped):
        return "major"
    return "minor"


def split_spelling(spelling: str) -> tuple[str, int]:
    letter = spelling[0]
    accidental_text = spelling[1:]
    return letter, accidental_value(accidental_text)


@dataclass(frozen=True)
class Key:
    tonic: str
    mode: str = "major"
    tonic_octave: int = 4

    def __post_init__(self) -> None:
        normalized_mode = self.mode.lower()
        if normalized_mode not in MODE_INTERVALS:
            raise ValueError(f"Unsupported mode: {self.mode}")
        object.__setattr__(self, "mode", normalized_mode)
        object.__setattr__(self, "tonic", self.tonic.strip())

    @property
    def tonic_pitch_class(self) -> int:
        return parse_pitch_class(self.tonic)

    @property
    def scale_intervals(self) -> tuple[int, ...]:
        return MODE_INTERVALS[self.mode]

    @property
    def scale_spellings(self) -> tuple[str, ...]:
        tonic_name = self.tonic.lower()
        tonic_letter = tonic_name[0]
        tonic_letter_index = LETTERS.index(tonic_letter)
        spellings: list[str] = []

        for degree_index, interval in enumerate(self.scale_intervals):
            letter = LETTERS[(tonic_letter_index + degree_index) % 7]
            target_pitch_class = (self.tonic_pitch_class + interval) % 12
            natural_pitch_class = NATURAL_PITCH_CLASSES[letter]
            accidental_distance = ((target_pitch_class - natural_pitch_class + 6) % 12) - 6
            if accidental_distance not in {-2, -1, 0, 1, 2}:
                raise ValueError(f"Cannot spell scale degree {degree_index + 1} in {self.tonic} {self.mode}")
            spellings.append(letter + accidental_suffix(accidental_distance))

        return tuple(spellings)

    def lilypond_pitch(self, scale_step: int) -> str:
        degree_index = scale_step % 7
        octave_offset = scale_step // 7
        pitch_name = self.scale_spellings[degree_index]
        octave = self.tonic_octave + octave_offset
        return f"{pitch_name}{lilypond_octave(octave)}"

    def chromatic_pitch(self, scale_step: int, chromatic_adjustment: int = 0) -> str:
        degree_index = scale_step % 7
        octave_offset = scale_step // 7
        pitch_name = self.scale_spellings[degree_index]
        letter, accidental = split_spelling(pitch_name)
        octave = self.tonic_octave + octave_offset
        return f"{letter}{accidental_suffix(accidental + chromatic_adjustment)}{lilypond_octave(octave)}"

    def scale_pitch_class(self, scale_step: int) -> int:
        degree_index = scale_step % 7
        octave_offset = scale_step // 7
        return (self.tonic_pitch_class + self.scale_intervals[degree_index] + (12 * octave_offset)) % 12

    def chord_tones(self, roman_symbol: str) -> tuple[int, int, int]:
        root_degree = ROMAN_TO_DEGREE[normalize_roman_symbol(roman_symbol)]
        return (
            root_degree % 7,
            (root_degree + 2) % 7,
            (root_degree + 4) % 7,
        )

    def chord_pitch_classes(self, roman_symbol: str) -> tuple[int, int, int]:
        normalized = normalize_roman_symbol(roman_symbol)
        root_degree = ROMAN_TO_DEGREE[normalized]
        root_pitch_class = (self.tonic_pitch_class + self.scale_intervals[root_degree] + roman_symbol_accidental(roman_symbol)) % 12
        quality = roman_symbol_quality(roman_symbol)
        intervals = TRIAD_QUALITIES[quality]
        return tuple((root_pitch_class + interval) % 12 for interval in intervals)

    def chord_scale_targets(self, roman_symbol: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        chord_degrees = self.chord_tones(roman_symbol)
        target_pitch_classes = self.chord_pitch_classes(roman_symbol)
        targets: list[tuple[int, int]] = []
        for degree, target_pitch_class in zip(chord_degrees, target_pitch_classes):
            diatonic_pitch_class = (self.tonic_pitch_class + self.scale_intervals[degree]) % 12
            adjustment = ((target_pitch_class - diatonic_pitch_class + 6) % 12) - 6
            if adjustment not in {-2, -1, 0, 1, 2}:
                raise ValueError(f"Chord symbol requires unsupported chromatic adjustment: {roman_symbol}")
            targets.append((degree, adjustment))
        return tuple(targets)  # type: ignore[return-value]
