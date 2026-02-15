import random
scale_degrees = ["1", "2", "3", "4", "5", "6", "7"]

# Generate random melody on scale degrees
# Handling of music concepts. Melodies, rhythm, keys etc... 

# Generate notes in a melody
def generate_notes(length=8):
    melody = [random.choice(scale_degrees) for _ in range(length)]
    
    return melody 

# Generate a random rhythm pattern and add to the melody
def add_rhythm(melody):
    out = []
    for note in melody:
        rhythm = random.choice(["2", "4", "8"])
        out.append(f"{note}{rhythm} ")
    
    return out

# Convert scale degrees to notes (assuming C major for simplicity)
def melody_to_notes(melody):
    degree_to_note = {
        "1": "c",
        "2": "d",
        "3": "e",
        "4": "f",
        "5": "g",
        "6": "a",
        "7": "b"
    }
    
    notes = [degree_to_note[degree] for degree in melody]
    
    return notes

