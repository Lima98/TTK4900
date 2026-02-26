// =====================================================
// NTNU THESIS TEMPLATE – Typst Version
// Fully working (Typst 0.11+)
// =====================================================


// -----------------------------
// PAGE + TEXT SETUP
// -----------------------------

#set page(
  margin: (left: 3cm, right: 2.5cm, top: 2.5cm, bottom: 2.5cm),
  numbering: "i",
  number-align: center,
)

#set text(
  font: "Times New Roman",
  size: 12pt,
)

#set par(leading: 1.5em)


// -----------------------------
// COUNTERS
// -----------------------------

#let chapter-counter = counter("chapter")
#let appendix-mode = state("appendix", false)


// -----------------------------
// TITLE PAGE
// -----------------------------

#let titlepage(
  title,
  subtitle,
  program,
  supervisor,
  cosupervisor,
  date,
  faculty,
  department,
) = [
  #set page(numbering: none)

  #align(center)[
    #v(2cm)
    #text(size: 20pt, weight: "bold")[#title]
    #v(0.5cm)
    #subtitle
    #v(1.5cm)

    Master’s thesis in #program \
    Supervisor: #supervisor \
    Co-supervisor: #cosupervisor

    #v(1cm)
    #date

    #v(2cm)
    Norwegian University of Science and Technology \
    #faculty \
    #department
  ]

  #pagebreak()
  #set page(numbering: "i")
]


// -----------------------------
// CHAPTER COMMAND
// -----------------------------

#let chapter(title) = [
  #pagebreak()

  #chapter-counter.step()

  // Reset figure and table counters per chapter
  #counter(figure).update(0)
  #counter(table).update(0)

  #align(center)[
    #text(weight: "bold")[CHAPTER]
    #v(0.5cm)

    #v(0.5cm)
  ]

  #v(1cm)
]

// -----------------------------
// FIGURE + TABLE NUMBERING
// -----------------------------

#show figure: it => [
]

#show table: it => [
  #let num = chapter-counter.get() + "." + counter(table).step()
  Table #num: #it.body
]


// =====================================================
// DOCUMENT START
// =====================================================


// -----------------------------
// TITLE PAGE
// -----------------------------

#titlepage(
  "The title of your master’s thesis should be written here",
  "Any undertitle is written here",
  "Physics and Mathematics",
  "Supervisor Name",
  "Co-supervisor Name",
  "June 2022",
  "Faculty of Natural Sciences",
  "Department of Physics",
)


// -----------------------------
// FRONT MATTER
// -----------------------------

#chapter("Abstract")
Write your abstract here.

#chapter("Preface")
Write your preface here.

#chapter("Contents")
#outline()

#pagebreak()

#chapter("List of Figures")
#outline(target: figure)

#pagebreak()

#chapter("List of Tables")
#outline(target: table)

#pagebreak()

#chapter("Abbreviations")

• EDA — Exploratory Data Analysis  
• GNSS — Global Navigation Satellite System  
• NTNU — Norwegian University of Science and Technology  


// -----------------------------
// MAIN MATTER
// -----------------------------

#set page(numbering: "1")

#chapter("Introduction")

== Motivation

Some text here.

== Project description

More text.


#chapter("Theory")

== Equations

$ r = 2\pi^2 $

== A Figure

#figure(
  rect(width: 4cm, height: 3cm),
  caption: "Example figure.",
)


#chapter("Methods")

== Section One

=== Subsection One


#chapter("Results")

#figure(
  rect(width: 4cm, height: 3cm),
  caption: "Trajectory example.",
)


#chapter("Discussion")

Discussion text.


#chapter("Conclusions")

Final summary text.


// -----------------------------
// REFERENCES
// -----------------------------

#pagebreak()
#chapter("References")

// #bibliography("refs.bib")


// -----------------------------
// APPENDIX
// -----------------------------

#appendix-mode.update(true)
#chapter-counter.update(0)

#chapter("Github Repository")

Repository link here.

#chapter("Additional Tables")

Extra material here.
