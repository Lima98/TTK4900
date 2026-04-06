class Event:
    def __init__(self, kind, duration, pitch=None):
        self.kind = kind        # "note" or "rest"
        self.duration = duration
        self.pitch = pitch      # MIDI number


class Voice:
    def __init__(self, name):
        self.name = name
        self.events = []

    def last_event(self):
        return self.events[-1] if self.events else None


class Bar:
    def __init__(self, beats=4):
        self.beats = beats
        self.voices = {
            "L": Voice("Lead"),
            "B": Voice("Bass"),
        }


class Score:
    def __init__(self):
        self.bars = []
