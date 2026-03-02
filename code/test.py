from out.lilypond import melody_to_lilypond, write_to_file
import generators.generator as gen
from core.models import Motif
from core.music import Key, Melody

OUTPUT_FILENAME = "melody.ly"
OUTPUT_PATH = "../output/.default/"

FULL_PATH = OUTPUT_PATH + OUTPUT_FILENAME 

KEY = Key("eb", "major")

TIME_SIG = "4/4"

motif = gen.generate_motif(KEY.mode)


print("Generated motif")
print(motif.notes)
print(motif.rhythm)

phrase1 = gen.motif_to_phrase(motif, KEY, TIME_SIG)

print("Generated phrase 1")
print(phrase1.notes)
print(phrase1.rhythm)

print("Generated melody 1")
Melody1 = gen.phrase_to_melody(phrase1, KEY)
print(Melody1.notes)

print("Convert to Melody object")
melody = Melody(KEY, notes=phrase1.notes, rhythm=phrase1.rhythm)
print(melody.notes)
print(melody.rhythm)
print(melody)

lilycode = melody_to_lilypond(melody, "voiceOne", "treble")
write_to_file(lilycode, FULL_PATH)
