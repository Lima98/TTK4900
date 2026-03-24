import random
import music as music
import constraints as constraints

def generate_phrase():
    pass

def generate_bar():
    pass

def generate_motif():
    # Generate a motif of 2-5 notes with a max length of 3 beats
    motif = music.Motif(key=music.KEYS[random.randint(0, 11)], beats=[], notes=[])
    num_notes = random.randint(2, 5)
    sum_beats = 0

    for _ in range(num_notes):
        beat = random.choice([0.25, 0.5, 1])
        if sum_beats + beat >= 3:
            break
        sum_beats += beat
        motif.beats.append(beat)
        pitch = random.choice(constraints.getValidScale())
        note = music.Note(degree=pitch % 12, key=music.getPitchClass(pitch), midiNum=pitch, duration=beat)
        motif.notes.append(note)
    return motif
