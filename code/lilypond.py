import music
import subprocess
import os

def octaveToLilyPond(octave):
    if octave == 0:
        return ",,,"
    elif octave == 1:
        return ",,"
    elif octave == 2:
        return ","
    elif octave == 3:
        return ""
    elif octave == 4:
        return "'"
    elif octave == 5:
        return "''"
    elif octave == 6:
        return "'''"
    else:
        raise ValueError("Octave out of range (0-6)")

def generateLilyPond(phrase, filename="output.ly"):
    key = phrase.key.lower()
    lilypond_str = "\\version \"2.20.0\"\n\n"
    lilypond_str += "\\language \"english\"\n\n"
    lilypond_str += "\\score {\n"
    lilypond_str += "  \\new Staff {\n"
    lilypond_str += "    \\clef \"treble_8\"\n"
    lilypond_str += f"    \\key {key} \\major\n"
    lilypond_str += "    \\time 4/4\n"
    
    for bar in phrase.bars:
        for note in bar.notes:
            pitch = music.getPitchClass(note.midiNum).lower()
            duration = int(4 / note.duration)
            octave = note.midiNum // 12 - 1
            octave_str = octaveToLilyPond(octave)
            lilypond_str += f"    {pitch}{octave_str}{duration} "
        lilypond_str += "|\n" 
    
    lilypond_str += "  }\n"
    lilypond_str += "   \\midi{}\n"
    lilypond_str += "   \\layout{}\n"
    lilypond_str += "}\n"

    with open("output.ly", "w") as file:
        file.write(lilypond_str)

def play(filename):
    subprocess.run(["lilypond", filename])
    midi_file = filename.replace('.ly', '.midi')
    audio_file = filename.replace('.ly', '.wav')

    if os.path.exists(midi_file):
        subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
        subprocess.run(["afplay", audio_file])
    else:
        print(f"MIDI file not found: {midi_file}")

