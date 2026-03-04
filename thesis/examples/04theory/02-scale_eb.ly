\version "2.24.4"
\language "english"

global = {
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
  ef4 f g af bf c d ef
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
