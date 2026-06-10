\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key d \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      fs'8 a'4 fs'2 g'8 |
      fs'8 fs'4 g'8 a'2 |
      g'2 fs'4 a'8 g'8 |
      b'4 g'4 a'2 |
      d''4 cs''4 d''4 c''4 |
      d''4 b'4 bf'8 bf'8 g'8 bf'8 |
      fs'4 a'8 fs'2 a'8 |
      fs'2 a'2 |
      fs'2 a'2 |
      b'2 a'2 |
      d''4 b'8 g'8 fs'4 a'8 g'8 |
      fs'2 g'2 |
      b'8 g'8 b'8 g'8 bf'2 |
      a'4 fs'4 a'8 fs'8 fs'8 a'8 |
      b'4 g'2 a'8 b'8 |
      f'8 g'4 f'8 a'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      d'8 d'4 d'2 e'8 |
      d'8 d'4 d'8 cs'2 |
      d'2 d'4 d'8 fs'8 |
      e'4 e'4 e'2 |
      fs'4 fs'4 f'4 f'4 |
      d'4 d'4 g'8 g'8 d'8 d'8 |
      d'4 d'8 d'2 e'8 |
      d'2 d'2 |
      d'2 cs'2 |
      d'2 d'2 |
      e'4 e'8 e'8 e'4 e'8 e'8 |
      d'2 e'2 |
      d'8 d'8 d'8 d'8 d'2 |
      d'4 d'4 cs'8 cs'8 cs'8 cs'8 |
      e'4 e'2 e'8 e'8 |
      d'8 d'4 d'8 d'2
      }
    >>
    \new Staff <<
      \clef "treble_8"
      \key d \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      a8 fs4 a2 a8 |
      b8 b4 fs8 fs2 |
      b2 a4 fs8 a8 |
      g4 b4 cs'2 |
      d'4 d'4 c'4 c'4 |
      b4 b4 d'8 d'8 bf8 bf8 |
      a4 fs8 a2 a8 |
      a2 fs2 |
      b2 a2 |
      g2 fs2 |
      g4 g8 b8 cs'4 cs'8 cs'8 |
      a2 c'2 |
      b8 b8 b8 b8 bf2 |
      fs4 a4 a8 a8 a8 a8 |
      g4 b2 a8 a8 |
      bf8 f4 bf8 fs2
      }
      \new Voice = "bass" { \voiceTwo
      d8 d4 d2 cs8 |
      b,8 b,4 b,8 cs2 |
      g2 d4 d8 d8 |
      e4 e4 a2 |
      a4 a4 a4 a4 |
      g4 g4 g8 g8 g8 g8 |
      d4 d8 d2 cs8 |
      d2 d2 |
      d2 fs2 |
      d2 d2 |
      b,4 e8 e8 a4 a8 a8 |
      d2 c2 |
      g8 g8 g8 g8 g2 |
      d4 d4 fs8 fs8 fs8 fs8 |
      e4 e2 cs8 cs8 |
      d8 bf,4 bf,8 d2
      }
    >>
  >>
  \layout {}
  \midi {}
}
