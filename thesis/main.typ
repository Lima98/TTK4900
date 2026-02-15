//#import "lib.typ": *
#import "@preview/nifty-ntnu-thesis:0.1.3": *
#let chapters-on-odd = false
#show: nifty-ntnu-thesis.with(
  title: [Procedural generation of music],
  short-title: [],
  authors: ("Jan-Øivind Lima",),
  short-author: ("Lima"),
  titlepage: false,
  chapters-on-odd: chapters-on-odd,
  bibliography: bibliography("thesis.bib"),
  figure-index: (enabled: true, title: "Figures"),
  table-index: (enabled: true, title: "Tables"),
  listing-index: (enabled: true, title: "Code listings"),
  abstract-en: [
  ],
  abstract-no: [
  ],
)

= Introduction
<introduction>

This thesis will cover the work of developing an algorithm and software for generating music that adheres to certain musical rules and concepts. 

= Theory

== Music theory

== Procedural generation
#figure(image("../code/output/random.cropped.png", width: 50%))
