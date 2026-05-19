import random

###########################################
# YOUR DATA STRUCTURES
###########################################

class Note:
    def __init__(self, octave, degree, duration, rest=False):
        self.octave = octave
        self.degree = degree
        self.duration = duration
        self.rest = rest

    def __repr__(self):
        if self.rest:
            return f"Rest({self.duration})"
        return f"N({self.degree}, {self.duration})"


class Bar:
    def __init__(self, beats=4):
        self.beats = beats
        self.notes = []

###########################################
# RHYTHM STATES
###########################################

class RhythmState:

    def __init__(self, duration=None, rest=False, start=False):
        self.duration = duration
        self.rest = rest
        self.start = start

    def is_hold(self):
        return not self.start


HOLD = RhythmState()

RHYTHM_STATES = [
    RhythmState(4, start=True),
    RhythmState(2, start=True),
    RhythmState(1, start=True),
    RhythmState(2, start=True, rest=True),
    RhythmState(1, start=True, rest=True),
    HOLD
]

###########################################
# RHYTHM WFC
###########################################

SLOTS = 16

def generate_rhythm():

    wave = [set(RHYTHM_STATES) for _ in range(SLOTS)]

    wave[0] = {s for s in RHYTHM_STATES if s.start}

    collapsed = [None] * SLOTS

    while None in collapsed:

        idx = min(
            (i for i in range(SLOTS) if collapsed[i] is None),
            key=lambda i: len(wave[i])
        )

        state = choose_rhythm_state(wave[idx], idx)

        collapsed[idx] = state
        wave[idx] = {state}

        propagate_rhythm(wave, collapsed, idx, state)

    return collapsed


def choose_rhythm_state(states, slot):

    heavy = slot % 4 == 0

    weights = []

    for s in states:

        if not s.start:
            weights.append(0.1)
            continue

        if heavy:
            if s.duration == 4:
                weights.append(3)
            elif s.duration == 2:
                weights.append(2)
            else:
                weights.append(1)
        else:
            if s.duration == 1:
                weights.append(3)
            elif s.duration == 2:
                weights.append(2)
            else:
                weights.append(0.5)

    return random.choices(list(states), weights=weights)[0]


def propagate_rhythm(wave, collapsed, idx, state):

    if not state.start:
        return

    for i in range(1, state.duration):

        if idx + i >= SLOTS:
            return

        collapsed[idx + i] = HOLD
        wave[idx + i] = {HOLD}

###########################################
# CONVERT RHYTHM → NOTES
###########################################

def rhythm_to_notes(slots):

    notes = []
    i = 0

    while i < len(slots):

        s = slots[i]

        if s.start:

            duration = s.duration / 4

            notes.append(
                Note(
                    octave=3,
                    degree=None,
                    duration=duration,
                    rest=s.rest
                )
            )

            i += s.duration
        else:
            i += 1

    return notes

###########################################
# MOTIF SYSTEM
###########################################

class Motif:

    def __init__(self, intervals):
        self.intervals = intervals

    def length(self):
        return len(self.intervals)


def transpose_motif(motif, start_degree):

    melody = [start_degree]

    for i in motif.intervals:
        melody.append(melody[-1] + i)

    return melody


###########################################
# PITCH WFC
###########################################

DEGREES = [1,2,3,4,5,6,7]

def pitch_wfc(notes, motif=None):

    indices = [i for i,n in enumerate(notes) if not n.rest]

    wave = {i:set(DEGREES) for i in indices}

    # phrase ending constraint
    last = indices[-1]
    wave[last] = {1,5}

    collapsed = {}

    while len(collapsed) < len(indices):

        idx = min(
            (i for i in indices if i not in collapsed),
            key=lambda i: len(wave[i])
        )

        degree = choose_pitch(wave[idx], idx, collapsed, notes)

        collapsed[idx] = degree

        propagate_pitch(wave, idx, degree)

    for i,d in collapsed.items():
        notes[i].degree = d


def choose_pitch(options, idx, collapsed, notes):

    weights = []

    prev_idx = None

    for i in reversed(range(idx)):
        if i in collapsed:
            prev_idx = i
            break

    for o in options:

        weight = 1

        if prev_idx is not None:

            interval = abs(o - collapsed[prev_idx])

            if interval == 0:
                weight *= 1.5
            elif interval == 1:
                weight *= 4
            elif interval == 2:
                weight *= 3
            elif interval == 3:
                weight *= 1
            else:
                weight *= 0.2

        weights.append(weight)

    return random.choices(list(options), weights=weights)[0]


def propagate_pitch(wave, idx, degree):

    for k in wave:

        if k > idx:
            wave[k] = {d for d in wave[k] if abs(d-degree) <= 4}

###########################################
# MOTIF INSERTION
###########################################

def apply_motif(notes):

    motif = Motif([1,-1,2])  # example motif

    start_positions = [0, 3]

    for start in start_positions:

        end = start + motif.length()

        if end >= len(notes):
            continue

        base = random.choice(DEGREES)

        motif_notes = transpose_motif(motif, base)

        for i,val in enumerate(motif_notes):

            if notes[start+i].rest:
                continue

            notes[start+i].degree = max(1,min(7,val))


###########################################
# GENERATOR
###########################################

def generate_bar():

    bar = Bar()

    rhythm = generate_rhythm()

    notes = rhythm_to_notes(rhythm)

    pitch_wfc(notes)

    apply_motif(notes)

    bar.notes = notes

    return bar

###########################################
# TEST
###########################################

if __name__ == "__main__":

    for _ in range(5):

        bar = generate_bar()

        print(bar.notes)
