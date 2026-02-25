# Handling of music concepts using Key, Note, Melody objects

# Define scale degrees, and letter order for pitch spelling
SCALES = {
        # Basic scales
        "chromatic": ["1","b2", "2","b3", "3", "4", "s4", "5", "b6", "6", "b7", "7"],
        "major": ["1", "2", "3", "4", "5", "6", "7"],
        "minor": ["1", "2", "b3", "4", "5", "b6", "b7"],

        #Pentatonic scales
        "major_pentatonic": ["1", "2", "3", "5", "6"],
        "minor_pentatonic": ["1", "b3", "4", "5", "b7"],

        # Diatonic modes
        "dorian": ["1", "2", "b3", "4", "5", "6", "b7"],
        "phrygian": ["1", "b2", "b3", "4", "5", "b6", "b7"],
        "lydian": ["1", "2", "3", "s4", "5", "6", "7"],
        "mixolydian": ["1", "2", "3", "4", "5", "6", "b7"],
        "locrian": ["1", "b2", "b3", "4", "b5", "b6", "b7"],

        #Exotic modes
        "harmonic_minor": ["1", "2", "b3", "4", "5", "b6", "7"],
        "phrygian_dominant":  ["1", "b2", "3", "4", "5", "b6", "b7"]
        }

LETTER_ORDER = ["c", "d", "e", "f", "g", "a", "b"]

NATURAL_PITCHES = { 
                   "c": 0,
                   "d": 2,
                   "e": 4,
                   "f": 5,
                   "g": 7,
                   "a": 9,
                   "b": 11
                   }

# Musical concepts represented as classes
class Note:
    """
    A musical note, represented by scale degree, concrete pitch and duration.

    Attributes:
        degree: Scale degree (1, 2, b3, s4, etc.) (Abstract)
        pitch: Concrete pitch ('c', 'eb', 'fs', etc.) (Concrete)
        duration: Duration in beats (1 for quarter note, 0.5 for eighth note, etc.)
    """
    def __init__(self, degree=None, pitch=None, duration=None):
        """ 
        Initialization function for Note class.

        Args:
            degree: Scale degree (1, 2, b3, s4, etc.)
            pitch: Concrete pitch ('c', 'eb', 'fs', etc.)
            duration: Duration in beats (1 for quarter note, 0.5 for eighth note, etc.)
        """
        self.degree = degree    # Scale degree (abstract)
        self.pitch = pitch      # Concrete pitch (string, e.g., 'c4')
        self.duration = duration # Duration in beats (optional)

    def is_abstract(self):
        """
        Utility function to check if the note is abstract (has a degree but no concrete pitch).

        Returns: True if the note has a degree but no concrete pitch, False otherwise.
            
        """
        return self.degree is not None

    def is_concrete(self):
        """
        Utility function to check if the note is concrete (has a concrete pitch).

        Returns: True if the note has a concrete pitch, False otherwise.
            
        """
        return self.pitch is not None

    def __repr__(self):
        """
        Debugging function to represent the Note object as a string for easy visualization.

        Returns: A string with the attributes of the Note object.

        """
        return f"Note({self.pitch or self.degree}, dur={self.duration})"

# Key class
class Key:
    """
    A musical key, defined by its tonic and mode.

    Attributes:
        tonic: Root note of the key ('c', 'eb', 'fs', etc.)
        mode: Scale type ('major', 'minor', 'dorian', etc.)
    """
    def __init__(self, tonic: str, mode: str = "major"):
        """
        Initialization function for Key class.

        Args:
            tonic: Root note of the key ('c', 'eb', 'fs', etc.)
            mode: Scale type ('major', 'minor', 'dorian', etc.)
        """
        self.tonic = tonic
        self.mode = mode
        self.degrees = SCALES[mode]

    def degree_to_pitch(self, degree: str) -> str:
        print("Key degree_to_pitch function run")
        """
        Utility function to convert a scale degree to its corresponding pitch name based on the key's tonic and mode.

        Args:
            degree: A string representing the scale degree (e.g., '1', 'b3', 's4', etc.)

        Returns: A string representing the corresponding pitch name (e.g., 'c', 'eb', 'fs', etc.)

        """
        return scale_degrees_to_pitch([degree], self.tonic)[0]

    def get_scale_pitches(self):
        """

        Returns:  A list of strings representing the pitch names of the scale degrees in the key.

        """
        return scale_degrees_to_pitch(self.degrees, self.tonic)

    def __repr__(self):
        """
        Debugging function to represent the Key object as a string for easy visualization.

        Returns: A string with the attributes of the Key object.

        """
        return f"Key({self.tonic} {self.mode})"

# Melody class
class Melody:
    """
    A musical melody, consisting of a sequence of notes and an associated key.

    Attributes:
        key: Key object representing the key of the melody.
        notes: List of Note objects representing the melody.
        tags: optional dictionary for additional metadata (e.g., verse, original/variation, bass/tenor, etc.)
    """
    def __init__(self, key: Key, notes, tags=None):
        """
        Initialization function for Melody class.

        Args:
            key: Key object representing the key of the melody.
            notes: List of Note objects representing the melody.
            tags: optional dictionary for additional metadata (e.g., verse, original/variation, bass/tenor, etc.)
        """
        self.notes = notes or []  # list of Note objects
        self.key = key
        self.tags = tags or {}

    def to_pitches(self):
        """
        Converts abstract notes (with scale degrees) to concrete pitches based on the melody's key.

        Raises:
            ValueError: If the melody has no key assigned or if any note is abstract without a degree.
        """
        if self.key is None:
            raise ValueError("Melody has no key assigned")
        for note in self.notes:
            if note.is_abstract() and note.pitch is None:
                note.pitch = self.key.degree_to_pitch(str(note.degree))

    def add_rhythm(self, rhythm):
        """
        Adds rhythm to the melody by assigning durations to each note based on a provided rhythm pattern.

        Args:
            rhythm (list): A list of durations corresponding to each note in the melody.

        Raises:
            ValueError: If the length of the rhythm list does not match the number of notes in the melody.
        """
        if len(rhythm) != len(self.notes):
            raise ValueError("Rhythm and notes length mismatch")
        for note, dur in zip(self.notes, rhythm):
            note.duration = dur

    def __repr__(self):
        """
        Debugging function to represent the Melody object as a string for easy visualization.

        Returns: A string with the attributes of the Melody object.

        """
        return f"Melody({self.notes}, key={self.key}, tags={self.tags})"

# Helper function to spell a note based on its letter and accidental
def spell_note(letter, accidental):
    """
    Helper function to spell a note based on its letter and accidental.

    Args:
        letter (str): A string representing note to be spelled.
        accidental (int): Integer representing accidental. (-2, -1, 0, 1, 2) Negative for flats and positive for sharps.

    Returns: A string with the spelled note.

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
    Converting scale degrees to pitch names based on the root note.

    Args:
        degrees (list): List of string representing the scale degrees.
        root (str): String representing the root of the key for the melody. ('c', 'eb', 'fs', etc.)

    Returns: A list of strings representing pitch names.

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
