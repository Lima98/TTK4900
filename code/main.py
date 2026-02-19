import music as ms
import lilyconvert as ly

filename = "melody.ly"
filepath = "code/output/"
file = filepath + filename

# TODO: Melody generator that does both in one

key_name = "eb major"
key = ms.build_key(key_name)
melody = ms.generate_notes(1000, key)
print(melody)

lilycode = ly.melody_to_lilypond(melody, key_name, "4/4")
ly.write_to_file(lilycode, file)
ly.generate_files(file, filepath)
ly.play(file)

print(ms.generate_random_notes(16))

# print("=== Generate Rhythm ===")
# rhythm1 = ms.generate_rhythm(2, 4, ["s"]) 
# rhythm2 = ms.generate_rhythm(1, 4, ["e", "s"])
# print(f"Rhythm 1: {rhythm1}")
# print(f"Rhythm 2: {rhythm2}")
# rhythm = rhythm1 + rhythm2 + rhythm1 + rhythm1
# print(f"Rhythm: {rhythm}")
#
# print("=== Generate Notes ===")
# # notes = ms.generate_notes(len(rhythm))
# notes = ms.generate_notes(len(rhythm), phrygian_dominant) # TEST: phrygian_dominant
# print(notes)
#
# print("=== Rhythm to lilypond ===")
# print(rhythm)
# rhythm = ly.beat_to_duration(rhythm)
# print(rhythm)
#
# print("=== Scale degree to note ===")
# melody = ms.melody_to_notes(notes)
# print(melody)
#
#
#
# print("=== Notes and rhythm to lilypond ===")
# melody = ly.note_and_rhythm(melody, rhythm)
# print(melody)
#
# # Generate LilyPond code from generated melody
# print("=== Generating lilypond output ===")
# lilycode = ly.melody_to_lilypond(melody)
# ly.write_to_file(lilycode, file)
# ly.generate_files(file, filepath)
# ly.play(file)

