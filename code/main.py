from music import Note, Bar
import generator as gen


number_of_bars = 2


for bar in range(number_of_bars):
    bars = gen.generate_bar(beats=4)

print("Dur:\tDeg:\tRest:")
for note in bars.notes:
    print(f"{note.duration}\t{note.degree}\t{note.rest}")

degree_to_pitch = {
    "1": "c",
    "b2": "db",
    "2": "d",
    "b3": "eb",
    "3": "e",
    "4": "f",
    "s4": "f#",
    "5": "g",
    "b6": "ab",
    "6": "a",
    "b7": "bb",
    "7": "b",
    }

print("---------------------")
for note in bars.notes:
    if note.degree is not None:
        note.pitch = degree_to_pitch[note.degree]
    else:
        note.pitch = None

    if note.pitch is not None:
        print(note.pitch)
    else:
        print("Rest")
