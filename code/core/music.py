# Handling of music concepts using Key, Note, Melody objects

# Define scale degrees, and letter order for pitch spelling
SCALES = {
    "chromatic": ["1","b2", "2","b3", "3", "4", "s4", "5", "b6", "6", "b7", "7"],
    "major": ["1", "2", "3", "4", "5", "6", "7"],
    "minor": ["1", "2", "b3", "4", "5", "b6", "b7"],

    "major_pentatonic": ["1", "2", "3", "5", "6"],
    "minor_pentatonic": ["1", "b3", "4", "5", "b7"],

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

# Musical concepts represented as classes
class Note:
    """

    Attributes:
        degree: scale degree (abstract, e.g., 1, b2, s4)
        pitch: concrete pitch (string, e.g., 'c4')
        duration: duration in beats (optional, e.g., 1 for quarter note, 0.5 for eighth note)
    """
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


class Key:
    """

    Attributes:
        tonic: root note of the key (string, e.g., 'c', 'd', 'eb')
        mode: scale type (string, e.g., 'major', 'minor', 'dorian')
        degrees: list of scale degrees for the mode (derived from SCALES)
    """
    def __init__(self, tonic: str, mode: str = "major"):
        self.tonic = tonic
        self.mode = mode
        self.degrees = SCALES[mode]

    def degree_to_pitch(self, degree: str) -> str:
        return scale_degrees_to_pitch([degree], self.tonic)[0]

    def get_scale_pitches(self):
        return scale_degrees_to_pitch(self.degrees, self.tonic)

    def __repr__(self):
        return f"Key({self.tonic} {self.mode})"


class Melody:
    """

    Attributes:
        notes: list of Note objects representing the melody
        key: Key object representing the key of the melody
        tags: optional dictionary for additional metadata (e.g., tempo, style)
    """
    def __init__(self, key: Key, notes, tags=None):
        self.notes = notes or []  # list of Note objects
        self.key = key
        self.tags = tags or {}

    def to_pitches(self):
        if self.key is None:
            raise ValueError("Melody has no key assigned")
        for note in self.notes:
            if note.is_abstract() and note.pitch is None:
                note.pitch = self.key.degree_to_pitch(str(note.degree))

    def add_rhythm(self, rhythm):
        if len(rhythm) != len(self.notes):
            raise ValueError("Rhythm and notes length mismatch")
        for note, dur in zip(self.notes, rhythm):
            note.duration = dur

    def __repr__(self):
        return f"Melody({self.notes}, key={self.key}, tags={self.tags})"


# Helper function to spell a note based on its letter and accidental
def spell_note(letter, accidental):
    """

    Args:
        letter (str): A string representing the letter name of the note (e.g., "c", "d", "e", "f", "g", "a", "b") to be spelled.
        accidental (int): An integer representing the accidental of the note, where 0 indicates a natural note, -1 indicates a flat, and 1 indicates a sharp. This value is used to determine how to modify the letter name of the note when spelling it (e.g., "c" with an accidental of -1 would be spelled as "cf" for C flat, while "c" with an accidental of 1 would be spelled as "cs" for C sharp).

    Returns:    A string representing the spelled note name based on the input letter and accidental, where the letter is modified according to the accidental (e.g., "c" with an accidental of -1 would return "cf", "c" with an accidental of 1 would return "cs", and "c" with an accidental of 0 would return "c").
        
    """
    if accidental == 0:
        return letter
    elif accidental == -1:
        return letter + "f"
    elif accidental == 1:
        return letter + "s"

# Convert scale degrees to pitch names based on the root note
def scale_degrees_to_pitch(degrees, root):
    """

    Args:
        degrees (list): A list of scale degrees (e.g., ["1", "b2", "3"]) to be converted to pitch names based on the specified root note. Each degree can include an accidental (e.g., "b2" for flat second, "s4" for sharp fourth) which will be taken into account when calculating the final pitch name.
        root (str): A string representing the root note (e.g., "c", "d", "eb") from which the scale degrees will be calculated. The root note can also include an accidental (e.g., "eb" for E flat, "fs" for F sharp) which will affect the starting pitch for the scale degree calculations.

    Returns:     A list of pitch names corresponding to the input scale degrees based on the specified root note. Each pitch name is derived from the root note and the intervals defined by the scale degrees, taking into account any accidentals in both the root and the degrees. For example, if the root is "c" and the degree is "b2", the resulting pitch name would be "cf" (C flat), while if the degree is "s4", the resulting pitch name would be "cs" (C sharp).
        
    """
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
