import generators.generator as gen
from core.models import Motif
from core.music import Key

KEY = Key("eb", "major")
TIME_SIG = "4/4"

motif = gen.generate_motif(KEY.mode)

print(gen.motif_to_melody(motif, KEY, TIME_SIG))

print(motif.notes)
print(motif.rhythm)



