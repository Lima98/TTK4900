\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \absolute {
	\global
  <c' ef'>1 _\markup {"m3"}
  <c' e'>1 _\markup {"M3"}
  <c' gf'>2 
  <c' g'>1 _\markup {"P5"}
  <c' a'>1 _\markup {"M6"}
  <c' c''>1 _\markup {"P8"}
}

\score {
\new ChoirStaff <<
	\new Staff {
	\clef treble
	\voiceOne
}
	>>
	\midi {}
	\layout {}
}
