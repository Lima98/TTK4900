import random
import music as music
import constraints as constraints

allowedBeats = [0.5, 1]

def generate_phrase(key, bars = 8):
    phrase = music.Phrase(key, bars=[])

    motif = generate_motif(key)

    for bar in range(bars):
            if bar == bars - 1:
                phrase.bars.append(generate_better_bar(motif, phrase.key, position='end'))
            else:
                phrase.bars.append(generate_better_bar(motif, phrase.key, position='start'))

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
            beat = random.choice(allowedBeats)
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
            beat = random.choice(allowedBeats)
            if beatsLeft - beat < 0:
                continue
            beatsLeft -= beat
            bar.beats.append(beat)
            note = music.Note(degree=0, key=key, midiNum=tonic_pitch, duration=beat)
            bar.notes.append(note)

        
    return bar

def generate_better_bar(motif, key, position='start'):
    bar = music.Bar(key, beats=[], notes=[])
    centerKey = key + '3'
    beatsLeft = 4 - motif.getLength()

    # Start with motif
    for beat in motif.beats:
        bar.beats.append(beat)
    for note in motif.notes:
        bar.notes.append(note)

    # Fill the rest, moving by 2nds or 3rds from previous pitch
    prev_pitch = bar.notes[-1].midiNum if bar.notes else random.choice(constraints.getValidScale(centerKey))
    valid_intervals = [2, 3, -2, -3]
    
    if position == 'start':
        while beatsLeft > 0:
            beat = random.choice(allowedBeats)
            if beatsLeft - beat < 0:
                continue
            beatsLeft -= beat

            # Get next pitch by interval
            interval = random.choice(valid_intervals)
            candidate_pitch = prev_pitch + interval
            scale = constraints.getValidScale(centerKey)
            # Snap to nearest valid scale note
            candidate_pitch = min(scale, key=lambda x: abs(x - candidate_pitch))
            prev_pitch = candidate_pitch

            bar.beats.append(beat)
            note = music.Note(degree=candidate_pitch % 12, key=music.getPitchClass(candidate_pitch), midiNum=candidate_pitch, duration=beat)
            bar.notes.append(note)

    elif position == 'end':
        # Fill the rest of the bar with the tonic note of the key, meaning the 1 scale degree
        tonic_pitch = music.KEYS.index(key) + 12 * 4  # Get the MIDI number for the tonic note in the 4th octave
        while beatsLeft > 0:
            beat = random.choice(allowedBeats)
            if beatsLeft - beat < 0:
                continue
            beatsLeft -= beat
            bar.beats.append(beat)
            note = music.Note(degree=0, key=key, midiNum=tonic_pitch, duration=beat)
            bar.notes.append(note)

    return bar

def generate_motif(key):
    # Generate a motif of 3-5 notes with a max length of 3 beats
    motif = music.Motif(key=key, beats=[], notes=[])
    num_notes = random.randint(3, 5)
    sum_beats = 0
    centerKey = key + '3'
    maxLength = random.choice([1, 2, 3])

    # Ensure the motif starts on tonic or dominant
    tonic_degree = 0
    dominant_degree = 7 % 12
    scale = constraints.getValidScale(centerKey)
    tonic_pitches = [p for p in scale if p % 12 == tonic_degree]
    dominant_pitches = [p for p in scale if p % 12 == dominant_degree]
    first_pitch = random.choice(tonic_pitches + dominant_pitches)

    # First note
    beat = random.choice(allowedBeats)
    motif.beats.append(beat)
    sum_beats += beat
    note = music.Note(degree=first_pitch % 12, key=music.getPitchClass(first_pitch), midiNum=first_pitch, duration=beat)
    motif.notes.append(note)

    for _ in range(1, num_notes):
        beat = random.choice(allowedBeats)
        if sum_beats + beat > maxLength:
            continue
        sum_beats += beat
        motif.beats.append(beat)
        pitch = random.choice(scale)
        note = music.Note(degree=pitch % 12, key=music.getPitchClass(pitch), midiNum=pitch, duration=beat)
        motif.notes.append(note)
    return motif
