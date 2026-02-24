\version "2.24.4"
\language "english"

global = {
	\key c \major_pentatonic
	\time 4/4
}

voiceOne = \relative c' {
	\global
	a2 d4 d4 e8 c2 a4 a8 g2 g4 c8 e8 e2 g4 d8 c8 
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