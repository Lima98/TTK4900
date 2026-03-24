import generators as gen 

KEYS = ['C', 'Df', 'D', 'Ef', 'E', 'F', 'Fs', 'G', 'Af', 'A', 'Bf', 'B']

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]

def getPitchClass(midiNum):
    return KEYS[midiNum % 12]

#   Get MIDI num using "Af4" format
def getMidiNum(note):
    octave = int(note[-1])
    key = note[:-1]
    return KEYS.index(key) + 12 * (octave + 1)

#   Max range of a melody of a single instrument, in semitones
MAX_REGISTER = 11 
UPPER_BOUND = getMidiNum('A4') 
LOWER_BOUND = getMidiNum('F2')

class Note:
    def __init__(self, degree, key, midiNum, duration):
        self.degree = degree
        self.key = key
        self.midiNum = midiNum
        self.duration = duration

class Motif:
    def __init__(self, key, beats=[], notes=[]):
        self.beats = beats
        self.notes = notes

    def getLength(self):
        length = 0
        for beat in self.beats:
            length += beat
        return length

class Bar:
    def __init__(self, key, beats, notes=[]):
        self.beats = beats
        self.notes = notes

class Phrase:
    def __init__(self, key, bars):
        self.melodies = bars
