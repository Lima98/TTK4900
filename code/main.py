import music as ms
import lilyconvert as ly

filename = "melody.ly"

# Generate a random melody and convert to notes
melody = ms.add_rhythm(ms.melody_to_notes(ms.generate_notes(16)))
print(melody)

# Generate LilyPond code from generated melody
lilycode = ly.melody_to_lilypond(melody)
ly.write_to_file(lilycode, filename)
ly.generate_files(filename)

