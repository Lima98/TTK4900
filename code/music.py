# Handling of music concepts. Melodies, rhythm, keys etc... 
import random

# Scales
scale_degrees = ["1", "2", "3", "4", "5", "6", "7"]
scale_degrees_full = ["1","b2" "2","b3", "3", "4", "s4", "5", "b6", "6", "b7", "7"]

# Generate random melody on scale degrees

# Generate notes in a melody NOTE: Not used anymore
def generate_random_notes(length=8):
    melody = [random.choice(scale_degrees_full) for _ in range(length)]
    return melody 

# Generate notes based on intervals
def generate_notes(notes = 4, scale=scale_degrees):
    intervals   =   [-2, -1, 0, 1, 2] # Only 2nds and 3rds for now
    melody      =   []
    current     =   0
    
    for _ in range(notes):
        val     =   random.choice(intervals)
        current +=  val
        
        if current < 0:
                current += 7
        if current > 6:
            current -= 7

        note    =   scale[current]
        melody.append(note)

    return melody

# Generate a bar of random rhythm pattern in a given Time Signature
def generate_rhythm(timeSig = 4):
    values  =   [4, 2, 1, 0.5]
    rhythm  =   []
    tot     =   0
    
    while tot < timeSig:
        choices = [v for v in values if tot + v <= timeSig]
        val     = random.choice(choices)
        rhythm.append(val)
        tot     += val
    return rhythm

# Convert scale degrees to notes (assuming C major for simplicity)
# TODO: Implement all keys in a smart way, maybe .csv or something
def melody_to_notes(melody):
    degree_to_note = {
        "1": "c",
        "b2": "df",
        "2": "d",
        "b3": "ef",
        "3": "e",
        "4": "f",
        "s4": "fs",
        "5": "g",
        "b6": "af",
        "6": "a",
        "b7": "bf",
        "7": "b"
    }
    
    notes = [degree_to_note[degree] for degree in melody]
    
    return notes

# Diatonic transposition TODO: Implement this
def transpose(melody, interval=0):

    return
