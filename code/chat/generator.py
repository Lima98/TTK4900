import random
from model import Event, Bar
from constraints import RangeConstraint, StepConstraint, ChordConstraint


SCALE = [60, 62, 64, 65, 67, 69, 71]  # C major


def generate_candidates(prev):
    candidates = []

    # rests
    if random.random() < 0.2:
        candidates.append(Event("rest", 1))

    # notes
    if prev and prev.kind == "note":
        for step in [-2, -1, 0, 1, 2]:
            candidates.append(Event("note", 1, prev.pitch + step))
    else:
        for p in SCALE:
            candidates.append(Event("note", 1, p))

    return candidates


def generate_event(voice, constraints):
    prev = voice.last_event()

    context = {
        "prev": prev,
        "constraints": constraints
    }

    candidates = generate_candidates(prev)

    valid = [
        c for c in candidates
        if all(con.is_valid(c, context) for con in constraints)
    ]

    if not valid:
        raise Exception("Dead end")

    return random.choice(valid)


def generate_bar():
    bar = Bar()

    lead_constraints = [
        RangeConstraint(60, 80),
        StepConstraint(5),
    ]

    bass_constraints = [
        RangeConstraint(40, 60),
        StepConstraint(7),
    ]

    for _ in range(bar.beats):
        # Lead
        lead_event = generate_event(bar.voices["L"], lead_constraints)
        bar.voices["L"].events.append(lead_event)

        # Bass (simple root-based harmony)
        chord = [60, 64, 67]
        bass_constraints_with_chord = bass_constraints + [ChordConstraint(chord)]

        bass_event = generate_event(bar.voices["B"], bass_constraints_with_chord)
        bar.voices["B"].events.append(bass_event)

    return bar


def generate_score(num_bars=4):
    from model import Score
    score = Score()

    for _ in range(num_bars):
        score.bars.append(generate_bar())

    return score
