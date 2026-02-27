from core.music import Key
from generators.generator import generate_notes, generate_rhythm
from out.lilypond import (
    melody_to_lilypond,
    voices_to_lilypond,
    write_to_file,
    generate_files,
    play
)

# ---------------- Configuration ----------------


OUTPUT_FILENAME = "melody.ly"
OUTPUT_PATH = "../output/.default/"

FULL_PATH = OUTPUT_PATH + OUTPUT_FILENAME 


KEY_NAME = "c"
MODE = "major"
TIME_SIGNATURE = "4/4"
BARS = 8

# Voice configuration (extensible)
VOICES = [
    {"name": "voiceOne",   "clef": "treble",      "rhythm_values": ["q", "e", "h"]},
    {"name": "voiceTwo",   "clef": "\"treble_8\"", "rhythm_values": ["q"]},
    {"name": "voiceThree", "clef": "bass",        "rhythm_values": ["h"]},
    {"name": "voiceFour",  "clef": "bass",        "rhythm_values": ["w"]},
]

# ---------------- Setup ----------------

key = Key(KEY_NAME, MODE)

melodies = []

# ---------------- Generate Music ----------------

for voice_config in VOICES:
    # Generate rhythm
    rhythm = generate_rhythm(
        bars=BARS,
        time_sig=TIME_SIGNATURE,
        values=voice_config["rhythm_values"]
    )

    # Generate melody
    melody = generate_notes(
        num_notes=len(rhythm),
        key=key
    )

    # Attach rhythm
    melody.add_rhythm(rhythm)

    melodies.append((melody, voice_config))


# ---------------- Convert to LilyPond ----------------

lily_voices = []

for melody, voice_config in melodies:
    lily_voice = melody_to_lilypond(
        melody,
        voice_config["name"],
        voice_config["clef"]
    )
    lily_voices.append(lily_voice)


# ---------------- Assemble Score ----------------

full_key_string = f"{KEY_NAME} {MODE}"

lily_code = voices_to_lilypond(
    lily_voices,
    full_key_string,
    TIME_SIGNATURE
)


# ---------------- Output ----------------

write_to_file(lily_code, FULL_PATH)
generate_files(FULL_PATH, OUTPUT_PATH)
play(FULL_PATH)
