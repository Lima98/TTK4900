import music as ms
import lilyconvert as ly
import generator as gen

filename = "melody.ly"
filepath = "code/output/"
file = filepath + filename

key_name = "eb major"
time_sig = "4/4"
key = ms.build_key(key_name)

rhythm1 = gen.generate_rhythm(4, time_sig, ["q", "h", "q", "e"] )
rhythm2 = gen.generate_rhythm(4, time_sig, ["q", "h", "q", "e"] )
rhythm3 = gen.generate_rhythm(4, time_sig, ["q", "h", "q", "e"] )
rhythm4 = gen.generate_rhythm(4, time_sig, ["q", "h", "q", "e"] )
melody1 = gen.generate_notes(len(rhythm1), key)
melody2 = gen.generate_notes(len(rhythm2), key)
melody3 = gen.generate_notes(len(rhythm3), key)
melody4 = gen.generate_notes(len(rhythm4), key)

part1 = ly.note_and_rhythm(melody1, rhythm1) 
part2 = ly.note_and_rhythm(melody2, rhythm2) 
part3 = ly.note_and_rhythm(melody3, rhythm3) 
part4 = ly.note_and_rhythm(melody4, rhythm4) 

melody1 = ly.melody_to_lilypond(part1, "voiceOne", "treble")
melody2 = ly.melody_to_lilypond(part2, "voiceTwo", "treble")
melody3 = ly.melody_to_lilypond(part3, "voiceThree", "treble")
melody4 = ly.melody_to_lilypond(part4, "voiceFour", "treble")

parts = [melody1, melody2, melody3, melody4]

lilycode = ly.voices_to_lilypond(parts, key_name, time_sig)

ly.write_to_file(lilycode, file)
ly.generate_files(file, filepath)
ly.play(file)
