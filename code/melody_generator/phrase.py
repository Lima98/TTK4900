import random

def generate_phrase(scale, rhythm, resolve=False):
    notes = []
    for i in range(len(rhythm)):
        if resolve and i == len(rhythm) - 1:
            notes.append(scale[0])  # Tonic for resolution
        else:
            notes.append(random.choice(scale))
    return list(zip(notes, rhythm))


