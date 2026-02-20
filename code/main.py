import music as ms
import lilyconvert as ly

filename = "melody.ly"
filepath = "code/output/"
file = filepath + filename

key_name = "eb major"
key = ms.build_key(key_name)

melody = ms.generate_notes(8, key)
melody1 = ly.melody_to_lilypond(melody, "voiceOne", "treble")

melody = ms.generate_notes(8, key)
melody2 = ly.melody_to_lilypond(melody, "voiceTwo", "treble")

parts = [melody1, melody2]

lilycode = ly.voices_to_lilypond(parts, key_name, "4/4")

ly.write_to_file(lilycode, file)
ly.generate_files(file, filepath)
ly.play(file)
