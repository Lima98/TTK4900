# Handling conversion to LilyPond and generating associated files.
import subprocess
import os

# Convert melody to LilyPond format
def melody_to_lilypond(melody):
    lilypond_output = "\\version \"2.24.4\"\n"
    lilypond_output += "\\language \"english\"\n\n"
    lilypond_output += "\\score {\n"
    lilypond_output += "\t \\new Staff {\n"
    lilypond_output += "\t\t\\key c \\major\n"
    lilypond_output += "\t\t\\time 4/4\n"
    lilypond_output += "\t\t\\relative \n"
    lilypond_output += "\t"


    for note in melody:
        lilypond_output += f"  {note} "


    lilypond_output += "\n}"
    lilypond_output += "\n\t\t\\layout {}"
    lilypond_output += "\n\t\t\\midi {}"
    lilypond_output += "\n}"
    
    return lilypond_output

# Write LilyPond code to a file
def write_to_file(lilypond_code, filename="code/output/default/output.ly"):
    with open(filename, "w") as file: 
        file.write(lilypond_code)

# Beat to lilypond durations
def beat_to_duration(beat):
    beat = [str(x) for x in beat]
    beat_to_dur = {
            "4": "1",
            "2": "2",
            "1": "4",
            "0.5": "8"
            }

    durations = [beat_to_dur[dur] for dur in beat]

    return durations

# Concatenate notes and rhythms
def note_and_rhythm(notes, rhythm):
    if len(notes) != len(rhythm):
        print("Notes and rhythm are different lengths")
        return

    melody = list(map(str.__add__, notes, rhythm))
    return melody

# Run lilypond to generate PDF, midi and png files
def generate_files(filename="code/output/default/output.ly", path = "code/output/"):
    subprocess.run(["lilypond", "-o", path, "-dcrop", filename])

    # Convert MIDI to audio file
    midi_file = filename.replace('.ly', '.midi')
    audio_file = filename.replace('.ly', '.wav')

    if os.path.exists(midi_file):
        print("Converting MIDI to audio...")
        subprocess.run(["timidity", path + midi_file, "-Ow", "-o", audio_file])
        print(f"Audio file created: {audio_file}")
        print("Playing audio...")
        subprocess.run(["afplay", audio_file])
    else:
        print(f"MIDI file not found: {midi_file}")
