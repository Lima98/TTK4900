# Handling conversion to LilyPond and generating associated files.
import subprocess
import os
from core.music import Key, Melody

# Duration mapping from beats to LilyPond notation
def beat_to_duration(beat):
    """
    Convert a duration in beats to the corresponding LilyPond duration notation.

    Args:
        beat (float): Duration in beats (e.g., 1 for quarter note, 0.5 for eighth note, etc.)

    Returns: Corresponding LilyPond duration notation as a string.
        
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
    Convert a Melody object to LilyPond format.

    Args:
        voice_name (str): Name of the voice to be used in LilyPond (e.g., "voiceOne").
        clef (str): Clef to be used in LilyPond (e.g., "treble", "bass", "\"treble_8\"").
        melody: Melody object to be converted to LilyPond format.

    Returns: A tuple containing the LilyPond code for the melody and the corresponding staff reference for the score.

    Raises:
        ValueError: If the melody has no key assigned, if any note has no pitch assigned, or if any note has no duration assigned.
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
    Write the generated LilyPond code to a .ly file.

    Args:
        lilypond_code (str): The LilyPond code to be written to the file.
        filename (str): The name of the .ly file to write to. Defaults to "output.ly".
    """
    with open(filename, "w") as file:
        file.write(lilypond_code)

# Combining multiple voices into a single LilyPond score
def voices_to_lilypond(voices, key, time_sig):
    """
    Write all voices into a single LilyPond score.

    Args:
        voices (list): List of tuples containing LilyPond code for each voice and their staff references.
        key (str): The key to notate the score in.
        time_sig (str): The time signature to notate the score in.

    Returns:
        
    """
    # Map music modes to valid LilyPond key modes
    _LILYPOND_MODES = {
        "major": "major",
        "minor": "minor",
        "dorian": "dorian",
        "phrygian": "phrygian",
        "lydian": "lydian",
        "mixolydian": "mixolydian",
        "locrian": "locrian",
        "major_pentatonic": "major",
        "minor_pentatonic": "minor",
        "harmonic_minor": "minor",
        "phrygian_dominant": "phrygian",
    }

    root, quality = key.split()
    root = root.replace("b", "f") if root.endswith("b") else root
    quality = _LILYPOND_MODES.get(quality, quality)

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
    Generate MIDI and PDF files from the .ly file using LilyPond.

    Args:
        filename (str): Name of the .ly file to be processed.
        path (str): Optional path where the generated files will be saved.
    """
    subprocess.run(["lilypond", "-o", path, "-dcrop", filename])

# Play generated files
def play(filename="output.ly"):
    """
    Play generated MIDI file using Timidity. Assumes that the MIDI file has been generated from the .ly file and is in the same directory.

    Args:
        filename (str): The name of the .ly file from which the MIDI file was generated. The function will look for a corresponding .midi file with the same base name.
    """
    midi_file = filename.replace('.ly', '.midi')
    audio_file = filename.replace('.ly', '.wav')

    if os.path.exists(midi_file):
        subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
        subprocess.run(["afplay", audio_file])
    else:
        print(f"MIDI file not found: {midi_file}")


# Converting a full Piece to a LilyPond score
def piece_to_lilypond(piece, voice_configs):
    """
    Convert a full Piece (with sections, phrases, and voices) to a LilyPond score.

    Iterates over the form, collecting all notes for each voice in playback order,
    then builds a single combined melody per voice and renders the score.

    Args:
        piece: A Piece object containing sections, form, key, and time signature.
        voice_configs: List of voice configuration dicts, each with keys:
            "name" (str), "clef" (str).

    Returns: A string containing the full LilyPond score.
    """
    num_voices = len(voice_configs)
    all_notes = [[] for _ in range(num_voices)]

    # Collect notes from all sections in form order
    for section in piece.get_ordered_sections():
        for phrase in section.phrases:
            for i, melody in enumerate(phrase.melodies):
                # Ensure concrete pitches are populated before collecting notes
                melody.to_pitches()
                all_notes[i].extend(melody.notes)

    # Build one combined Melody per voice and convert to LilyPond
    lily_voices = []
    for i, voice_config in enumerate(voice_configs):
        combined = Melody(key=piece.key, notes=all_notes[i])
        lily_voice = melody_to_lilypond(combined, voice_config["name"], voice_config["clef"])
        lily_voices.append(lily_voice)

    key_string = f"{piece.key.tonic} {piece.key.mode}"
    lily_code = voices_to_lilypond(lily_voices, key_string, piece.time_sig)

    # Inject tempo marking after the \time directive
    tempo_line = f"\t\\tempo 4 = {piece.tempo}\n"
    lily_code = lily_code.replace(
        f"\t\\time {piece.time_sig}\n",
        f"\t\\time {piece.time_sig}\n{tempo_line}"
    )

    return lily_code
