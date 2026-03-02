// -------------------------
// PAGE SETUP
// -------------------------

#set page(
  paper: "a4",
  margin: (left: 3cm, right: 2.5cm, top: 2.5cm, bottom: 2.5cm),
  numbering: "1",
)

#set text(
  font: "Times New Roman",
  size: 12pt,
)

#set par(
  leading: 1.5em,
  spacing: 1em,
)

#set heading(
  numbering: "1.1",
)

// -------------------------
// TITLE PAGE
// -------------------------

#let titlepage(
  author,
  title,
  subtitle,
  program,
  supervisor,
  cosupervisor,
  date,
) = [
  #align(center)[
    #v(3cm)
    #text(size: 20pt, weight: "bold")[#title]
    #v(0.5cm)
    #text(size: 16pt)[#subtitle]
    #v(1.5cm)

    #text(size: 14pt)[Master’s thesis in #program]

    #v(0.5cm)
    Supervisor: #supervisor \
    Co-supervisor: #cosupervisor

    #v(1cm)
    #date

    #v(2cm)
    Norwegian University of Science and Technology \
    Faculty of Natural Sciences \
    Department of Physics
  ]

  #pagebreak()
]

// -------------------------
// CHAPTER STYLE
// -------------------------

#let chapter(title) = [
  #pagebreak()
  #align(center)[
    CHAPTER

    #v(0.5cm)
    #upper(counter(heading).display())
    #v(0.5cm)

    #upper(title)
  ]
  #v(1cm)
]

// -------------------------
// DOCUMENT START
// -------------------------

#titlepage(
  author: "Nina Salvesen",
  title: "The title of your master’s thesis should be written here",
  subtitle: "Any undertitle is written here",
  program: "Physics and Mathematics",
  supervisor: "Supervisor Name",
  cosupervisor: "Co-supervisor Name",
  date: "June 2022",
)

// Roman numbering for frontmatter
#set page(numbering: "i")

= ABSTRACT

Write abstract here.

#pagebreak()

= PREFACE

Write preface here.

#pagebreak()

= CONTENTS
#outline()

#pagebreak()

= LIST OF FIGURES
#figure.outline()

#pagebreak()

= LIST OF TABLES
#table.outline()

#pagebreak()

= ABBREVIATIONS

- EDA — Exploratory Data Analysis
- GNNS — Global Navigation Satellite System

#pagebreak()

// Switch to arabic numbering
#set page(numbering: "1")

// -------------------------
// MAIN CHAPTERS
// -------------------------

#chapter("Introduction")

== Motivation

Lorem ipsum...

== Project description

Lorem ipsum...

#chapter("Theory")

== Equations

$r = 2π^2$ <eq1>

See equation @eq1.

#chapter("Methods")

#chapter("Results")

#chapter("Discussion")

#chapter("Conclusions")

#pagebreak()

= REFERENCES

#bibliography("references.bib")
