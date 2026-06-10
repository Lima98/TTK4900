\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key af \minor
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      cf''2 ef''4 cf''8 df''8 |
      cf''2 cf''8 ef''4 cf''8 |
      df''4 ff''2 ef''8 df''8 |
      ef''2 ef''2 |
      cf''4 ef''8 gf''8 af''2 |
      ff''2 ff''2 |
      ef''8 cf''2 ef''8 ef''4 |
      cf''2 ef''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      ef''2 af'4 ef''8 af'8 |
      ff''2 ff''8 af'4 af''8 |
      af'4 af'2 af'8 af'8 |
      bf'2 bf'2 |
      ef''4 gf'8 gf'8 ef''2 |
      df''2 df''2 |
      bf'8 ef''2 bf'8 bf'4 |
      ef''2 af'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key af \minor
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      af'2 ef'4 ef'8 ef'8 |
      af'2 af'8 ff'4 af'8 |
      df'4 df'2 df'8 df'8 |
      g'2 g'2 |
      gf'4 ef'8 ef'8 cf'2 |
      af'2 af'2 |
      g'8 g'2 g'8 g'4 |
      af'2 ef'2
      }
      \new Voice = "bass" { \voiceTwo
      af2 af4 af8 af8 |
      ff2 ff8 ff4 ff8 |
      ff4 ff2 ff8 ff8 |
      ef'2 ef'2 |
      ef'4 gf8 gf8 gf2 |
      df'2 df'2 |
      ef'8 bf2 ef'8 ef'4 |
      af2 af2
      }
    >>
  >>
  \layout {}
  \midi {}
}
