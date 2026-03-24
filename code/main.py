import constraints as con
import generators as gen
import music as music

motif = gen.generate_motif()
for note in motif.notes:
    print(note.midiNum, note.key, note.duration )
