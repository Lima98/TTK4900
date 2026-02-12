import random

# Mapping scale degrees to semitone offsets from tonic
DEGREE_TO_OFFSET = {
    "1": 0, "2": 2, "3": 4, "4": 5, "5": 7, "6": 9, "7": 11,
    "4s": 6, "2s": 3, "5s": 8, "7s": 12, "3s": 5, "6s": 10,
    "2b": 1, "3b": 3, "4b": 4, "5b": 6, "6b": 8, "7b": 10
}

# C major scale for reference
NOTE_NAMES = ['c', 'd', 'e', 'f', 'g', 'a', 'b']

def generate_melody(length=8):
    degrees = ["1", "2", "3", "4", "5", "6", "7", "4s", "7b"]
    return [random.choice(degrees) for _ in range(length)]

def degree_to_note(degree, tonic="c"):
    # Find tonic index
    tonic_index = NOTE_NAMES.index(tonic)
    offset = DEGREE_TO_OFFSET[degree]
    note_index = (tonic_index + offset) % 12
    # Map to note name (simplified, only for C major)
    # For full chromatic, expand NOTE_NAMES and handle sharps/flats
    return NOTE_NAMES[note_index % 7]  # Simplified

def melody_to_lilypond(melody, tonic="c"):
    notes = [degree_to_note(degree, tonic) for degree in melody]
    return "\\version \"2.24.2\"\n{ " + " ".join(notes) + " }"

if __name__ == "__main__":
    melody = generate_melody()
    lilypond = melody_to_lilypond(melody, tonic="c")
    with open("melody.ly", "w") as f:
        f.write(lilypond)
