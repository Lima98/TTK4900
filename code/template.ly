\version "2.24.4"
\language "english"

music = {
  \relative c' {
    c4 d e f
  }
}

\score {
  % The music is defined in the variable "music" above, and is inserted here.
	 \new Staff {
      \clef treble
      \key ef \major
      \time 4/4
      \music
    }
  % End of music

		\midi {}
		\layout {}
}
