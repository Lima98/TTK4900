\version "2.24.4"
\language "english"
\override Score.SpacingSpanner.uniform-stretching = ##t

\score {
  \new PianoStaff <<
    % Treble staff
    \new Staff {
      \override Staff.BarLine.allow-span-bar = ##f
      \clef treble
      \relative c {
        s1*10 
        f1 g a b
        c d e f g a b
        c d e f g a b c
     }
    }

    % Bass staff
    \new Staff {
      \clef bass
      \relative c, {
        c1 d e f g a b
        c d e f g a b
        c d e s2 s1*12
      }
    }
  >>
  \layout {
    \context {
    \Staff
    \omit TimeSignature
    \omit BarLine
    }
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1)
    }
  }
}
