\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	b2 c4 a8 c8 d4 e4 e2 e2 c8 a4 b8 d4 b4 d2 d8 d2 b4 b8 a8 g8 b2 g8 f8 d2 c4 d4 c4 e8 c8 e8 g8 b8 g8 
}

voiceTwo = \relative c' {
	\global
	d4 d4 e4 d4 e4 e4 f4 e4 c4 c4 d4 b4 c4 c4 e4 g4 e4 e4 g4 f4 e4 f4 d4 d4 f4 g4 g4 a4 c4 d4 f4 e4 
}

voiceThree = \relative c' {
	\global
	a2 g2 e2 d2 f2 f2 e2 g2 e2 g2 b2 c2 a2 g2 f2 d2 
}

voiceFour = \relative c' {
	\global
	e1 f1 d1 f1 a1 g1 f1 g1 
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