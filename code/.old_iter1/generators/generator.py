# Main module for generating melodies and rhythms using Melody/Note objects
import random
from core.music import Key, Note, Melody, SCALES
from core.models import Phrase, Motif

# Generate a random chromatic melody
# NOTE: Deprecated
def generate_random_notes(length=8, key: Key = Key("c", "major")) -> Melody:
    """
    Generate a random chromatic melody.

    Args:
        length (int): Number of notes in the melody.
        key: Key object representing the key to display the melody in.

    Returns: A Melody object containing the generated notes and the associated key.
        
    """
    # Random scale degrees from chromatic scale
    degrees = [random.choice(SCALES["chromatic"]) for _ in range(length)]
    
    # Create Note objects and convert to pitch
    notes = [Note(degree=int(d.replace("b","").replace("s","") if d[0] in "bs" else int(d)), 
                  pitch=key.degree_to_pitch(d)) for d in degrees]
    
    return Melody(notes = notes, key = key, rhythm=None)

# Generate a melody by randomly moving in 2nds and 3rds within the scale
def generate_notes(num_notes=4, key: Key = Key("c", "major")) -> Melody:
    """
    Generate a melody by randomly moving in 2nds and 3rds within the scale.

    Args:
        num_notes (int): Number of notes to generate in the melody.
        key: Key object representing the key of the melody.

    Returns:
        
    """
    intervals = [-2, -1, 0, 1, 2]  # only 2nds and 3rds
    melody_notes = []
    current_idx = 0
    scale = key.get_scale_pitches()

    for _ in range(num_notes):
        val = random.choice(intervals)
        current_idx = (current_idx + val) % len(scale)
        note = Note(degree=current_idx+1, pitch=scale[current_idx])
        melody_notes.append(note)

    return Melody(notes = melody_notes, key = key, rhythm=None)

# Generate a rhythm pattern based on the time signature and allowed rhythm values
# TODO: add support for rests?
def generate_rhythm(bars=1, time_sig="4/4", values=["q"]):
    """
    Generate a rhythm pattern based on the time signature and allowed rhythm values.

    Args:
        bars (int): Number of bars to generate.
        time_sig (str): Time signature in the format "quantity/value" (e.g., "4/4", "3/4", "6/8").
      

    Returns: A list of rhythm values corresponding to the generated rhythm pattern.
        
    """
    quantity, unit = map(int, time_sig.split("/"))
    notes_per_bar = int(quantity * (4 / unit))
    rhythm = []
    values = rhythm_to_values(values)

    for _ in range(bars):
        tot = 0
        while tot < notes_per_bar:
            choices = [v for v in values if tot + v <= notes_per_bar]
            val = random.choice(choices)
            rhythm.append(val)
            tot += val

    return rhythm

# Helper function to convert rhythm symbols to beat values
def rhythm_to_values(rhythm):
    """
    Convert rhythm symbols to beat values.

    Args:
        rhythm (list): List of rhythm symbols (e.g., ["q", "e", "h"]).

    Returns:
        
    """
    rhythm_to_val = {
        "l": 16,
        "b": 8,
        "w": 4,
        "h": 2,
        "q": 1,
        "e": 0.5,
        "s": 0.25,
        "t": 0.125,
        "x": 0.0625
    }
    return [rhythm_to_val[dur] for dur in rhythm]

# Generate small motif of 2-4 notes with simple rhythm patterns
def generate_motif(scale = "major") -> Motif:
    """
    Generate small motif of 2-4 notes with simple rhythm patterns.

    Args:
        scale (str): Scale to generate the motif in (e.g., "major", "minor" etc. ).

    Returns: A tuple containing a list of note degrees and a list of rhythm symbols corresponding to the generated motif.
        
    """
    degrees = SCALES[scale]
    length = random.randint(2, 4)

    rhythm = random.choices(["q", "e", "s"], k=length)
    notes = random.choices(degrees, k=length)

    motif = Motif(notes=notes, rhythm=rhythm)
    return motif

# Fill a bar with music starting with the motif
def motif_to_phrase(motif: Motif, key: Key, TIME_SIG) -> Phrase:
    num_beats = int(TIME_SIG.split("/")[0])

    # Place the motif at the beginning of the bar and fill the rest with random rhythm values
    rhythm = rhythm_to_values(motif.rhythm)
    random_rhythm = generate_rhythm(bars=1, time_sig=TIME_SIG, values=["q", "e", "s"])
    # Append random rhythm until full bar
    for val in random_rhythm:
        if sum(rhythm) + val <= num_beats:
            rhythm.append(val)
        else:
            break

    degrees = motif.notes
    
    while len(degrees) < len(rhythm):
        degrees.append(random.choice(SCALES[key.mode]))

    return Phrase(notes=degrees, rhythm = rhythm)

# Convert Motif to a Melody by filling in pitches and durations
def phrase_to_melody(phrase: Phrase, key: Key) -> Melody:
    notes = []
    for degree, dur in zip(phrase.notes, phrase.rhythm):
        pitch = key.degree_to_pitch(degree)
        note = Note(degree=degree, pitch=pitch, duration=dur)
        notes.append(note)

    return Melody(key=key, notes=notes, rhythm=dur)
