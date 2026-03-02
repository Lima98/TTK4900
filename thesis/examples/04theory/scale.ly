\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
  c4 d e f g a b c
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
    \omit TimeSignature
    \omit BarLine
    }
  }
}
