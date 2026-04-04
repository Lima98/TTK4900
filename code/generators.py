import random
import music as music
import constraints as constraints

def generate_phrase(key, bars = 8):
    phrase = music.Phrase(key, bars=[])

    motif = generate_motif(key)

    for bar in range(bars):
            if bar == bars - 1:
                phrase.bars.append(generate_bar(motif, phrase.key, position='end'))
            else:
                phrase.bars.append(generate_bar(motif, phrase.key, position='start'))

    return phrase

def generate_bar(motif, key, position='start'):
    bar = music.Bar(key, beats=[], notes=[])
    centerKey = key + '3'

    beatsLeft = 4
    beatsLeft = beatsLeft - motif.getLength()

    if position == 'start':
        for beat in motif.beats:
            bar.beats.append(beat)
        for note in motif.notes:
            bar.notes.append(note)
        pass
        while beatsLeft > 0:
            beat = random.choice([0.25, 0.5, 1])
            if beatsLeft - beat < 0:
                continue
            beatsLeft -= beat
            bar.beats.append(beat)
            pitch = random.choice(constraints.getValidScale(root_note=centerKey))
            note = music.Note(degree=pitch % 12, key=music.getPitchClass(pitch), midiNum=pitch, duration=beat)
            bar.notes.append(note)

    if position == 'middle':
        # TODO: Not yet implemented, but the idea is to randomly place the motif somewhere in the middle of the bar and fill the rest with random notes
        pass

    elif position == 'end':
        for beat in motif.beats:
            bar.beats.append(beat)
        for note in motif.notes:
            bar.notes.append(note)
        # Fill the rest of the bar with the tonic note of the key, meaning the 1 scale degree
        tonic_pitch = music.KEYS.index(key) + 12 * 4  # Get the MIDI number for the tonic note in the 4th octave
        while beatsLeft > 0:
            beat = random.choice([0.25, 0.5, 1])
            if beatsLeft - beat < 0:
                break
            beatsLeft -= beat
            bar.beats.append(beat)
            note = music.Note(degree=0, key=key, midiNum=tonic_pitch, duration=beat)
            bar.notes.append(note)

        
    return bar

def generate_motif(key):
    # Generate a motif of 2-5 notes with a max length of 3 beats
    motif = music.Motif(key=key, beats=[], notes=[])
    num_notes = random.randint(2, 5)
    sum_beats = 0
    centerKey = key + '3'

    for _ in range(num_notes):
        beat = random.choice([0.25, 0.5, 1])
        if sum_beats + beat >= 3:
            break
        sum_beats += beat
        motif.beats.append(beat)
        pitch = random.choice(constraints.getValidScale(centerKey))
        note = music.Note(degree=pitch % 12, key=music.getPitchClass(pitch), midiNum=pitch, duration=beat)
        motif.notes.append(note)
    return motif
