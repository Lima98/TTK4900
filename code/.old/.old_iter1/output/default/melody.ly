\version "2.24.4"
\language "english"

global = {
	\key c \major
	\time 4/4
}

voiceOne = \relative c' {
	\global
	a2 a8 b8 c8 a8 c4 a4 b4 a8 b8 g2 b8 d4 f8 f8 a2 b4 c8 
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