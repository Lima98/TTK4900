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
  // bibliography: bibliography("thesis.bib"),
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

== Background

When writing computer programs we are often tasked with creating a system that is hierarchical, meaning that we have a way to write code that is very top down and easily digestible. The structure will resemble a tree in many ways, with the main functionality being the bulk of the program and the small individual functions will be like the leaves of the tree. This is a tried and true way to develop software, however for certain problems this way of structuring the program falls apart.

In this instance we are trying to create software that should compose music that is coherent, and makes sense with the conventions of melodic structure as well as rhythmic figures. In order to do this we need the program to refer back to itself. We cannot simply construct a rhythm and then construct a melodic phrase and expect them to work together. They need to be intrinsically linked in a way that makes them both affect each other. In addition we need to have the musical ideas repeat themselves. Self-similarity is a very important concept when it comes to constructing good music. Without repetition the listener will perceive the music as random and completely incoherent.
// WARN: The claims here and not backed up by any research, need to add sources to this.

== Motivation
As a musician the problem of composing and arranging music can sometimes be seen as a somewhat rule-driven process. There are always many approaches and ways to go about choosing which note to put where, but we are often guided by theory and conventions. This is a fascinating problem to try to solve with a computer program, because it is not a problem that has a clear solution. There are many different ways to approach the problem, and there is no one right way to do it.

In addition to being an interesting problem it can also become a useful tool for teaching. Such a program could generate examples or exercises for students to work with, and it could also be used to demonstrate certain concepts in music theory. It could also be used as a tool for composers to generate ideas or to help them with the compositional process.

When arranging music there are as mentioned several rules and conventions that we often follow. This means that we could create a model of the choices that need to be made, meaning that we could create a Constraint Satisfaction Problem (CSP) that could be solved with a backtracking algorithm, or we could go about it by creating a meta-model of the musical structure which models the system in several hierarchical structures from the high-level structure of the musical form and harmonic progression down to the lowest level of placing the individual notes. 



= Theory

== Music theory
In order to fully appreciate the problem of procedural music generation we need to have a basic understanding of music theory. This is not a comprehensive overview of music theory, but rather a brief introduction to the concepts that are relevant to the problem at hand.

 

=== Musical notation

=== Scales and modes

=== Rhythm and meter

=== Harmony and voice leading

=== Musical form

== Procedural generation
