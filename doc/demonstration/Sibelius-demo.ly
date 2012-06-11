\version "2.14.2"

\header {
  % Remove default LilyPond tagline
  tagline = ##f
}

\paper {
  #(set-paper-size "letter")
}

\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
}

global = {
  \key c \major
  \numericTimeSignature
  \time 3/2
}

rightOne = \relative c' {
  \global
  % Music follows here.
  
  d='2. d4( e f | g2.) g4( a b | c2.) c4( d e | f1) e2 | e1. |
  
}

rightTwo = \relative c' {
  \global
  % Music follows here.
  
  c='1. | b2. b4( c d | <e g>2.) <e g>4( <d f> <c e g> | <c a'>2) <d b'>1 | <c c'>1. |
  
}

leftOne = \relative c {
  \global
  % Music follows here.
  
  <c= f>1. | a' | g2. e4( f g | a2) g1 | g1. |
  
}

leftTwo = \relative c, {
  \global
  % Music follows here.
  
  f=,1. | f' | e | d2 g,1 | c,1. |
  
}

\score {
  \new PianoStaff \with {
    % instrumentName = "Piano"
  } <<
    \new Staff = "right" << \rightOne \\ \rightTwo >>
    \new Staff = "left" { \clef bass << \leftOne \\ \leftTwo >> }
  >>
  \layout { }
}
