\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \absolute {
	\global
  <c' df'>1 _\markup {"m2"}
  <c' d'>1 _\markup {"M2"}
  <c' f'>1 _\markup {"P4"}
  <c' fs'>2 _\markup {"A4/d5"}
  <c' gf'>2 
  <c' af'>1 _\markup {"m6"}
  <c' bf'>1 _\markup {"m7"}
  <c' b'>1 _\markup {"M7"}
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
