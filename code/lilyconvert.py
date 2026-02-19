# Handling conversion to LilyPond and generating associated files.
import subprocess
import os

# Convert melody to LilyPond format
def melody_to_lilypond(melody, key, time_sig):
    """

    Args:
        melody (): A list of notes in the melody, where each note is represented as a string (e.g., "c4", "d8", "e16").

    Returns:        A string containing the LilyPond code representing the melody, including necessary headers and structure for a complete score.
        
    """
    root, quality = key.split()
    root = root.replace("b","f") if root.endswith("b") else root
    lilypond_output = "\\version \"2.24.4\"\n"
    lilypond_output += "\\language \"english\"\n\n"
    lilypond_output += "\\score {\n"
    lilypond_output += "\t \\new Staff {\n"
    lilypond_output += f"\t\t\\key {root} \\{quality}\n"
    lilypond_output += f"\t\t\\time {time_sig}\n"
    lilypond_output += "\t\t\\relative c'{\n"
    lilypond_output += "\t\t"

    for note in melody:
        lilypond_output += f"  {note} "

    lilypond_output += "\n\t\t\t}"
    lilypond_output += "\n\t\t}"
    lilypond_output += "\n\t\t\\midi {}"
    lilypond_output += "\n\t\t\\layout {}"
    lilypond_output += "\n}"
    
    return lilypond_output

# Write LilyPond code to a file
def write_to_file(lilypond_code, filename="code/output/default/output.ly"):
    """

    Args:
        lilypond_code (): A string containing the LilyPond code to be written to a file.
        filename (): The name of the file where the LilyPond code will be saved. 
    """
    with open(filename, "w") as file: 
        file.write(lilypond_code)

# Beat to lilypond durations
def beat_to_duration(beat):
    beat = [str(x) for x in beat]
    beat_to_dur = {
            "16": "\\longa",
            "8": "\\breve",
            "4": "1",
            "2": "2",
            "1": "4",
            "0.5": "8",
            "0.25": "16",
            "0.125": "32",
            "0.0625": "64",
            }

    durations = [beat_to_dur[dur] for dur in beat]

    return durations

# Concatenate notes and rhythms
def note_and_rhythm(notes, rhythm):
    """

    Args:
        notes (): A list of notes in the melody, where each note is represented as a string (e.g., "c", "d", "e").
        rhythm (): A list of rhythm durations corresponding to each note, where each duration is represented as a string (e.g., "4" for whole note, "2" for half note, "1" for quarter note, etc.). 

    Returns:    A list of strings where each string represents a note combined with its corresponding rhythm duration in LilyPond format (e.g., "c4", "d8", "e16"). The function checks if the lengths of the notes and rhythm lists are the same and prints an error message if they are not.
        
    """
    if len(notes) != len(rhythm):
        print("Notes and rhythm are different lengths")
        return

    melody = list(map(str.__add__, notes, rhythm))
    return melody

# Run lilypond to generate PDF, midi and png files
def generate_files(filename="code/output/default/output.ly", path = "code/output/"):
    """

    Args:
        filename (): The name of the LilyPond file to be processed, including its path. 
        path (): The directory where the generated files (PDF, MIDI, PNG) will be saved. The function uses the subprocess module to run the LilyPond command-line tool, which processes the specified LilyPond file and generates the corresponding output files in the specified directory. The "-o" option specifies the output directory, and the "-dcrop" option tells LilyPond to crop the PDF output to fit the content.
    """
    subprocess.run(["lilypond", "-o", path, "-dcrop",  filename])


def play(filename="code/output/default/output.ly"):
    """

    Args:
        filename (): The name of the LilyPond file to be processed for audio playback, including its path. The function first checks if a corresponding MIDI file exists (with the same name but a .midi extension). If the MIDI file is found, it uses the Timidity++ software synthesizer to convert the MIDI file into a WAV audio file. After the audio file is created, it uses the "afplay" command (specific to macOS) to play the generated audio file. If the MIDI file is not found, it prints an error message indicating that the MIDI file could not be located.
    """
    # Convert MIDI to audio file
    midi_file = filename.replace('.ly', '.midi')
    audio_file = filename.replace('.ly', '.wav')
    if os.path.exists(midi_file):
        print("Converting MIDI to audio...")
        subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
        print(f"Audio file created: {audio_file}")
        print("Playing audio...")
        subprocess.run(["afplay", audio_file])
        # subprocess.run(["timidity", midi_file]) Does not work
    else:
        print(f"MIDI file not found: {midi_file}")
