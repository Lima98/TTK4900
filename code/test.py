LETTER_ORDER = ["c", "d", "e", "f", "g", "a", "b"]

NATURAL_PITCHES = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}

# Major scale semitone pattern from root
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]

def parse_accidentals(text: str) -> int:
    """
    Counts sharps ('s') and flats ('b')
    Supports unlimited accidentals: bb, sss, etc.
    """
    return text.count("s") - text.count("b")

def parse_note(note: str):
    letter = note[0].lower()
    accidental = parse_accidentals(note[1:])
    pitch = (NATURAL_PITCHES[letter] + accidental) % 12
    return letter, pitch

def scale_degrees_to_pitch(degrees, root):
    """
    Converts scale degrees (e.g., ["1", "b3", "5"]) into properly spelled
    pitch names in a major key defined by `root`.

    Supports unlimited sharps/flats in both root and degrees.
    """

    pitches = []

    # --- Parse root ---
    root_letter, root_pitch = parse_note(root)

    root_index = LETTER_ORDER.index(root_letter)

    for degree in degrees:
        # --- Parse degree ---
        i = 0
        while i < len(degree) and not degree[i].isdigit():
            i += 1

        accidental_text = degree[:i]
        degree_number = int(degree[i:])
        degree_accidental = parse_accidentals(accidental_text)

        # --- Determine scale letter ---
        letter_index = (root_index + degree_number - 1) % 7
        letter = LETTER_ORDER[letter_index]

        # --- Target pitch ---
        scale_interval = MAJOR_SCALE_INTERVALS[degree_number - 1]
        pitch = (root_pitch + scale_interval + degree_accidental) % 12

        # --- Natural pitch of letter ---
        natural_pitch = NATURAL_PITCHES[letter]

        # --- Required accidental relative to natural letter ---
        accidental = pitch - natural_pitch

        # Normalize into range -6 to +6
        accidental = (accidental + 6) % 12 - 6

        pitches.append(spell_note(letter, accidental))

    return pitches

def spell_note(letter, accidental):
    """

    Args:
        letter (str): The natural letter name of the note (e.g., "c", "d", "e", "f", "g", "a", "b") to which the accidental will be applied.
        accidental (int): An integer representing the accidental to apply to the letter, where 0 means natural, -1 means flat, and 1 means sharp.

    Returns:       A string representing the pitch name of the note after applying the accidental to the natural letter, following standard musical notation conventions (e.g., "c", "df", "es", "f", "gs", etc.).
        
    """
    if accidental == 0:
        return letter
    elif accidental == -1:
        return letter + "f"
    elif accidental == 1:
        return letter + "s"

