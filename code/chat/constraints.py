class Constraint:
    def is_valid(self, candidate, context):
        return True


class RangeConstraint(Constraint):
    def __init__(self, min_pitch, max_pitch):
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch

    def is_valid(self, candidate, context):
        if candidate.kind == "rest":
            return True
        return self.min_pitch <= candidate.pitch <= self.max_pitch


class StepConstraint(Constraint):
    def __init__(self, max_step=5):
        self.max_step = max_step

    def is_valid(self, candidate, context):
        prev = context.get("prev")

        if not prev or prev.kind == "rest" or candidate.kind == "rest":
            return True

        return abs(candidate.pitch - prev.pitch) <= self.max_step


class ChordConstraint(Constraint):
    def __init__(self, chord):
        self.chord = chord  # list of MIDI pitches

    def is_valid(self, candidate, context):
        if candidate.kind == "rest":
            return True

        return candidate.pitch % 12 in [p % 12 for p in self.chord]
