\version "2.24.4"
\language "english"

\score {
  \new ChoirStaff <<
    \new Staff <<
      \clef "treble"
      \key e \major
      \time 4/4
      \new Voice = "soprano" { \voiceOne
      gs'4 b'2 gs'8 b'8 |
      cs''2 b'8 gs'8 a'8 gs'8 |
      a'4 b'4 cs''4 a'8 cs''8 |
      b'8 gs'8 a'4 b'2 |
      gs'4 b'2 gs'4 |
      cs''2 e''2 |
      cs''2 b'4 gs'8 b'8 |
      b'8 gs'8 b'4 b'2 \bar "|."
      }
      \new Voice = "alto" { \voiceTwo
      e'4 gs'2 gs'8 gs'8 |
      gs'2 gs'8 gs'8 gs'8 gs'8 |
      e'4 a'4 a'4 a'8 a'8 |
      fs'8 fs'8 fs'4 fs'2 |
      gs'4 gs'2 gs'4 |
      a'2 a'2 |
      b'2 fs'4 fs'8 fs'8 |
      gs'8 gs'8 gs'4 gs'2
      }
    >>
    \new Staff <<
      \clef "treble"
      \key e \major
      \time 4/4
      \new Voice = "tenor" { \voiceOne
      e'4 e'2 e'8 e'8 |
      e'2 e'8 e'8 e'8 e'8 |
      e'4 e'4 e'4 e'8 e'8 |
      ds'8 ds'8 ds'4 ds'2 |
      ds'4 ds'2 ds'4 |
      e'2 e'2 |
      fs'2 ds'4 ds'8 ds'8 |
      e'8 e'8 e'4 e'2
      }
      \new Voice = "bass" { \voiceTwo
      b4 b2 b8 b8 |
      cs'2 cs'8 cs'8 cs'8 cs'8 |
      cs'4 cs'4 cs'4 cs'8 cs'8 |
      b8 b8 b4 b2 |
      b4 b2 b4 |
      cs'2 cs'2 |
      ds'2 b4 b8 b8 |
      b8 b8 b4 b2
      }
    >>
  >>
  \layout {}
  \midi {}
}
