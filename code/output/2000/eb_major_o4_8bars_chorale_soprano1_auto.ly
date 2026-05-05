\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key ef \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      g'4 bf'8 g'4 bf'4 g'8 |
      c'2 ef''2 |
      c'8 bf'4 c'8 af'2 |
      bf'8 g'4 bf'8 af'2 |
      bf'2 g'4 af'8 bf'8 |
      c'2 ef''8 c'4 af'8 |
      bf'8 d'2 bf'8 c'8 bf'8 |
      g'2 bf'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      ef'4 ef'8 ef'4 ef'4 ef'8 |
      c'2 g'2 |
      c'8 c'4 c'8 c'2 |
      d'8 d'4 d'8 d'2 |
      d'2 d'4 d'8 d'8 |
      c'2 af'8 c'4 c'8 |
      d'8 d'2 d'8 d8 d'8 |
      ef'2 ef'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key ef \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      bf4 g8 bf4 g4 bf8 |
      g2 g2 |
      af8 af4 af8 af2 |
      bf8 bf4 bf8 bf2 |
      bf2 bf4 bf8 bf8 |
      af2 af8 af4 af8 |
      bf8 bf2 bf8 d8 d8 |
      bf2 g2
      }
      \new Voice = "bass" { \voiceTwo
      ef4 ef8 ef4 ef4 ef8 |
      ef2 c2 |
      ef8 ef4 ef8 ef2 |
      f8 f4 f8 f2 |
      g2 g4 g8 g8 |
      ef2 c8 ef4 ef8 |
      f8 f2 f8 d,8 d,8 |
      ef2 ef2
      }
    >>
  >>
  \layout {}
  \midi {}
}
