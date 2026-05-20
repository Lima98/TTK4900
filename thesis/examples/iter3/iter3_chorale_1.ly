\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key c \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      e'4 g'8 e'4 g'4 e'8 |
      a'2 c''2 |
      a'8 g'4 a'8 f'2 |
      g'8 e'4 g'8 f'2 |
      g'2 e'4 f'8 g'8 |
      a'2 c''8 a'4 f'8 |
      g'8 b'2 g'8 a'8 g'8 |
      e'2 g'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      c'4 c'8 c'4 c'4 c'8 |
      e'2 e'2 |
      f'8 f'4 f'8 c'2 |
      b8 d'4 d'8 d'2 |
      e'2 b4 b8 b8 |
      c'2 c'8 c'4 c'8 |
      d'8 d'2 d'8 d'8 d'8 |
      c'2 c'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key c \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      g4 e8 g4 e4 g8 |
      c'2 a2 |
      c'8 c'4 c'8 a2 |
      g8 b4 b8 b2 |
      b2 g4 g8 g8 |
      f2 f8 f4 f8 |
      b8 b2 b8 b8 b8 |
      g2 e2
      }
      \new Voice = "bass" { \voiceTwo
      c4 c8 c4 c4 c8 |
      a,2 a,2 |
      f8 a4 f8 f2 |
      d8 g4 g8 g2 |
      e2 e4 e8 e8 |
      c2 a,8 a,4 a,8 |
      g8 g2 g8 g8 g8 |
      c2 c2
      }
    >>
  >>
  \layout {}
  \midi {}
}
