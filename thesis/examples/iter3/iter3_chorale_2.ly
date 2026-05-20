\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key c \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      e'2 g'8 e'4 g'8 |
      e'8 g'2 f'8 e'8 a'8 |
      f'4 g'4 a'8 g'8 f'4 |
      g'8 b'4 c''8 g'2 |
      e'4 g'4 e'2 |
      f'4 a'4 c''4 a'4 |
      g'8 e'4 g'4 e'4 g'8 |
      e'4 g'4 c''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      c'2 c'8 c'4 c'8 |
      c'8 c'2 c'8 c'8 c'8 |
      c'4 c'4 c'8 c'8 c'4 |
      d'8 d'4 d'8 d'2 |
      b4 b4 b2 |
      c'4 c'4 c'4 c'4 |
      d'8 d'4 d'4 d'4 d'8 |
      c'4 c'4 e'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key c \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      g2 e8 g4 e8 |
      a8 e2 e8 a8 e8 |
      f4 f4 f8 f8 f4 |
      b8 b4 b8 b2 |
      g4 g4 g2 |
      f4 f4 f4 f4 |
      b8 b4 b4 b4 b8 |
      g4 e4 g2
      }
      \new Voice = "bass" { \voiceTwo
      c2 c8 c4 c8 |
      c8 a,2 a,8 a,8 a,8 |
      a,4 a,4 a,8 a,8 a,4 |
      g8 g4 g8 g2 |
      b,4 e4 e2 |
      a,4 a,4 a,4 a,4 |
      g8 g4 g4 g4 g8 |
      c4 c4 c2
      }
    >>
  >>
  \layout {}
  \midi {}
}
