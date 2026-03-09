class chord:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __str__(self):
        return f"{self.name} chord: {', '.join(self.notes)}"

    def valid_transition():


chords_major = [
    chord("I", ["1", "3", "5"]),
    chord("ii", ["2", "4", "6"]),
    chord("iii", ["3", "5", "7"]),
    chord("IV", ["4", "6", "1"]),
    chord("V", ["5", "7", "2"]),
    chord("vi", ["6", "1", "3"]),
    chord("vii°", ["7", "2", "4"])
]

chords_minor = [
    chord("i", ["1", "b3", "5"]),
    chord("ii°", ["2", "4", "b6"]),
    chord("III", ["b3", "5", "b7"]),
    chord("iv", ["4", "b6", "1"]),
    chord("v", ["5", "b7", "2"]),
    chord("VI", ["b6", "1", "b3"]),
    chord("VII", ["b7", "2", "4"])
]
