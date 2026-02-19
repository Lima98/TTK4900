# Handling of music concepts. Melodies, rhythm, keys etc... 
import random

# Define scale degrees and scales
SCALES = {
    # Diatonic modes/scales
    "chromatic": ["1","b2", "2","b3", "3", "4", "s4", "5", "b6", "6", "b7", "7"],
    "major": ["1", "2", "3", "4", "5", "6", "7"],
    "minor": ["1", "2", "b3", "4", "5", "b6", "b7"],
    "dorian": ["1", "2", "b3", "4", "5", "6", "b7"],
    "phrygian": ["1", "b2", "b3", "4", "5", "b6", "b7"],
    "lydian": ["1", "2", "3", "s4", "5", "6", "7"],
    "mixolydian": ["1", "2", "3", "4", "5", "6", "b7"],
    "locrian": ["1", "b2", "b3", "4", "b5", "b6", "b7"],

    # Exotic scales
    "harmonic_minor": ["1", "2", "b3", "4", "5", "b6", "7"],
    "phrygian_dominant":  ["1", "b2", "3", "4", "5", "b6", "b7"]
    # Add more scales as needed
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

def build_key(key="c major"):
    """

    Args:
        key (str): A string representing the musical key, consisting of a root note and an optional scale type (e.g., "c major", "d minor", "eb phrygian"). The root note can include accidentals (e.g., "c", "d", "eb", "fs"), and the scale type can be one of the predefined scales in the SCALES dictionary (e.g., "major", "minor", "dorian", etc.). If the scale type is not specified, it defaults to "major".

    Returns:    A list of pitch names corresponding to the scale degrees of the specified key, where each pitch name is derived from the root note and the intervals defined by the chosen scale. The function processes the input key to determine the root and scale, retrieves the appropriate scale degrees, and converts them into pitch names based on the root and any accidentals present in the key.
        
    """
    # Get root and scale from the key input
    root, *rest = key.split()
    scale = rest[0] if rest else "major"

    # Get the scale degrees for the specified scale
    degrees = SCALES[scale]

    # Convert scale degrees to pitch names
    key_pitches = scale_degrees_to_pitch(degrees, root)

    return key_pitches

# TODO: Go over the code, make it more readable and handle double flats and sharps
def scale_degrees_to_pitch(degrees, root):
    """

    Args:
        degrees (list): A list of scale degrees (e.g., ["1", "2", "3", "4", "5", "6", "7"]) to convert to their corresponding pitch names based on the specified root.
        root (str): The root note of the key (e.g., "c", "d", "eb", "fs") to use as the basis for calculating the pitch names of the scale degrees.

    Returns:      A list of pitch names corresponding to the input scale degrees based on the specified root, taking into account any accidentals in the root and the scale degrees.
        
    """
    pitches = []

    # Base root pitch
    root_letter = root[0]
    root_pitch = NATURAL_PITCHES[root_letter]

    # Adjust for accidental in the root
    if len(root) > 1:
        if root[1] == "b":
            root_pitch -= 1
        elif root[1] == "s":
            root_pitch += 1

    # Process each degree
    for degree in degrees:
        # Determine accidental for the degree
        if degree.startswith("b"):
            accidental = -1
            degree_num = int(degree[1:])
        elif degree.startswith("s"):
            accidental = 1
            degree_num = int(degree[1:])
        else:
            accidental = 0
            degree_num = int(degree)

        # Find the letter corresponding to this degree in the key
        letter_index = (LETTER_ORDER.index(root_letter) + degree_num - 1) % 7
        letter = LETTER_ORDER[letter_index]

        # Natural pitch of the letter
        natural_pitch = NATURAL_PITCHES[letter]

        # Compute pitch number relative to root
        # Rough approximation: major scale steps
        scale_interval = (degree_num - 1) * 2
        if degree_num > 3:  # adjust for half steps in major scale
            scale_interval -= 1

        pitch = (root_pitch + scale_interval + accidental) % 12

        # Determine accidental relative to natural letter
        final_accidental = (pitch - natural_pitch + 12) % 12
        if final_accidental > 6:
            final_accidental -= 12

        # Spell the note
        pitches.append(spell_note(letter, final_accidental))

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

# Generate notes in a melody
def generate_random_notes(length=8):
    """

    Args:
        length (int):  The number of notes in the generated melody.

    Returns:        A list of pitch names representing a melody generated by randomly selecting scale degrees from the chromatic scale and converting them to pitch names based on the key of C major.
    
    """
    melody = [random.choice(SCALES["chromatic"]) for _ in range(length)]
    melody = scale_degrees_to_pitch(melody, "c") 
    return melody 


# Generate notes based on intervals
def generate_notes(notes = 4, key = build_key("c major")):
    """

    Args:
        notes (int): The number of notes in the generated melody.
        scale (list): The scale to use for generating the melody. Default is the major scale represented by scale_degrees. 

    Returns:       A list of scale degrees representing a melody generated based on random intervals from the given scale.
        
    """
    intervals   =   [-2, -1, 0, 1, 2] # only 2nds and 3rds for now
    melody      =   []
    current     =   0
    
    for _ in range(notes):
        val     =   random.choice(intervals)
        current +=  val
        
        if current < 0:
                current += len(key) 
        if current > len(key) - 1:
            current -= len(key)

        note    =   key[current]
        melody.append(note)

    return melody


# generate a numbers of bars of random rhythm pattern in a given time signature
# TODO: Change notesPerBar to key signature and split with .split('/') 
def generate_rhythm(bars = 1, notesPerBar = 4, values = ["q"]):
    """

    Args:
        bars (int):        The number of bars to generate.
        notesPerBar (int): The number of beats per bar (e.g., 4 for 4/4 time).
        values (list):      A list of rhythm symbols to use for generating the rhythm. Default is ["q"] (quarter notes).

    Returns:            A list of rhythm values representing the generated rhythm pattern.
        
    """
    rhythm  =   []
    tot     =   0
    values  =   rhythm_to_values(values)
    
    for _ in range(bars):
        tot = 0
        while tot < notesPerBar:
            choices = [v for v in values if tot + v <= notesPerBar]
            val     = random.choice(choices)
            rhythm.append(val)
            tot     += val

    return rhythm


# Convert rhythm symbols to their corresponding beat values
def rhythm_to_values(rhythm):
    """

    Args:
        rhythm (list): A list of rhythm symbols (e.g., ["q", "e", "s"]) to convert to their corresponding beat values.

    Returns:       A list of beat values corresponding to the input rhythm symbols.
        
    """
    rhythm_to_val = {
            "l": 16,        # longa
            "b": 8,         # breve
            "w": 4,         # whole note
            "h": 2,         # half note
            "q": 1,         # quarter note
            "e": 0.5,       # eighth note
            "s": 0.25,      # sixteenth note
            "t": 0.125,     # thirty-second note
            "x": 0.0625     # sixty-fourth note
            }
    values = [rhythm_to_val[dur] for dur in rhythm]

    return values


# TODO: Implement this
# Diatonic transposition using the scale degrees
def transpose(melody, interval=random.choice([-2, -1, 1, 2])):
    transposed_melody = []

    return transposed_melody


# TODO: Implement this
# Create a variation of given melody
def variation_melody(melody):
    
    return


# TODO: Implement this
# Create a variation of given melody
def variation_rhythm(rhythm):
    
    return
