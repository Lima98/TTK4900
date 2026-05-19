
\version "2.24.0"

\score {
  <<
    \new Staff = "lead" {
      \clef treble
      \time 4/4
      g'4 a'4 b'4 r4 |
  a'4 b'4 cis''4 d''4 |
  g'4 a'4 a'4 g'4 |
  d'4 ees'4 d'4 c'4 |
  e'4 d'4 d'4 d'4 |
  b'4 bes'4 b'4 bes'4 |
  f'4 f'4 ees'4 f'4 |
  c'4 c'4 cis'4 cis'4
    }
    \new Staff = "bass" {
      \clef bass
      \time 4/4
      c'4 c'4 c'4 c'4 |
  c'4 c'4 c'4 c'4 |
  c'4 c'4 c'4 c'4 |
  c'4 c'4 c'4 c'4 |
  c'4 c'4 c'4 r4 |
  r4 c'4 c'4 c'4 |
  c'4 c'4 c'4 c'4 |
  c'4 c'4 c'4 c'4
    }
  >>
  \layout {}
  \midi {}
}
