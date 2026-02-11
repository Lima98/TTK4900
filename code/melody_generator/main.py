# main.py
# -dcrop makes the output PDF only contain the music, without extra margins
from scales import generate_major_scale
from rhythm import generate_rhythm
from phrase import generate_phrase
from variation import transpose

def phrase_to_lilypond(phrase):
    # Assumes phrase is a list of (pitch, duration) tuples
    # MIDI 60 = c', 62 = d', etc. (simple mapping for C major)
    midi_to_note = {
        60: "c'", 61: "cis'", 62: "d'", 63: "ees'", 64: "e'", 65: "f'",
        66: "fis'", 67: "g'", 68: "gis'", 69: "a'", 70: "bes'", 71: "b'",
        72: "c''"
    }
    # Simple duration mapping: 1 = quarter, 2 = half, 0.5 = eighth, etc.
    duration_map = {1: "4", 2: "2", 0.5: "8", 0.25: "16"}

    notes = []
    for pitch, dur in phrase:
        note = midi_to_note.get(pitch, "c'")
        duration = duration_map.get(dur, "4")
        notes.append(f"{note}{duration}")
    return " ".join(notes)

if __name__ == "__main__":
    tonic = 60  # C4 in MIDI
    scale = generate_major_scale(tonic)
    rhythm = generate_rhythm(4)
    call = generate_phrase(scale, rhythm, resolve=False)
    response = generate_phrase(scale, rhythm, resolve=True)
    varied_call = transpose(call, 2)  # Transpose up a major second

    lilypond_output = f"""
\\version "2.24.2"
\\score {{
  <<
    \\new Staff {{
      % Call
      {phrase_to_lilypond(call)}
      % Varied Call
      {phrase_to_lilypond(varied_call)}
      % Response
      {phrase_to_lilypond(response)}
    }}
  >>
}}
"""
import os
from datetime import datetime

output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(output_dir, f"{timestamp}.ly")

with open(output_path, "w") as f:
    f.write(lilypond_output)
# Compile the Lilypond file to MIDI and PDF, and play it with timidity
midi_path = output_path.replace(".ly", ".midi")
output_folder = os.path.dirname(output_path)
os.system(f"lilypond -o -dcrop {output_path[:-3]} {output_path}")  # MIDI and PDF
os.system(f"cd {output_folder} && lilypond {os.path.basename(output_path)}")  # PDF in output folder
os.system(f"timidity {midi_path}")
