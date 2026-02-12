
\version "2.24.0"

\score {
  \new StaffGroup <<
    \new Staff {
      \clef treble
      \time 4/4
          c2 a8 a8 b8 f8 |
    b4 e8 f8 b2 |
    e2 e2 |
    f8 c2 e4 f8 |
    g2 e8 g4 b8 |
    g8 c2 f4 c8 |
    b4 e2 g4 |
    b4 d2 e4 |
    }
    \new Staff {
      \clef bass
      \time 4/4
          e2 c'8 f'8 g'8 c'8 |
    g'4 b8 d'8 g'2 |
    b2 g2 |
    a8 e2 g4 c'8 |
    b2 c'8 d'4 g'8 |
    e'8 a2 c'4 g8 |
    d'4 b2 d'4 |
    g'4 a2 g4 |
    }
  >>
  \layout { }
  \midi { }
}
