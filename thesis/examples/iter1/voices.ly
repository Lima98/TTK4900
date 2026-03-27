\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	e2 d2 d2 b4 b4 d8 b8 c2 a4 a4 a2 a4 
}

voiceTwo = \relative c' {
	\global
	d4 f4 g4 f4 f4 a4 c4 b4 b4 b4 g4 e4 g4 b4 a4 a4 
}

voiceThree = \relative c' {
	\global
	b2 d2 d2 d2 e2 d2 c2 d2 
}

voiceFour = \relative c' {
	\global
	d1 f1 d1 f1 
}

\score {
\new ChoirStaff <<
	\new Staff {
	\clef treble
	\voiceOne
}
	\new Staff {
	\clef "treble_8"
	\voiceTwo
}
	\new Staff {
	\clef bass
	\voiceThree
}
	\new Staff {
	\clef bass
	\voiceFour
}
	>>
	\midi {}
	\layout {}
}