\version "2.24.4"
\language "english"

global = { 
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
\global	  ef8   d8   f8   ef8   d8   c8   ef8   g8   g8   bf8   bf8   af8   g8   f8   ef8   c8   d8   bf8   g8   ef8   ef8   d8   d8   ef8   ef8   g8   bf8   af8   bf8   bf8   d8   d8 
}

voiceTwo = \relative c' {
\global	  ef4   d4   ef4   c4   ef4   d4   ef4   f4   ef4   g4   g4   bf4   af4   f4   d4   d4 
}

voiceThree = \relative c' {
\global	  g2   bf2   g2   ef2   f2   g2   bf2   g2 
}

voiceFour = \relative c' {
\global	  f1   ef1   g1   f1 
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