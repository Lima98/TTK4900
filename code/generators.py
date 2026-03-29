import random
import music as music
import constraints as constraints

def generate_phrase(key, bars = 4):
    phrase = music.Phrase(key, bars=[])

    motif = generate_motif()

    for bar in range(bars):
            if bar == bars - 1:
                phrase.bars.append(generate_bar(motif, key, position='end'))
            else:
                phrase.bars.append(generate_bar(motif, key, position='start'))

    return phrase

def generate_bar(motif, key, position='start'):
    bar = music.Bar(key, beats=[], notes=[])

    beatsLeft = 4
    beatsleft = beatsLeft - motif.getLength()

    if position == 'start':
        for beat in motif.beats:
            bar.beats.append(beat)
        for note in motif.notes:
            bar.notes.append(note)
        pass
        while beatsleft > 0:
            beat = random.choice([0.25, 0.5, 1])
            if beatsleft - beat < 0:
                break
            beatsleft -= beat
            bar.beats.append(beat)
            pitch = random.choice(constraints.getValidScale())
            note = music.Note(degree=pitch % 12, key=music.getPitchClass(pitch), midiNum=pitch, duration=beat)
            bar.notes.append(note)

    if position == 'middle':
        pass

    elif position == 'end':
        for beat in motif.beats:
            bar.beats.append(beat)
        for note in motif.notes:
            bar.notes.append(note)
        # Fill the rest of the bar with the tonic note of the key, meaning the 1 scale degree
        tonic_pitch = music.KEYS.index(key) + 12 * 4  # Get the MIDI number for the tonic note in the 4th octave
        while beatsleft > 0:
            beat = random.choice([0.25, 0.5, 1])
            if beatsleft - beat < 0:
                break
            beatsleft -= beat
            bar.beats.append(beat)
            note = music.Note(degree=0, key=key, midiNum=tonic_pitch, duration=beat)
            bar.notes.append(note)

        
    return bar
def generate_motif():
    # Generate a motif of 2-5 notes with a max length of 3 beats
    randKey = music.KEYS[random.randint(0, 11)]
    motif = music.Motif(key=randKey, beats=[], notes=[])
    motif.key = randKey
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
