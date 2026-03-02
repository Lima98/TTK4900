# Musical models for structuring melodies

from core.music import Note


class Motif:
    def __init__(self, notes, rhythm):
        self.notes = notes
        self.rhythm = rhythm

class Phrase:
    def __init__(self, notes, rhythm):
        self.notes = notes
        self.rhythm = rhythm

class Section:
    phrases = list[Phrase]

class Form:
    sections = list[Section]
