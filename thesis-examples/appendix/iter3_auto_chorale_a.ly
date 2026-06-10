\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key a \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      cs''2 cs''4 d''8 e''8 |
      fs''2 cs''2 |
      d''8 fs''2 fs''4 r8 |
      e''2 e''2 |
      cs''4 e''8 cs''8 e''8 cs''8 e''4 |
      fs''2 a''2 |
      gs''2 e''8 cs''4 e''8 |
      cs''8 e''4 cs''8 e''2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      a'2 a'4 cs''8 a'8 |
      a'2 a'2 |
      a'8 a'2 a'4 r8 |
      b'2 b'2 |
      gs'4 gs'8 gs'8 gs'8 gs'8 gs'4 |
      a'2 a'2 |
      e''2 b'8 b'4 b'8 |
      a'8 a'4 a'8 a'2
      }
    >>
    \new Staff <<
      \clef "bass"
      \key a \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      e'2 e'4 e'8 cs'8 |
      cs'2 fs'2 |
      d'8 d'2 d'4 r8 |
      gs'2 gs'2 |
      e'4 e'8 e'8 e'8 e'8 e'4 |
      d'2 d'2 |
      e'2 gs'8 gs'4 gs'8 |
      e'8 cs'4 e'8 cs'2
      }
      \new Voice = "bass" { \voiceTwo
      a2 a4 a8 a8 |
      fs2 fs2 |
      fs8 fs2 fs4 r8 |
      e'2 e'2 |
      gs4 cs'8 cs'8 cs'8 cs'8 cs'4 |
      a2 fs2 |
      b2 e'8 e'4 e'8 |
      a8 a4 a8 a2
      }
    >>
  >>
  \layout {}
  \midi {}
}
