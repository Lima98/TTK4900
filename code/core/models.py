# Musical models for structuring melodies

from core.music import Note


class Motif:
    def __init__(self, notes=None, rhythm=None):
        self.notes = notes
        self.rhythm = rhythm

class Phrase:
    motifs = list[Motif]

class Section:
    phrases = list[Phrase]

class Form:
    sections = list[Section]
