\version "2.24.4"
\language "english"

global = { 
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
\global	  ef8   d8   ef8   c8   bf8   g8   f8   d8   f8   d8   ef8   g8   ef8   f8   f8   d8   f8   ef8   c8   ef8   f8   af8   g8   f8   d8   ef8   d8   bf8   d8   bf8   af8   bf8 
}

voiceTwo = \relative c' {
\global	  g4   af4   bf4   d4   f4   af4   f4   af4   c4   af4   c4   af4   c4   bf4   af4   bf4 
}

voiceThree = \relative c' {
\global	  d2   ef2   g2   g2   af2   f2   af2   f2 
}

voiceFour = \relative c' {
\global	  c1   bf1   g1   bf1 
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