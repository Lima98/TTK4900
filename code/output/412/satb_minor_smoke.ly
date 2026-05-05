\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key ef \minor
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      gf'4 bf'2 gf'8 bf'8 |
      gf'8 bf'8 gf'4 bf'8 gf'8 bf'4 |
      af'4 af'8 cf'8 af'2 |
      bf'2 cf'2 |
      ef''8 df'4 bf'2 cf'8 |
      bf'2 af'4 bf'4 |
      gf'4 cf'2 gf'4 |
      bf'4 gf'4 bf'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      ef'4 ef'2 ef'8 ef'8 |
      ef'8 ef'8 ef'4 ef'8 ef'8 ef'4 |
      ef'4 ef'8 ef'8 ef'2 |
      ef'2 ef'2 |
      f'8 d4 d'2 d'8 |
      d'2 d'4 d'4 |
      ef'4 gf'2 ef'4 |
      ef'4 ef'4 ef'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key ef \minor
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      bf4 gf2 bf8 gf8 |
      bf8 gf8 bf4 gf8 bf8 gf4 |
      cf4 cf8 cf8 cf2 |
      cf2 cf2 |
      bf8 d4 d2 d8 |
      bf2 bf4 bf4 |
      bf4 bf2 bf4 |
      gf4 bf4 gf2
      }
      \new Voice = "bass" { \voiceTwo
      ef4 ef2 ef8 ef8 |
      ef8 ef8 ef4 ef8 ef8 ef4 |
      af4 af8 af8 af2 |
      af2 af2 |
      d8 d,4 d,2 d,8 |
      f2 f4 f4 |
      ef4 ef2 ef4 |
      ef4 ef4 ef2
      }
    >>
  >>
  \layout {}
  \midi {}
}
