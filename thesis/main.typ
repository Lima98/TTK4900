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

When writing computer programs we are often tasked with creating a system that is hierarchical, meaning that we have a way to write code that is very top down and easily digestible. The structure will resemble a tree in many ways, with the main functionality being the bulk of the program and the small individual functions will be like the leaves of the tree. This is a tried and true way to develop software, however for certain problems this way of structuring the program falls apart.

In this instance we are trying to create software that should compose music that is coherent, and makes sense with the conventions of melodic structure as well as rhythmic figures. In order to do this we need the program to refer back to itself. We cannot simply construct a rhythm and then construct a melodic phrase and expect them to work together. They need to be intrinsically linked in a way that makes them both affect each other. In addition we need to have the musical ideas repeat themselves. Self-similarity is a very important concept when it comes to constructing good music. Without repetition the listener will perceive the music as random and completely incoherent.
// WARN: The claims here and not backed up by any research, need to add sources to this.
== Motivation
With this in mind we need to re-think how we go about structuring such a program, without changing the way we build a program we will be unable to create something meaningful

= Theory

== Music theory

== Procedural generation
#figure(image("../code/output/random.cropped.png", width: 50%))
