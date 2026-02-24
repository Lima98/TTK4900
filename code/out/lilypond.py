# Handling conversion to LilyPond and generating associated files.
import subprocess
import os
from core.music import Melody

# Duration mapping from beats to LilyPond notation
def beat_to_duration(beat):
    """

    Args:
        beat (): A numerical value representing the duration of a note in beats (e.g., 1 for quarter note, 0.5 for eighth note) to convert to its corresponding LilyPond duration notation.

    Returns:       A string representing the LilyPond duration notation corresponding to the input beat value, such as "1" for a quarter note, "2" for a half note, "4" for a whole note, etc., based on standard musical durations.
        
    """
    beat_to_dur = {
        16: "\\longa",
        8: "\\breve",
        4: "1",
        2: "2",
        1: "4",
        0.5: "8",
        0.25: "16",
        0.125: "32",
        0.0625: "64",
    }

    return beat_to_dur.get(beat)


# Converting Melody objects to LilyPond format
def melody_to_lilypond(melody: Melody, voice_name, clef):
    """

    Args:
        voice_name (): A string representing the name of the voice (e.g., "soprano", "alto", "tenor", "bass") to be used in the LilyPond output for labeling the musical part corresponding to the given melody.
        clef (): A string representing the clef (e.g., "treble", "bass") to be used in the LilyPond output for the staff that will contain the given melody.
        melody: A Melody object containing a list of Note objects representing the melody to be converted into LilyPond format. Each Note object should have its pitch and duration properties populated for accurate conversion.

    Returns:     A list containing two strings: the first string is the LilyPond code defining the voice with the melody, and the second string is the LilyPond code for the staff that references this voice. These strings can be combined with other voices and staff definitions to create a complete LilyPond score.
        

    Raises:
        ValueError: If the melody does not have a key assigned, or if any note in the melody lacks a pitch or duration, a ValueError is raised with an appropriate message indicating the issue.
    """
    if melody.key is None:
        raise ValueError("Melody must have a key before exporting to LilyPond")

    # Ensure pitches are populated
    melody.to_pitches()

    lilypond_melody = f"{voice_name} = \\relative c' " + "{\n"
    lilypond_melody += "\t\\global\n\t"

    for note in melody.notes:
        if note.pitch is None:
            raise ValueError("Note has no pitch assigned")

        if note.duration is None:
            raise ValueError("Note has no duration assigned")

        duration = beat_to_duration(note.duration)
        lilypond_melody += f"{note.pitch}{duration} "

    lilypond_melody += "\n}"

    score_part = "\\new Staff {\n"
    score_part += f"\t\\clef {clef}\n"
    score_part += f"\t\\{voice_name}\n"
    score_part += "}"

    return [lilypond_melody, score_part]


# Writing the generated LilyPond code to a .ly file
def write_to_file(lilypond_code, filename="output.ly"):
    """

    Args:
        lilypond_code (str): A string containing the complete LilyPond code that represents the musical score to be written to a .ly file. This code should include all necessary definitions for voices, staves, and global settings to create a valid LilyPond file that can be processed to generate MIDI and PDF outputs.
        filename (str): The name of the .ly file to which the LilyPond code will be written. This file will be created or overwritten in the current working directory, and it should have a .ly extension to be recognized as a valid LilyPond file.
    """
    with open(filename, "w") as file:
        file.write(lilypond_code)


# Combining multiple voices into a single LilyPond score
def voices_to_lilypond(voices, key, time_sig):
    """

    Args:
        voices (list): A list of tuples, where each tuple contains two strings: the first string is the LilyPond code defining a voice with its melody, and the second string is the LilyPond code for the staff that references this voice. This list represents all the voices that will be included in the final LilyPond score.
        key (str): A string representing the key signature (e.g., "c major", "eb minor") to be included in the global settings of the LilyPond score. This key signature will apply to all voices in the score and should be formatted correctly for LilyPond syntax.
        time_sig (str): A string representing the time signature (e.g., "4/4", "3/4", "6/8") to be included in the global settings of the LilyPond score. This time signature will apply to all voices in the score and should be formatted correctly for LilyPond syntax.

    Returns:    A string containing the complete LilyPond code for the score, which includes global settings for the key signature and time signature, as well as the definitions for all voices and their corresponding staves. This code can be written to a .ly file and processed by LilyPond to generate MIDI and PDF outputs.
        
    """
    root, quality = key.split()
    root = root.replace("b", "f") if root.endswith("b") else root

    lilypond_output = "\\version \"2.24.4\"\n"
    lilypond_output += "\\language \"english\"\n\n"

    lilypond_output += "global = {\n"
    lilypond_output += f"\t\\key {root} \\{quality}\n"
    lilypond_output += f"\t\\time {time_sig}\n"
    lilypond_output += "}\n\n"

    # Voice definitions
    for voice in voices:
        lilypond_output += voice[0] + "\n\n"

    lilypond_output += "\\score {\n"
    lilypond_output += "\\new ChoirStaff <<\n"

    # Staff references
    for voice in voices:
        lilypond_output += "\t" + voice[1] + "\n"

    lilypond_output += "\t>>\n"
    lilypond_output += "\t\\midi {}\n"
    lilypond_output += "\t\\layout {}\n"
    lilypond_output += "}"

    return lilypond_output

# Generating MIDI and PDF files from the .ly file using LilyPond, and playing the MIDI file using Timidity.
def generate_files(filename="output.ly", path=""):
    """

    Args:
        filename (str): The name of the .ly file that contains the LilyPond code to be processed. This file should exist in the current working directory and should have a valid .ly extension for LilyPond to recognize it as an input file.
        path (str): The directory path where the generated MIDI and PDF files will be saved. If this path is empty, the generated files will be saved in the current working directory. The path should end with a separator (e.g., "/" or "\\") if it is not empty to ensure that the generated files are saved in the correct location.
    """
    subprocess.run(["lilypond", "-o", path, "-dcrop", filename])


def play(filename="output.ly"):
    """

    Args:
        filename (str): The name of the .ly file that contains the LilyPond code for the musical score. This file should exist in the current working directory and should have a valid .ly extension. The function will look for a corresponding MIDI file with the same base name (but with a .midi extension) generated from this .ly file, and if found, it will use Timidity to play the MIDI file. If the MIDI file is not found, an error message will be printed indicating that the MIDI file could not be located.
    """
    midi_file = filename.replace('.ly', '.midi')
    audio_file = filename.replace('.ly', '.wav')

    if os.path.exists(midi_file):
        subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
        subprocess.run(["afplay", audio_file])
    else:
        print(f"MIDI file not found: {midi_file}")
