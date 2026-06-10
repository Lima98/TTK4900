\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble_8"
      \key d \minor
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      c'8 d'2 f'4 d'8 |
      f'2 d'4 f'4 |
      g'4 a'4 g'2 |
      a'4 f'4 e'2 |
      d'4 c'8 d'4 c'8 d'8 c'8 |
      d'4 bf8 d'4 bf4 d'8 |
      a'4 f'2 e'8 f'8 |
      d'8 e'8 d'4 d'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      a8 a2 a4 a8 |
      bf2 bf4 bf4 |
      bf4 bf4 bf2 |
      a4 cs'4 cs'2 |
      c'4 a8 a4 a8 a8 a8 |
      g4 g8 g4 g4 g8 |
      cs'4 cs'2 cs'8 cs'8 |
      a8 a8 a4 a2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key d \minor
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      f8 f2 f4 f8 |
      d2 f4 d4 |
      d4 d4 d2 |
      e4 e4 a2 |
      a4 f8 c4 f8 c8 f8 |
      bf,4 d8 bf,4 d4 bf,8 |
      e4 e2 a8 e8 |
      f8 f8 f4 f2
      }
      \new Voice = "bass" { \voiceTwo
      d8 d2 d4 d8 |
      bf,2 bf,4 bf,4 |
      g,4 g,4 g,2 |
      cs4 a,4 a,2 |
      f,4 f,8 f,4 f,8 f,8 f,8 |
      g,4 g,8 g,4 g,4 g,8 |
      a,4 a,2 a,8 a,8 |
      d8 d8 d4 d2
      }
    >>
  >>
  \layout {}
  \midi {}
}
