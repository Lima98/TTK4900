import random

def generate_rhythm(length=8):
    # Simple rhythm: quarter (1) or eighth (0.5) notes
    durations = []
    while sum(durations) < length:
        d = random.choice([0.5, 1])
        if sum(durations) + d > length:
            d = length - sum(durations)
        durations.append(d)
    return durations
