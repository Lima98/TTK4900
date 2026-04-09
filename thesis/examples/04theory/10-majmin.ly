\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \absolute {
	\global
  <c' e' g'>1 _\markup {"Maj."}
  s1 
  <c' ef' g'>1 _\markup {"Min."}
  s1
  <c' ef' gf'>1 _\markup {"Dim."}
  s1
  <c' e' gs'>1 _\markup {"Aug."}
  s1
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
