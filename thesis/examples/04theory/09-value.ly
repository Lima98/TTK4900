\version "2.24.4"
\language "english"

\score {
  \relative {
  \override Staff.StaffSymbol.color = #(x11-color 'grey30)
  \override Staff.TimeSignature.color = #(x11-color 'grey60)
  \override Staff.Clef.color = #(x11-color 'grey60)
  \override Voice.NoteHead.color = #(rgb-color 0.8 0 0)
  \override Voice.Stem.color = #(rgb-color 0 0.8 0)
  \override Voice.Flag.color = #(rgb-color 0 0 0.8)
  \override Voice.Beam.color = #(rgb-color 0.6 0 0.6)
  \time 10/4

  g'1 g2 g4
  g8 g 
  g \nobeam
  g16 
  g16 \nobeam g
  }
  \layout {
    \context {
    \Staff
    \omit TimeSignature
    \omit BarLine
    \omit Staff
    }
    \context {
    }
  }
}

