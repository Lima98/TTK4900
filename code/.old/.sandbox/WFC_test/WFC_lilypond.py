import WFC_concept as gen


###########################################
# DEGREE → PITCH (C MAJOR)
###########################################

degree_to_pitch = {
    1: "c",
    2: "d",
    3: "e",
    4: "f",
    5: "g",
    6: "a",
    7: "b"
}


###########################################
# DURATION → LILYPOND
###########################################

def duration_to_lily(duration):

    mapping = {
        1.0: "4",
        0.5: "8",
        0.25: "16",
        2.0: "2",
    }

    return mapping.get(duration, "4")


###########################################
# NOTE → LILYPOND
###########################################

def note_to_lily(note):

    dur = duration_to_lily(note.duration)

    if note.rest:
        return f"r{dur}"

    pitch = degree_to_pitch[note.degree]

    return f"{pitch}'{dur}"


###########################################
# BAR → LILYPOND
###########################################

def bar_to_lily(bar):

    tokens = []

    for n in bar.notes:
        tokens.append(note_to_lily(n))

    return " ".join(tokens)


###########################################
# GENERATE MUSIC
###########################################

def generate_piece(bars=8):

    music = []

    for _ in range(bars):

        bar = gen.generate_bar()

        music.append(bar_to_lily(bar))

    return " |\n".join(music)


###########################################
# WRITE FILE
###########################################

def write_lilypond(filename="generated_music.ly", bars=8):

    music = generate_piece(bars)

    lily = f"""
\\version "2.24.0"

\\score {{
  \\new Staff {{
    \\time 4/4
    \\key c \\major

    {music}
  }}
  \\layout{{}}
  \\midi{{}}
}}
"""

    with open(filename, "w") as f:
        f.write(lily)

    print(f"Written {filename}")


###########################################
# RUN
###########################################

if __name__ == "__main__":

    write_lilypond("generated_music.ly", bars=12)
