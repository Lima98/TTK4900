\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \absolute {
	\global
  <c' d'>1 _\markup {"2nd"}
  <c' e'> _\markup {"3rd"}
  <c' f'> _\markup {"4th"}
  <c' g'> _\markup {"5th"}
  <c' a'> _\markup {"6th"}
  <c' b'> _\markup {"7th"}
  <c' c''> _\markup {"8th"}
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
