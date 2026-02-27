\version "2.24.4"
\language "english"

global = {
	\key g \major
	\time 4/4
	\tempo 4 = 100
}

voiceOne = \relative c' {
	\global
	b2 g2 fs4 d4 c2 d2 c4 c4 a2 c4 d4 e4 e2 c4 d2 c2 a4 fs2 a4 b4 g2 b4 b2 g2 fs4 d4 c2 d2 c4 c4 a2 c4 d4 e4 e2 c4 d2 c2 a4 fs2 a4 b4 g2 b4 e4 fs4 e8 fs4 d8 e4 fs4 a4 a4 a4 b8 a8 fs8 a4 fs8 e8 e4 c8 d8 c8 b8 d8 e4 c4 c4 e8 g8 e8 e8 g8 g4 b4 b8 d8 fs8 fs4 e4 c4 d8 d8 c8 b4 c8 b8 b8 b2 g2 fs4 d4 c2 d2 c4 c4 a2 c4 d4 e4 e2 c4 d2 c2 a4 fs2 a4 b4 g2 b4 
}

voiceFour = \relative c' {
	\global
	b2 g2 e2 c2 c2 d2 e2 e2 a2 c2 a1 g1 g2 a2 b2 g2 e2 c2 c2 d2 e2 e2 a2 c2 a1 g1 g2 a2 e4 d4 c4 b4 g4 e2 c4 c2 b4 g4 g4 a2 b4 b2 g2 g2 e4 fs4 d4 c2 d4 c2 c4 a4 b2 g2 e2 c2 c2 d2 e2 e2 a2 c2 a1 g1 g2 a2 
}

\score {
\new ChoirStaff <<
	\new Staff {
	\clef treble
	\voiceOne
}
	\new Staff {
	\clef bass
	\voiceFour
}
	>>
	\midi {}
	\layout {}
}