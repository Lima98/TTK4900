\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key d \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      fs'2 a'8 fs'4 a'8 |
      fs'4 a'2 bf'4 |
      a'8 fs'2 g'4 bf'8 |
      a'8 fs'8 a'8 fs'8 a'2 |
      g'2 a'2 |
      d''2 b'4 g'4 |
      b'4 g'4 bf'2 |
      fs'2 a'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      d'2 e'8 e'4 e'8 |
      d'4 d'2 d'4 |
      d'8 d'2 d'4 d'8 |
      d'8 d'8 d'8 d'8 cs'2 |
      d'2 cs'2 |
      d'2 d'4 d'4 |
      d'4 d'4 d'2 |
      d'2 d'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key d \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      a2 a8 a4 a8 |
      b4 fs2 g4 |
      fs8 a2 g4 g8 |
      fs8 a8 fs8 a8 a2 |
      b2 a2 |
      fs2 g4 g4 |
      g4 g4 g2 |
      a2 fs2
      }
      \new Voice = "bass" { \voiceTwo
      d2 cs8 cs4 cs8 |
      b,4 b,2 bf,4 |
      d8 d2 bf,4 bf,8 |
      d8 d8 d8 d8 fs2 |
      g2 e2 |
      b,2 b,4 b,4 |
      b,4 b,4 bf,2 |
      d2 d2
      }
    >>
  >>
  \layout {}
  \midi {}
}
