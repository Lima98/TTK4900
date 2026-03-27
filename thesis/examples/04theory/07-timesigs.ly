\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
  \numericTimeSignature
}

voiceOne = \relative c'' {
	\global
  \time 4/4
  g4 g g g |
  \time 3/4
  g g g |
  \time 2/4
  g g |
  \time 2/2
  g2 g |
  \time 6/8
  g8 g g g g g |
}

\score {
\new ChoirStaff <<
	\new Staff {
	\clef treble
	\voiceOne
}
	>>
	\midi {}
	\layout {
    \context {
    \Staff
    }
  }
}
