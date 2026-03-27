# This script compiles the .ly files in a give sub-directory using LilyPond and saves the output in the examples folder in the thesis.
# Run this script from the root of the .git repository to ensure correct paths.

import os
import subprocess
from pathlib import Path

# ====================================
# ======== Folder to process =========
# ====================================
PATH = "iter1"
# ====================================
# ======== only folder name ==========
# ====================================
# ====================================

PATH = "/" + PATH + "/"
cwd = str(Path(__file__).resolve().parent)
folder_path = cwd + PATH
OUTPUT_PATH = cwd + "/../latex/examples" + PATH

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

if os.path.isdir(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):


            INPUT =  cwd + PATH + os.path.splitext(filename)[0] + ".ly"

            if not os.path.exists(INPUT):
                print(f"Error: File '{INPUT}' does not exist.")
                exit(1)

            # Run lilypond to generate files
            subprocess.run(["lilypond", "-o", OUTPUT_PATH, "-dcrop", INPUT])
            midi_file = OUTPUT_PATH + os.path.splitext(filename)[0] + ".midi"
            audio_file =  "thesis/latex/examples" + PATH + os.path.splitext(filename)[0] + ".wav"

            subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
            #subprocess.run(["afplay", audio_file])

# Clean up unnecessary files and rename the cropped PDF
target_pattern = '.cropped.pdf'
for file in Path(OUTPUT_PATH).glob("*"):
    # Only delete files that are not the cropped PDF or wav file
    if not (file.name.endswith(target_pattern) or file.name.endswith('.wav')):
        try:
            file.unlink()
            print(f"Deleted: {file.name}")
        except Exception as e:
            print(f"Error deleting {file.name}: {e}")

