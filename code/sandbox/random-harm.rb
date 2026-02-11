# Generate a simple melody in LilyPond format
filename = "melody.ly"

note_pool = %w[c d e f g a b]
time_signature_pool = ['4/4']

num_bars = 8

# Note to semitone and index mappings for harmony
note_index = { 'c' => 0, 'd' => 1, 'e' => 2, 'f' => 3, 'g' => 4, 'a' => 5, 'b' => 6 }
note_semitones = { 'c' => 0, 'd' => 2, 'e' => 4, 'f' => 5, 'g' => 7, 'a' => 9, 'b' => 11 }

# Generate consonant harmony note (3rd, 5th, or 6th above)
def get_harmony_note(melody_note, note_pool, note_index, note_semitones)
  melody_idx = note_index[melody_note]
  melody_semitone = note_semitones[melody_note]
  
  # Consonant intervals: 3rd (2 steps), 5th (4 steps), 6th (5 steps)
  harmony_intervals = [2, 4, 5]
  interval = harmony_intervals.sample
  
  harmony_idx = (melody_idx + interval) % 7
  harmony_note = note_pool[harmony_idx]
  harmony_semitone = note_semitones[harmony_note]
  
  # Adjust octave if harmony is lower than melody
  if harmony_semitone <= melody_semitone
    harmony_note + "'"
  else
    harmony_note
  end
end

# Generate melody bar by bar, ensuring each bar sums to 4 beats
bars1 = []
bars2 = []

num_bars.times do
  bar_notes = []
  bar_durations = []
  beats_remaining = 4.0
  
  while beats_remaining > 0
    # Choose duration that fits in remaining beats
    available_durations = []
    available_durations << '2' if beats_remaining >= 2.0
    available_durations << '4' if beats_remaining >= 1.0
    available_durations << '8' if beats_remaining >= 0.5
    
    break if available_durations.empty?
    
    duration = available_durations.sample
    bar_notes << note_pool.sample
    bar_durations << duration
    
    # Subtract beats (2 = 2 beats, 4 = 1 beat, 8 = 0.5 beats)
    beats_remaining -= case duration
                       when '2' then 2.0
                       when '4' then 1.0
                       when '8' then 0.5
                       end
  end
  
  # Create bar string for melody 1
  bar1_str = bar_notes.zip(bar_durations).map { |note, duration| "#{note}#{duration}" }.join(' ')
  bars1 << bar1_str
  
  # Create harmonized melody 2 with consonant intervals
  bar_notes2 = bar_notes.map { |note| get_harmony_note(note, note_pool, note_index, note_semitones) }
  bar2_str = bar_notes2.zip(bar_durations).map { |note, duration| "#{note}#{duration}" }.join(' ')
  bars2 << bar2_str
end

time_signature = time_signature_pool.sample 
melody1 = bars1.map { |bar| "    #{bar} |" }.join("\n")
melody2 = bars2.map { |bar| "    #{bar} |" }.join("\n")

lilypond_output = %{
\\version "2.24.0"

\\score {
  \\new StaffGroup <<
    \\new Staff {
      \\clef treble
      \\time #{time_signature}
      #{melody1}
    }
    \\new Staff {
      \\clef bass
      \\time #{time_signature}
      #{melody2}
    }
  >>
  \\layout { }
  \\midi { }
}
}

output_path = File.join(__dir__, filename)
File.write(output_path, lilypond_output)
puts "Melody written to #{output_path}"

puts "Running lilypond..."
system("lilypond #{filename}")

# Convert MIDI to audio file
midi_file = filename.sub('.ly', '.midi')
audio_file = filename.sub('.ly', '.wav')

if File.exist?(midi_file)
  puts "Converting MIDI to audio..."
  # Try timidity first (common on macOS via Homebrew)
    system("timidity #{midi_file} -Ow -o #{audio_file}")
    puts "Audio file created: #{audio_file}"
    puts "Playing audio..."
    system("afplay #{audio_file}")
else
  puts "MIDI file not found: #{midi_file}"
end