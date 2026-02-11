MAJOR_SCALE_STEPS = [2, 2, 1, 2, 2, 2, 1]
MINOR_SCALE_STEPS = [2, 1, 2, 2, 1, 2, 2]

def generate_major_scale(tonic_midi, steps=MAJOR_SCALE_STEPS):
    scale = [tonic_midi]
    for step in steps:
        scale.append(scale[-1] + step)
    return scale[:-1]  # 7 notes

def generate_minor_scale(tonic_midi, steps=MINOR_SCALE_STEPS):
    scale = [tonic_midi]
    for step in steps:
        scale.append(scale[-1] + step)
    return scale[:-1]  # 7 notes
