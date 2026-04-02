import constraints as con
import generators as gen
import music as music
import lilypond as lily

phrase = gen.generate_phrase('C')

# Print all the generated music in a readable format
print(f"Phrase in key of {phrase.key}:")
for i, bar in enumerate(phrase.bars):
    print(f"Bar {i + 1}:")
    for note in bar.notes:
        print(f"Note: {note.key}{note.midiNum // 12 - 1}, Duration: {note.duration} beats")

lily.generateLilyPond(phrase)
