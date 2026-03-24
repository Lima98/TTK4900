
\version "2.24.0"

\score {
  <<
    \new Staff = "lead" {
      \clef treble
      \time 4/4
      a'4 g'4 gis'4 bes'4 |
  r4 f'4 e'4 d'4 |
  g'4 fis'4 f'4 g'4 |
  d'4 e'4 e'4 d'4
    }
    \new Staff = "bass" {
      \clef bass
      \time 4/4
      c'4 r4 c'4 c'4 |
  c'4 c'4 c'4 r4 |
  c'4 c'4 r4 c'4 |
  c'4 c'4 c'4 c'4
    }
  >>
  \layout {}
  \midi {}
}
