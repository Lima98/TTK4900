# Handling of music concepts using Key, Note, Melody objects
import random

# Define scale degrees, and letter order for pitch spelling
SCALES = {
    "chromatic": ["1","b2", "2","b3", "3", "4", "s4", "5", "b6", "6", "b7", "7"],
    "major": ["1", "2", "3", "4", "5", "6", "7"],
    "minor": ["1", "2", "b3", "4", "5", "b6", "b7"],
    "dorian": ["1", "2", "b3", "4", "5", "6", "b7"],
    "phrygian": ["1", "b2", "b3", "4", "5", "b6", "b7"],
    "lydian": ["1", "2", "3", "s4", "5", "6", "7"],
    "mixolydian": ["1", "2", "3", "4", "5", "6", "b7"],
    "locrian": ["1", "b2", "b3", "4", "b5", "b6", "b7"],
    "harmonic_minor": ["1", "2", "b3", "4", "5", "b6", "7"],
    "phrygian_dominant":  ["1", "b2", "3", "4", "5", "b6", "b7"]
}

LETTER_ORDER = ["c", "d", "e", "f", "g", "a", "b"]

NATURAL_PITCHES = { 
    "c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11
}


# ---------------- Note ----------------
class Note:
    def __init__(self, degree=None, pitch=None, duration=None):
        self.degree = degree    # Scale degree (abstract)
        self.pitch = pitch      # Concrete pitch (string, e.g., 'c4')
        self.duration = duration # Duration in beats (optional)

    def is_abstract(self):
        return self.degree is not None

    def is_concrete(self):
        return self.pitch is not None

    def __repr__(self):
        return f"Note({self.pitch or self.degree}, dur={self.duration})"


# ---------------- Key ----------------
class Key:
    def __init__(self, tonic: str, mode: str = "major"):
        self.tonic = tonic
        self.mode = mode
        self.degrees = SCALES[mode]

    def degree_to_pitch(self, degree: str) -> str:
        """Convert a single scale degree to pitch in this key."""
        return scale_degrees_to_pitch([degree], self.tonic)[0]

    def get_scale_pitches(self):
        return scale_degrees_to_pitch(self.degrees, self.tonic)

    def __repr__(self):
        return f"Key({self.tonic} {self.mode})"


# ---------------- Melody ----------------
class Melody:
    def __init__(self, notes=None, key: Key = None, tags=None):
        self.notes = notes or []  # list of Note objects
        self.key = key
        self.tags = tags or {}

    def to_pitches(self):
        """Convert all degree notes to pitches using the melody's key."""
        if self.key is None:
            raise ValueError("Melody has no key assigned")
        for note in self.notes:
            if note.is_abstract() and note.pitch is None:
                note.pitch = self.key.degree_to_pitch(str(note.degree))

    def add_rhythm(self, rhythm):
        """Assign durations to notes."""
        if len(rhythm) != len(self.notes):
            raise ValueError("Rhythm and notes length mismatch")
        for note, dur in zip(self.notes, rhythm):
            note.duration = dur

    def __repr__(self):
        return f"Melody({self.notes}, key={self.key}, tags={self.tags})"


# ---------------- Helpers ----------------
def spell_note(letter, accidental):
    if accidental == 0:
        return letter
    elif accidental == -1:
        return letter + "f"
    elif accidental == 1:
        return letter + "s"


def scale_degrees_to_pitch(degrees, root):
    """Convert scale degrees to pitch names based on a root."""
    pitches = []
    root_letter = root[0]
    root_pitch = NATURAL_PITCHES[root_letter]

    # Adjust for accidental in root
    if len(root) > 1:
        if root[1] == "b":
            root_pitch -= 1
        elif root[1] == "s":
            root_pitch += 1

    for degree in degrees:
        if degree.startswith("b"):
            accidental = -1
            degree_num = int(degree[1:])
        elif degree.startswith("s"):
            accidental = 1
            degree_num = int(degree[1:])
        else:
            accidental = 0
            degree_num = int(degree)

        letter_index = (LETTER_ORDER.index(root_letter) + degree_num - 1) % 7
        letter = LETTER_ORDER[letter_index]
        natural_pitch = NATURAL_PITCHES[letter]
        scale_interval = (degree_num - 1) * 2
        if degree_num > 3:
            scale_interval -= 1
        pitch = (root_pitch + scale_interval + accidental) % 12
        final_accidental = (pitch - natural_pitch + 12) % 12
        if final_accidental > 6:
            final_accidental -= 12
        pitches.append(spell_note(letter, final_accidental))
    return pitches
