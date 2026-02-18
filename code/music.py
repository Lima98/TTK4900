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
def generate_notes(notes = 4, scale=scale_degrees, ):
    intervals   =   [-2, -1, 0, 1, 2] # only 2nds and 3rds for now
    melody      =   []
    current     =   0
    
    for _ in range(notes):
        val     =   random.choice(intervals)
        current +=  val
        
        if current < 0:
                current += len(scale) 
        if current > 6:
            current -= len(scale)

        note    =   scale[current]
        melody.append(note)

    return melody

# generate a numbers of bars of random rhythm pattern in a given time signature
def generate_rhythm(bars = 1, notesPerBar = 4, values = ["q"]):
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
    rhythm_to_val = {
            "b": 8,
            "w": 4,
            "h": 2,
            "q": 1,
            "e": 0.5,
            "s": 0.25,
            "t": 0.125,
            "x": 0.0625
            }
    values = [rhythm_to_val[dur] for dur in rhythm]

    return values


# Convert scale degrees to notes (assuming C major for simplicity)
# TODO: implement all keys in a smart way, maybe .csv or something
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

# TODO: Implement this
# Diatonic transposition using the scale degrees
def ttranspose(melody, interval=0):
    transposed_melody = []
    for note in melody:
        if note in scale_degrees_full:
            index = scale_degrees_full.index(note)
            transposed_index = (index + interval) % len(scale_degrees_full)
            transposed_note = scale_degrees_full[transposed_index]
            transposed_melody.append(transposed_note)
        else:
            transposed_melody.append(note)  # If the note is not in the scale, keep it unchanged
    return transposed_melody

def transpose(melody, interval=0):
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
