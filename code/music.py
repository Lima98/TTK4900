class Song:
    def __init__(self, sections):
        self.sections = sections

class Section:
    def __init__(self, phrases):
        self.phrases = phrases

class Phrase:
    def __init__(self, melodies):
        self.melodies = melodies

class Melody:
    def __init__(self, bars):
        self.motifs = bars

class Bar:
    def __init__(self, beats, notes=[]):
        self.beats = beats
        self.notes = notes

class Note:
    def __init__(self, octave, degree, duration, rest=True):
        self.octave = octave
        self.degree = degree
        self.duration = duration
        self.rest = rest

