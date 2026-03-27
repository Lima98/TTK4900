\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	e2 e8 d4 b8 d4 d4 e4 e8 d8 e8 e4 c8 b4 g4 f2 d8 c8 c4 b2 d4 c4 a8 g8 a8 b4 g8 f4 e4 f8 a8 a4 a8 g8 e2 d2 c4 a8 b8 c8 e8 e4 e8 f8 g2 a8 c8 c2 c2 a4 c2 c8 c8 d4 b2 c8 e8 e2 f4 e8 d8 b4 b8 d4 d8 c4 a4 g8 e4 f4 g8 
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