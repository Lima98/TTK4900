import music as ms
import lilyconvert as ly

file = "melody.ly"
filepath = "code/output/"
filename = filepath + file

# Testing custom scales
phrygian_dominant = ["1", "b2", "3", "4", "5", "b6", "b7"]

print("=== Rhythm ===")
rhythm1 = ms.generate_rhythm(4)
rhythm2 = ms.generate_rhythm(4)
print(rhythm1)
print(rhythm2)
rhythm = rhythm1 + rhythm2 + rhythm1 + rhythm1

print(rhythm)
rhythm = ly.beat_to_duration(rhythm)
print(rhythm)
print("=== === === === ")

print("=== Notes ===")
notes = ms.generate_notes(len(rhythm))
# notes = ms.generate_notes(len(rhythm1), phrygian_dominant)
print(notes)

melody = ms.melody_to_notes(notes)
print(melody)
print("=== === === ===")



print("=== Melody ===")
melody = ly.note_and_rhythm(melody, rhythm)
print(melody)
print("=== === === === ")

# Generate LilyPond code from generated melody
print("=== Generating lilypond output ===")
lilycode = ly.melody_to_lilypond(melody)
ly.write_to_file(lilycode, filename)
ly.generate_files(filename)

