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


// ----------------------
// TITLE PAGE
// ----------------------

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
  #align(center)[
    #v(2cm)
    #text(size: 20pt, weight: "bold")[#title]
    #v(0.5cm)
    #subtitle
    #v(1.5cm)

    Master’s thesis in #program  
    Supervisor: #supervisor  
    Co-supervisor: #cosupervisor  

    #v(1cm)
    #date

    #v(2cm)
    Norwegian University of Science and Technology  
    #faculty  
    #department
  ]
  #pagebreak()
]


// ----------------------
// CHAPTER STYLE
// ----------------------

#show heading.where(level: 1): it => [
  #pagebreak()
  #align(center)[
    #text(size: 14pt, weight: "bold")[CHAPTER]
    #v(0.5cm)
    #text(size: 14pt, weight: "bold")[#upper(it.numbering())]
    #v(0.5cm)
    #text(size: 18pt, weight: "bold")[#upper(it.body)]
  ]
  #v(1cm)
]


// ----------------------
// FRONT MATTER
// ----------------------

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

#heading(level: 1)[Abstract]
Write abstract here.

#pagebreak()

#heading(level: 1)[Preface]
Write preface here.

#pagebreak()

#heading(level: 1)[Contents]
#outline()

#pagebreak()


// Switch to Arabic numbering for main matter
#set page(numbering: "1")


// ----------------------
// MAIN CHAPTERS
// ----------------------

= Introduction

== Motivation

=== Stakeholders


= Theory

== Equations

