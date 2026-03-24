import music
import random

#   Get notes in the scale of the root key
def getValidScale(root_note = music.getMidiNum('A4') + random.randint(-24, -12), scale_type=music.MAJOR_SCALE) -> list:
    root_key = music.KEYS[root_note % 12]
    scale = []

    for interval in scale_type:
        scale.append((root_note + interval))

    # Prepend the scale an octave lower and append the octave higher to the scale
    scale = [note - 12 for note in scale] + scale + [note + 12 for note in scale]

    #   Get a valid range using the max register and upper/lower bounds
    start_index = random.randint(0, len(scale) - music.MAX_REGISTER - 1)
    valid_notes = scale[start_index : start_index + music.MAX_REGISTER]

    while valid_notes[-1] > music.UPPER_BOUND or valid_notes[0] < music.LOWER_BOUND:
        start_index = random.randint(0, len(scale) - music.MAX_REGISTER - 1)
        valid_notes = scale[start_index : start_index + music.MAX_REGISTER]

    return valid_notes
