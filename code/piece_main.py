from core.music import Key
from generators.generator import generate_piece
from out.lilypond import (
    piece_to_lilypond,
    write_to_file,
    generate_files,
    play
)

# ---------------- Configuration ----------------

OUTPUT_FILENAME = "piece.ly"
OUTPUT_PATH = "../output/musical-piece/"
FULL_PATH = OUTPUT_PATH + OUTPUT_FILENAME

TITLE = "AABA Sketch"
KEY_NAME = "g"
MODE = "major"
TIME_SIGNATURE = "4/4"
TEMPO = 100

# Voice configuration: soprano melody and bass line
VOICE_CONFIGS = [
    {"name": "voiceOne", "clef": "treble",      "rhythm_values": ["q", "h"]},
    {"name": "voiceFour", "clef": "bass",        "rhythm_values": ["h", "w"]},
]

# ---------------- Form Definition ----------------
#
# AABA (32-bar) form:
#   A sections  – 8 bars each (2 phrases × 4 bars), stepwise quarter/half motion
#   B section   – 8 bars (2 phrases × 4 bars), livelier eighth/quarter motion
#
FORM_DEF = {
    "A": {
        "num_phrases": 2,
        "bars_per_phrase": 4,
        "rhythm_values": ["q", "h"],
        "voice_overrides": [
            {"rhythm_values": ["q", "h"]},   # soprano: quarters and halves
            {"rhythm_values": ["h", "w"]},   # bass: halves and whole notes
        ],
    },
    "B": {
        "num_phrases": 2,
        "bars_per_phrase": 4,
        "rhythm_values": ["e", "q"],
        "voice_overrides": [
            {"rhythm_values": ["e", "q"]},   # soprano: more active motion
            {"rhythm_values": ["q", "h"]},   # bass: quarter/half movement
        ],
    },
}

FORM_ORDER = ["A", "A", "B", "A"]

# ---------------- Generate Piece ----------------

key = Key(KEY_NAME, MODE)

piece = generate_piece(
    title=TITLE,
    key=key,
    form_def=FORM_DEF,
    form_order=FORM_ORDER,
    voice_configs=VOICE_CONFIGS,
    time_sig=TIME_SIGNATURE,
    tempo=TEMPO
)

print(f"Generated: {piece}")
for label in piece.form:
    section = piece.sections[label]
    print(f"  Section {section.label}: {len(section.phrases)} phrases")
    for phrase in section.phrases:
        print(f"    Phrase {phrase.label}: {phrase.bars} bars, "
              f"{sum(len(m.notes) for m in phrase.melodies)} total notes across "
              f"{len(phrase.melodies)} voice(s)")

# ---------------- Convert to LilyPond ----------------

lily_code = piece_to_lilypond(piece, VOICE_CONFIGS)

# ---------------- Output ----------------

write_to_file(lily_code, FULL_PATH)
print(f"\nLilyPond file written to: {FULL_PATH}")

generate_files(FULL_PATH, OUTPUT_PATH)
play(FULL_PATH)
