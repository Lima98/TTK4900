def midi_to_lily(pitch):
    names = ['c', 'cis', 'd', 'ees', 'e', 'f',
             'fis', 'g', 'gis', 'a', 'bes', 'b']

    name = names[pitch % 12]
    octave = (pitch // 12) - 4

    if octave >= 0:
        name += "'" * octave
    else:
        name += "," * (-octave)

    return name


def event_to_lily(event):
    if event.kind == "rest":
        return "r4"
    else:
        return f"{midi_to_lily(event.pitch)}4"


def voice_to_lily(voice):
    return " ".join(event_to_lily(e) for e in voice.events)


def score_to_lily(score):
    lead = []
    bass = []

    for bar in score.bars:
        lead.append(voice_to_lily(bar.voices["L"]))
        bass.append(voice_to_lily(bar.voices["B"]))

    lead_str = " |\n  ".join(lead)
    bass_str = " |\n  ".join(bass)

    return f"""
\\version "2.24.0"

\\score {{
  <<
    \\new Staff = "lead" {{
      \\clef treble
      \\time 4/4
      {lead_str}
    }}
    \\new Staff = "bass" {{
      \\clef bass
      \\time 4/4
      {bass_str}
    }}
  >>
  \\layout {{}}
  \\midi {{}}
}}
"""
