\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key bf \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      d''2 f''4 ef''4 |
      d''8 d''8 ef''4 d''2 |
      ef''4 d''4 ef''4 d''4 |
      g''2 f''2 |
      a''4 bf''4 a''2 |
      bf''8 a''8 bf''4 a''2 |
      bf''4 g''8 ef''2 gf''8 |
      f''4 ef''8 d''8 f''2 |
      d''2 ef''4 d''4 |
      ef''8 g''4 ef''4 gf''8 ef''4 |
      f''2 d''8 f''4 d''8 |
      ef''4 g''4 f''2 |
      g''4 bf''8 f''8 g''8 ef''8 g''8 ef''8 |
      g''4 f''4 g''2 |
      f''2 f''8 a''8 f''4 |
      g''2 bf''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      bf'2 c''4 c''4 |
      bf'8 bf'8 bf'4 a'2 |
      bf'4 bf'4 d''4 bf'4 |
      ef''2 c''2 |
      d''4 d''4 f''2 |
      d''8 d''8 d''4 d''2 |
      bf'4 bf'8 bf'2 bf'8 |
      bf'4 d''8 bf'8 c''2 |
      bf'2 c''4 c''4 |
      bf'8 bf'4 bf'4 bf'8 bf'4 |
      bf'2 bf'8 bf'4 bf'8 |
      c''4 c''4 c''2 |
      d''4 d''8 d''8 ef''8 bf'8 bf'8 bf'8 |
      c''4 ef''4 a'2 |
      bf'2 a'8 a'8 a'4 |
      bf'2 d''2
      }
    >>
    \new Staff <<
      \clef "treble_8"
      \key bf \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      f'2 f'4 f'4 |
      g'8 g'8 d'4 f'2 |
      ef'4 ef'4 f'4 f'4 |
      ef'2 a'2 |
      bf'4 bf'4 c''2 |
      bf'8 bf'8 bf'4 f'2 |
      ef'4 ef'8 ef'2 ef'8 |
      d'4 f'8 f'8 f'2 |
      f'2 af'4 ef'4 |
      ef'8 ef'4 ef'4 ef'8 ef'4 |
      d'2 g'8 d'4 g'8 |
      g'4 ef'4 a'2 |
      bf'4 bf'8 bf'8 bf'8 g'8 g'8 g'8 |
      ef'4 g'4 f'2 |
      f'2 f'8 f'8 f'4 |
      f'2 f'2
      }
      \new Voice = "bass" { \voiceTwo
      bf2 a4 a4 |
      g8 g8 g4 d'2 |
      g4 g4 bf4 bf4 |
      c'2 f'2 |
      f'4 f'4 f'2 |
      g'8 g'8 g'4 d'2 |
      g4 g8 g2 gf8 |
      bf4 bf8 bf8 a2 |
      bf2 af4 af4 |
      g8 g4 g4 gf8 gf4 |
      bf2 bf8 g4 g8 |
      c'4 c'4 f'2 |
      f'4 f'8 bf8 ef'8 ef'8 ef'8 ef'8 |
      c'4 c'4 c'2 |
      d'2 c'8 c'8 c'4 |
      d'2 bf2
      }
    >>
  >>
  \layout {}
  \midi {}
}
