class Melody:
    def __init__(self, notes, key, tags=None):
        self.notes = notes         # list of Note objects
        self.key = key             # Key object
        self.tags = tags or {}     # e.g., {"style": "barbershop", "section": "verse"}

    def to_scale_degrees(self):
        # Returns list of scale degree representations
        pass

    def to_pitches(self):
        # Converts degrees to absolute pitches in the current key
        pass


class Note:
    def __init__(self, pitch=None, degree=None, duration=1):
        self.pitch = pitch         # Absolute pitch (e.g., 'c4')
        self.degree = degree       # Scale degree (1-7, maybe with accidentals)
        self.duration = duration   # Quarter note, etc.

    def is_abstract(self):
        return self.degree is not None

    def is_concrete(self):
        return self.pitch is not None


class Key:
    def __init__(self, tonic, mode='major'):
        self.tonic = tonic         # e.g., 'C'
        self.mode = mode           # 'major', 'minor', 'dorian', etc.

    def degree_to_pitch(self, degree):
        # Convert scale degree to pitch in this key
        pass
