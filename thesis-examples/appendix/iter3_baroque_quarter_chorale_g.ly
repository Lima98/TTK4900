\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key g \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      b'4 d''4 b'4 c''4 |
      e''4 c''4 e''4 c''4 |
      fs''4 g''4 fs''4 g''4 |
      fs''4 g''4 fs''2 |
      g''4 e''4 g''4 e''4 |
      g''4 e''4 c''4 e''4 |
      d''4 c''4 b'4 d''4 |
      b'4 d''4 d''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      g'4 g'4 g'4 b'4 |
      c''4 g'4 g'4 g'4 |
      a'4 a'4 a'4 a'4 |
      b'4 d''4 d''2 |
      e''4 b'4 b'4 b'4 |
      c''4 c''4 a'4 a'4 |
      a'4 a'4 a'4 a'4 |
      g'4 g'4 g'2
      }
    >>
    \new Staff <<
      \clef "treble_8"
      \key g \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      d'4 b4 d'4 d'4 |
      c'4 e'4 e'4 e'4 |
      c'4 c'4 c'4 c'4 |
      d'4 fs'4 b'2 |
      b'4 g'4 e'4 g'4 |
      e'4 a'4 e'4 c'4 |
      fs'4 fs'4 fs'4 fs'4 |
      d'4 b4 b2
      }
      \new Voice = "bass" { \voiceTwo
      g4 g4 g4 g4 |
      g4 c'4 c'4 c'4 |
      fs4 fs4 fs4 fs4 |
      b4 b4 b2 |
      e4 e4 e4 e4 |
      a4 a4 a4 a4 |
      d'4 d'4 d'4 d'4 |
      g4 g4 g2
      }
    >>
  >>
  \layout {}
  \midi {}
}
