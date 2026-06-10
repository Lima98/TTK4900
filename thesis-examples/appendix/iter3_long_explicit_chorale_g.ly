\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key g \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      b'8 d''8 b'2 d''4 |
      b'2 d''4 e''8 fs''8 |
      g''2 d''2 |
      c''4 b'4 d''2 |
      g''4 g''4 fs''8 g''4 fs''8 |
      g''4 e''4 d''2 |
      c''4 e''4 c''8 ef''8 c''4 |
      d''4 d''8 b'8 d''2 |
      c''4 b'8 d''2 c''8 |
      b'2 d''4 c''8 c''8 |
      b'4 d''2 b'8 d''8 |
      b'8 e''4 fs''8 g''2 |
      d''8 fs''2 e''8 r8 d''8 |
      e''4 c''2 ef''8 c''8 |
      d''2 e''4 c''8 e''8 |
      d''4 e''8 fs''8 g''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      g'8 g'8 g'2 a'4 |
      g'2 fs'4 fs'8 fs'8 |
      c''2 b'2 |
      a'4 a'4 a'2 |
      b'4 b'4 d''8 a'4 a'8 |
      b'4 b'4 b'2 |
      g'4 g'4 g'8 g'8 g'4 |
      g'4 g'8 g'8 g'2 |
      b'4 g'8 g'2 a'8 |
      g'2 g'4 g'8 g'8 |
      g'4 g'2 fs'8 fs'8 |
      g'8 g'4 g'8 a'2 |
      a'8 a'2 b'8 r8 g'8 |
      g'4 g'2 g'8 g'8 |
      g'2 c''4 a'8 a'8 |
      a'4 a'8 a'8 b'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key g \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      d'8 b8 d'2 d'4 |
      e'2 d'4 d'8 d'8 |
      c'2 d'2 |
      e'4 e'4 fs'2 |
      g'4 g'4 a'8 fs'4 fs'8 |
      e'4 g'4 fs'2 |
      e'4 e'4 ef'8 ef'8 ef'4 |
      b4 b8 d'8 b2 |
      d'4 d'8 b2 c'8 |
      e'2 ef'4 ef'8 ef'8 |
      d'4 b2 d'8 d'8 |
      e'8 b4 b8 c'2 |
      d'8 d'2 d'8 r8 b8 |
      c'4 e'2 ef'8 ef'8 |
      b2 c'4 e'8 c'8 |
      fs'4 fs'8 fs'8 d'2
      }
      \new Voice = "bass" { \voiceTwo
      g8 g8 g2 fs4 |
      e2 b4 b8 b8 |
      e2 g2 |
      a4 c'4 d'2 |
      d'4 d'4 d'8 d'4 d'8 |
      e4 e4 b2 |
      c'4 c'4 c'8 c'8 c'4 |
      g4 g8 g8 g2 |
      g4 g8 g2 f8 |
      c'2 c'4 c'8 c'8 |
      g4 g2 b8 b8 |
      e8 e4 e8 e2 |
      fs8 fs2 g8 r8 g8 |
      g4 c'2 c'8 c'8 |
      g2 a4 a8 a8 |
      d'4 d'8 d'8 g2
      }
    >>
  >>
  \layout {}
  \midi {}
}
