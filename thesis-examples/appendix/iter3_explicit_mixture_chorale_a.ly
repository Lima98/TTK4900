\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key a \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      cs''8 e''2 cs''8 d''8 e''8 |
      fs''2 e''2 |
      fs''8 fs''8 d''2 f''8 d''8 |
      cs''2 e''2 |
      cs''2 d''2 |
      cs''4 d''4 f''4 d''8 f''8 |
      e''4 cs''8 e''8 fs''8 fs''8 d''8 fs''8 |
      e''8 d''8 e''4 e''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      a'8 a'2 b'8 b'8 b'8 |
      cs''2 cs''2 |
      a'8 a'8 a'2 a'8 a'8 |
      a'2 b'2 |
      a'2 b'2 |
      a'4 a'4 a'4 a'8 a'8 |
      a'4 a'8 a'8 d''8 b'8 b'8 b'8 |
      b'8 b'8 b'4 cs''2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key a \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      e'8 cs'2 gs'8 gs'8 gs'8 |
      a'2 gs'2 |
      fs'8 fs'8 fs'2 f'8 f'8 |
      e'2 e'2 |
      e'2 g'2 |
      fs'4 fs'4 f'4 f'8 f'8 |
      cs'4 e'8 cs'8 d'8 d'8 fs'8 d'8 |
      gs'8 gs'8 gs'4 a'2
      }
      \new Voice = "bass" { \voiceTwo
      a8 a2 e'8 e'8 e'8 |
      fs2 cs'2 |
      d'8 d'8 d'2 d'8 d'8 |
      a2 gs2 |
      a2 g2 |
      d'4 d'4 d'4 d'8 d'8 |
      a4 a8 a8 b8 b8 b8 b8 |
      e'8 e'8 e'4 a2
      }
    >>
  >>
  \layout {}
  \midi {}
}
