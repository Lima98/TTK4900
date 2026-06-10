\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble_8"
      \key g \minor
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      g'4 a'4 bf'2 |
      g'4 bf'8 g'2 bf'8 |
      g'2 bf'8 a'8 g'8 f'8 |
      g'2 a'2 |
      g'4 f'2 g'4 |
      f'4 g'8 ef'2 g'8 |
      d''8 bf'2 a'4 fs'8 |
      g'8 bf'8 g'8 bf'8 g'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      d'4 d'4 d'2 |
      ef'4 ef'8 ef'2 ef'8 |
      ef'2 ef'8 ef'8 ef'8 ef'8 |
      a2 a2 |
      bf4 bf2 bf4 |
      ef'4 ef'8 c'2 c'8 |
      fs'8 fs'2 fs'4 d'8 |
      d'8 d'8 d'8 d'8 d'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key g \minor
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      bf4 bf4 bf2 |
      bf4 g8 bf2 g8 |
      c'2 g8 g8 c'8 g8 |
      fs2 fs2 |
      f4 f2 f4 |
      g4 g8 g2 ef8 |
      a8 a2 d'4 a8 |
      bf8 bf8 bf8 bf8 bf2
      }
      \new Voice = "bass" { \voiceTwo
      g4 g4 g2 |
      ef4 ef8 ef2 ef8 |
      ef2 c8 c8 c8 c8 |
      d2 d2 |
      d4 d2 d4 |
      c4 c8 c2 c8 |
      d8 d2 d4 d8 |
      g8 g8 g8 g8 g2
      }
    >>
  >>
  \layout {}
  \midi {}
}
