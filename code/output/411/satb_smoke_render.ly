\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key c \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      e'8 g'8 e'4 g'8 g'8 a'8 g'8 |
      e'4 a'8 g'8 e'2 |
      f'2 g'2 |
      b'2 c''2 |
      b'8 g'2 e'8 g'8 e'8 |
      f'2 a'2 |
      g'2 g'2 |
      e'4 e'4 g'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      c'8 c'8 c'4 c'8 c'8 e'8 e'8 |
      c'4 c'8 c'8 c'2 |
      c'2 c'2 |
      b2 d'2 |
      e'8 e'2 b8 b8 b8 |
      c'2 c'2 |
      d'2 d'2 |
      c'4 c'4 c'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key c \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      g8 e8 g4 e8 e8 g8 c'8 |
      a4 e8 e8 a2 |
      f2 f2 |
      g2 g2 |
      g8 b2 g8 g8 g8 |
      f2 f2 |
      b2 b2 |
      g4 g4 e2
      }
      \new Voice = "bass" { \voiceTwo
      c8 c8 c4 c8 c8 c8 c8 |
      c4 a,8 a,8 a,2 |
      a,2 a,2 |
      d2 b,2 |
      e8 e2 e8 e8 e8 |
      a,2 a,2 |
      g2 g2 |
      c4 c4 c2
      }
    >>
  >>
  \layout {}
  \midi {}
}
