import os
import random
import subprocess

filename = "melody.ly"

note_pool = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
time_signature_pool = ['4/4']

num_bars = 1000

# Generate melody bar by bar, ensuring each bar sums to 4 beats
bars1 = []
bars2 = []

for _ in range(num_bars):
    bar_notes = []
    bar_durations = []
    beats_remaining = 4.0

    while beats_remaining > 0:
        available_durations = []
        if beats_remaining >= 2.0:
            available_durations.append('2')
        if beats_remaining >= 1.0:
            available_durations.append('4')
        if beats_remaining >= 0.5:
            available_durations.append('8')

        if not available_durations:
            break

        duration = random.choice(available_durations)
        bar_notes.append(random.choice(note_pool))
        bar_durations.append(duration)

        if duration == '2':
            beats_remaining -= 2.0
        elif duration == '4':
            beats_remaining -= 1.0
        elif duration == '8':
            beats_remaining -= 0.5

    bar1_str = ' '.join(f"{note}{duration}" for note, duration in zip(bar_notes, bar_durations))
    bars1.append(bar1_str)

    bar_notes2 = [random.choice(note_pool) for _ in bar_durations]
    bar2_str = ' '.join(f"{note}{duration}" for note, duration in zip(bar_notes2, bar_durations))
    bars2.append(bar2_str)

time_signature = random.choice(time_signature_pool)
melody1 = '\n'.join(f"    {bar} |" for bar in bars1)
melody2 = '\n'.join(f"    {bar} |" for bar in bars2)

lilypond_output = f"""
\\version "2.24.0"

\\score {{
  \\new StaffGroup <<
    \\new Staff {{
      \\clef treble
      \\time {time_signature}
{melody1}
    }}
    \\new Staff {{
      \\clef bass
      \\time {time_signature}
{melody2}
    }}
  >>
  \\layout {{ }}
  \\midi {{ }}
}}
"""

output_path = os.path.join(os.path.dirname(__file__), filename)
with open(output_path, 'w') as f:
    f.write(lilypond_output)
print(f"Melody written to {output_path}")

print("Running lilypond...")
subprocess.run(["lilypond", filename])

# Convert MIDI to audio file
midi_file = filename.replace('.ly', '.midi')
audio_file = filename.replace('.ly', '.wav')

if os.path.exists(midi_file):
    print("Converting MIDI to audio...")
    subprocess.run(["timidity", midi_file, "-Ow", "-o", audio_file])
    print(f"Audio file created: {audio_file}")
    print("Playing audio...")
    subprocess.run(["afplay", audio_file])
else:
    print(f"MIDI file not found: {midi_file}")
