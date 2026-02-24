\version "2.24.4"
\language "english"

global = {
	\key c \major_pentatonic
	\time 4/4
}

voiceOne = \relative c' {
	\global
	g8 g4 e4 e8 d4 g4 d4 e4 a8 g8 g8 c4 g2 d8 a2 d2 
}

voiceOnea = \relative c' {
	\global
	g4 e4 c8 e8 c8 c8 a2 d8 g4 d8 c4 c4 d8 g8 c8 e8 g8 d2 d4 c8 
}

voiceOn = \relative c' {
	\global
	g2 c4 c4 g8 a8 g4 g2 e2 c4 c4 a8 g4 c8 e8 g8 g4 
}

voiceOe = \relative c' {
	\global
	c2 c8 d8 c4 d2 d2 e8 c8 e2 c4 c4 g2 e8 d8 
}

voicene = \relative c' {
	\global
	e2 g8 c8 a8 g8 e4 g2 d8 d8 e2 d4 a4 g4 a4 d4 a8 g8 
}

voicOne = \relative c' {
	\global
	g2 a8 a8 g4 e4 g2 c4 c4 a2 g4 c4 g4 d8 c8 c4 
}

voieOne = \relative c' {
	\global
	g2 e2 e8 a4 c2 g8 c4 d2 e4 a2 g4 c4 
}

voceOne = \relative c' {
	\global
	a2 a4 d4 e8 a4 g4 a8 d4 c4 a2 e8 c8 d4 d8 e8 d2 
}

viceOne = \relative c' {
	\global
	c2 g4 c4 g8 e4 c4 a8 c4 a4 c4 c4 a4 g8 c4 c2 g8 
}

oiceOne = \relative c' {
	\global
	e4 d4 a8 g8 g8 g8 d4 a8 c2 g8 d8 e8 c8 a4 c4 g8 a2 g2 
}

\score {
\new ChoirStaff <<
	\new Staff {
	\clef treble
	\voiceOne
}
	\new Staff {
	\clef treble
	\voiceOnea
}
	\new Staff {
	\clef treble
	\voiceOn
}
	\new Staff {
	\clef treble
	\voiceOe
}
	\new Staff {
	\clef treble
	\voicene
}
	\new Staff {
	\clef treble
	\voicOne
}
	\new Staff {
	\clef treble
	\voieOne
}
	\new Staff {
	\clef treble
	\voceOne
}
	\new Staff {
	\clef treble
	\viceOne
}
	\new Staff {
	\clef treble
	\oiceOne
}
	>>
	\midi {}
	\layout {}
}