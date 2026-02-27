\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	a8 f2 a8 f8 f8 f4 g4 e4 c8 d8 d2 b2 d8 b4 a4 b4 a8 c8 a8 c2 c4 c4 a2 b8 a8 a2 c8 e8 d8 f8 f2 g4 a8 f8 
}

voiceTwo = \relative c' {
	\global
	a4 c4 d4 e4 g4 b4 a4 g4 f4 g4 f4 f4 a4 c4 e4 f4 d4 d4 b4 a4 c4 c4 e4 c4 a4 c4 e4 f4 e4 g4 b4 d4 
}

voiceThree = \relative c' {
	\global
	b2 a2 a2 g2 g2 a2 a2 a2 g2 e2 g2 e2 f2 d2 f2 g2 
}

voiceFour = \relative c' {
	\global
	b1 a1 g1 a1 g1 b1 g1 f1 
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