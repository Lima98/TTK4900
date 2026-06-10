\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key e \minor
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      g'4 b'8 g'8 b'2 |
      g'4 a'2 g'4 |
      a'8 b'4 a'8 c''8 a'8 c''4 |
      b'4 ds''8 b'8 b'2 |
      d''8 e''4 d''4 e''8 d''4 |
      e''2 c''4 a'8 c''8 |
      b'2 g'4 b'4 |
      g'8 b'8 g'8 b'8 b'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      e'4 e'8 e'8 e'2 |
      e'4 e'2 e'4 |
      e'8 e'4 e'8 e'8 e'8 e'4 |
      fs'4 fs'8 fs'8 fs'2 |
      g'8 g'4 g'4 g'8 g'4 |
      e'2 e'4 e'8 e'8 |
      fs'2 fs'4 fs'4 |
      e'8 e'8 e'8 e'8 e'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key e \minor
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      b4 g8 b8 g2 |
      c'4 g2 c'4 |
      a8 a4 a8 a8 a8 a4 |
      ds'4 ds'8 ds'8 ds'2 |
      b8 b4 b4 b8 b4 |
      a2 a4 a8 a8 |
      ds'2 ds'4 ds'4 |
      b8 g8 b8 g8 g2
      }
      \new Voice = "bass" { \voiceTwo
      e4 e8 e8 e2 |
      e4 c2 c4 |
      c8 c4 c8 c8 c8 c4 |
      b4 b8 b8 b2 |
      g8 d4 g4 d8 g4 |
      c2 c4 c8 c8 |
      b2 b4 b4 |
      e8 e8 e8 e8 e2
      }
    >>
  >>
  \layout {}
  \midi {}
}
