\version "2.24.4"
\language "english"

\score {
  \relative {
  \override Staff.StaffSymbol.color = #(x11-color 'grey30)
  \override Staff.TimeSignature.color = #(x11-color 'grey60)
  \override Staff.Clef.color = #(x11-color 'grey60)
  \override Voice.NoteHead.color = #(rgb-color 0 0 0)
  \override Voice.Stem.color = #(rgb-color 0.30 0.46 0.42)
  \override Voice.Flag.color = #(rgb-color 0.28 0.40 0.62)
  \override Voice.Beam.color = #(rgb-color 0.50 0.34 0.52)
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
