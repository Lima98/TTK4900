# Handling conversion to LilyPond and generating associated files.
import subprocess

# Convert melody to LilyPond format
def melody_to_lilypond(melody):
    lilypond_output = "\\version \"2.24.4\"\n\n"
    lilypond_output += "\\relative c' {\n"
    for note in melody:
        lilypond_output += f"  {note} "
    lilypond_output += "\n}"
    return lilypond_output

# Write LilyPond code to a file
def write_to_file(lilypond_code, filename="output.ly"):
    with open("code/output/" + filename, "w") as file: 
        file.write(lilypond_code)


# Run lilypond to generate PDF, midi and png files
def generate_files(filename="output.ly"):
    subprocess.run(["lilypond", "-o", "code/output/", "-dcrop", "code/output/" + filename])


