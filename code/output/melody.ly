\version "2.24.4"
\language "english"

global = { 
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
\global	  ef8   f8   d8   f8   f8   af8   bf8   g8   af8   c8   af8   c8   c8   ef8   ef8   d8   ef8   ef8   ef8   c8   af8   g8   af8   f8   d8   f8   af8   bf8   g8   g8   ef8   ef8 
}

voiceTwo = \relative c' {
\global	  ef4   g4   af4   g4   ef4   d4   f4   af4   g4   af4   f4   f4   d4   d4   c4   af4 
}

voiceThree = \relative c' {
\global	  d2   d2   f2   g2   g2   f2   g2   f2 
}

voiceFour = \relative c' {
\global	  g1   f1   f1   f1 
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