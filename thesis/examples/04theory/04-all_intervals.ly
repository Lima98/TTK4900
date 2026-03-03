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
  <c' ef'>1 _\markup {"m3"}
  <c' e'>1 _\markup {"M3"}
  <c' f'>1 _\markup {"P4"}
  <c' fs'>2 _\markup {"A4/d5"}
  <c' gf'>2 
  <c' g'>1 _\markup {"P5"}
  <c' af'>1 _\markup {"m6"}
  <c' a'>1 _\markup {"M6"}
  <c' bf'>1 _\markup {"m7"}
  <c' b'>1 _\markup {"M7"}
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
