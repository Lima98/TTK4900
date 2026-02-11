# Generate a simple melody in LilyPond format
filename = "melody.ly"

note_pool = %w[c d e f g a b]
time_signature_pool = ['4/4']

num_bars = 80

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
  
  # Create bar string for melody 2 with same rhythm but different notes
  bar_notes2 = bar_durations.map { note_pool.sample }
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
