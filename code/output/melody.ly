\version "2.24.4"
\language "english"

global = { 
	\key ef \major
	\time 4/4
}

voiceOne = \relative c' {
\global	  c   ef   d   f   g   af   c   af 
}

voiceTwo = \relative c' {
\global	  g   af   af   f   f   d   d   d 
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
	>>

		\midi {}
		\layout {}
}