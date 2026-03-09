from music import Note, Bar
import generator as gen


number_of_bars = 2


for bar in range(number_of_bars):
    bars = gen.generate_bar(beats=4)

for note in bars.notes:
    print(note.duration, note.degree, note.rest)
