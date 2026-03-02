\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	a2 c4 e8 d8 f8 d4 d4 e8 d8 e8 c4 a2 f4 d4 f4 a2 b4 b8 d2 b8 d8 f2 f4 e8 d4 d2 c8 e8 e8 g2 b8 d4 
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