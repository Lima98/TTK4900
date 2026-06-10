\version "2.24.4"
\language "english"

global = {
  \key d \major
  \omit Staff.TimeSignature
  \omit Staff.BarLine
}

triads = \absolute {
  \global
  <d' fs' a'>1^\markup \center-column { "I" "Tonic" }
  <e' g' b'>1^\markup \center-column { "ii" "Predominant" }
  <fs' a' cs''>1^\markup \center-column { "iii" "Mediant" }
  <g' b' d''>1^\markup \center-column { "IV" "Predominant" }
  <a' cs'' e''>1^\markup \center-column { "V" "Dominant" }
  <b' d'' fs''>1^\markup \center-column { "vi" "Submediant" }
  <cs'' e'' g''>1^\markup \center-column { "vii°" "Dominant" }
}

\score {
  \new Staff {
    \clef treble
    \triads
  }
  \midi {}
  \layout {
    indent = 0
    short-indent = 0
    ragged-right = ##f
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/1)
      \override SpacingSpanner.common-shortest-duration = #(ly:make-moment 1/1)
      \override SpacingSpanner.shortest-duration-space = #1.8
    }
    \context {
      \Staff
      \remove "Time_signature_engraver"
      \remove "Bar_engraver"
    }
  }
}
