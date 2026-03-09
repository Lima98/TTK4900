# Generate different musical structures

import music
import random


def generate_bar(beats=4) -> music.Bar:
    output = music.Bar(4)

    used_beats = 0
    rest_chance = 0.2
    beat_values = [4, 2, 1, 0.5, 0.25]
    weight_heavy = [0.5, 1, 2, 2, 0.4]
    weight_light = [0.1, 0.5, 2, 4, 3]
    
    while used_beats < beats:
        if used_beats % 1 == 0:
            value = random.choices(beat_values, weights=weight_heavy)
            if used_beats + value[0] > beats:
                continue
            output.notes.append(music.Note(octave = 3, duration=value[0], degree=choose_note(rest_chance, heavy=True)))
            used_beats += value[0]
        else:
            value = random.choices(beat_values, weights=weight_light)
            if used_beats + value[0] > beats:
                continue
            output.notes.append(music.Note(octave = 3, duration=value[0], degree=choose_note(rest_chance, heavy=False)))
            used_beats += value[0]
        
    return output

                                       
def choose_note(rest_chance, heavy=True):

    note_values = ["1", "2", "3", "4", "5", "6", "7"]
    weight_heavy = [1, 0.2, 0.6, 0.2, 0.7, 0.3, 0.05]
    weight_light = [0.5, 0.5, 0.5, 1, 0.5, 1, 1]

    if check_rest(rest_chance):
        return None
    else:
        if heavy:
            return random.choices(note_values, weights=weight_heavy)[0]
        else:
            return random.choices(note_values, weights=weight_light)[0]
        

def check_rest(rest_chance):
    if random.random() < rest_chance:
        return True
    return False

