# Main module for generating melodies and rhythms using Melody/Note objects
import random
from core.music import Key, Note, Melody, SCALES

# Generate a random chromatic melody
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
    
    return Melody(notes = notes, key = key)

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

    return Melody(notes = melody_notes, key = key)

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

# Generate a rhythm pattern based on the time signature and allowed rhythm values
def generate_rhythm(bars=1, time_sig="4/4", values=["q"]):
    """
    Generate a rhythm pattern based on the time signature and allowed rhythm values.

    Args:
        bars (int): Number of bars to generate.
        time_sig (str): Time signature in the format "quantity/value" (e.g., "4/4", "3/4", "6/8").
        values (list): List of rhythm symbols (e.g., ["q", "e", "h"]) that can be used in the rhythm pattern.

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
