import music

def generateLilyPond(phrase):
    key = phrase.key.lower()
    lilypond_str = "\\version \"2.20.0\"\n\n"
    lilypond_str += "\\score {\n"
    lilypond_str += "  \\new Staff {\n"
    lilypond_str += "    \\clef \"treble_8\"\n"
    lilypond_str += f"    \\key {key} \\major\n"
    lilypond_str += "    \\time 4/4\n"
    
    for bar in phrase.bars:
        for note in bar.notes:
            pitch = music.getPitchClass(note.midiNum).lower()
            duration = int(4 / note.duration)
            lilypond_str += f"    {pitch}{duration} "
        lilypond_str += "|\n" 
    
    lilypond_str += "  }\n"
    lilypond_str += "   \\midi{}\n"
    lilypond_str += "}\n"

    with open("output.ly", "w") as file:
        file.write(lilypond_str)
