\version "2.24.4"
\language "english"

global = { 
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
\global	  d4   f4   d4   f4   ef2   c2   c4   d4   d4   c4   d2   c2 
}

voiceTwo = \relative c' {
\global	  ef4   g2   f8   ef8   g8   ef4   c4   c4   c8   af8   bf2   c4   af8   f2   g4   g4 
}

voiceThree = \relative c' {
\global	  g2   bf2   d8   f4   f4   g8   ef4   d8   bf4   bf2   bf8   bf8   g2   ef8   d4 
}

voiceFour = \relative c' {
\global	  c4   c8   c4   ef4   c8   ef4   d2   bf4   c4   d8   bf4   bf8   bf8   bf8   bf4   af4   c8   af8   c8   d8 
}

\score {
\new ChoirStaff <<
		\new Staff {
		 \clef treble
			\voiceOne
			}
		\new Staff {
		 \clef treble
			\voiceTwo
			}
		\new Staff {
		 \clef treble
			\voiceThree
			}
		\new Staff {
		 \clef treble
			\voiceFour
			}
	>>

		\midi {}
		\layout {}
}