import music as ms
import lilyconvert as ly

file = "melody.ly"
filepath = "code/output/"
filename = filepath + file

# Testing custom scales TEST: Example of custom scale
phrygian_dominant = ["1", "b2", "3", "4", "5", "b6", "b7"]

print("=== Generate Rhythm ===")
rhythm1 = ms.generate_rhythm(2, 2)
rhythm2 = ms.generate_rhythm(1, 2)
print(f"Rhythm 1: {rhythm1}")
print(f"Rhythm 2: {rhythm2}")
rhythm = rhythm1 + rhythm2 + rhythm1 + rhythm1
print(f"Rhythm: {rhythm}")

print("=== Generate Notes ===")
# notes = ms.generate_notes(len(rhythm))
notes = ms.generate_notes(len(rhythm), phrygian_dominant) # TEST: phrygian_dominant
print(notes)

print("=== Rhythm to lilypond ===")
print(rhythm)
rhythm = ly.beat_to_duration(rhythm)
print(rhythm)


print("=== Scale degree to note ===")
melody = ms.melody_to_notes(notes)
print(melody)



print("=== Notes and rhythm to lilypond ===")
melody = ly.note_and_rhythm(melody, rhythm)
print(melody)

# Generate LilyPond code from generated melody
print("=== Generating lilypond output ===")
lilycode = ly.melody_to_lilypond(melody)
ly.write_to_file(lilycode, filename)
ly.generate_files(filename, filepath)
ly.play(filename)

