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
      e'4 g'4 e'2 |
      f'8 a'8 a'4 f'2 |
      g'4 b'8 g'8 a'2 |
      g'4 e'4 g'4 e'8 g'8 |
      c''8 a'8 f'2 a'4 |
      g'4 a'2 g'4 |
      e'2 g'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      c'2 c'8 c'4 c'8 |
      c'4 c'4 c'2 |
      c'8 c'8 c'4 c'2 |
      d'4 d'8 d'8 d'2 |
      e'4 b4 b4 b8 b8 |
      c'8 c'8 c'2 c'4 |
      d'4 d'2 d'4 |
      c'2 c'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key c \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      g2 e8 g4 e8 |
      a4 e4 a2 |
      f8 f8 f4 f2 |
      b4 b8 b8 b2 |
      b4 g4 g4 g8 g8 |
      f8 f8 f2 f4 |
      b4 b2 b4 |
      g2 e2
      }
      \new Voice = "bass" { \voiceTwo
      c2 c8 c4 c8 |
      c4 a,4 a,2 |
      a,8 a,8 a,4 a,2 |
      g4 g8 g8 g2 |
      e4 e4 e4 e8 e8 |
      a,8 a,8 a,2 a,4 |
      g4 g2 g4 |
      c2 c2
      }
    >>
  >>
  \layout {}
  \midi {}
}
