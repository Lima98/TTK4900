\version "2.24.4"
\language "english"

global = {
	\key c \major_pentatonic
	\time 4/4
}

voiceOne = \relative c' {
	\global
	a4 c4 a4 e4 
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