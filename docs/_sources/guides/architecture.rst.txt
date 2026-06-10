Architecture
============

High-Level Design
-----------------

The project is organized around a single melody-generation pipeline:

1. launch the default configuration from ``code/main.py``
2. parse CLI settings and workflow commands in ``code/app_cli.py``
3. build a ``GenerationSettings`` object
4. generate rhythm, form targets, and harmony-aware note candidates
5. score candidates with melodic constraints
6. export LilyPond and optionally render PDF/WAV assets

Core Modules
------------

``melody_engine.structure``
  Defines the core data model such as melodies, notes, time signatures, form plans,
  harmony plans, and voice profiles.

``melody_engine.theory``
  Handles key spelling, Roman numeral interpretation, chord-tone targeting,
  and pitch conversion helpers.

``melody_engine.constraints``
  Contains the soft constraints that shape the generated melody. These include
  stepwise motion, leap recovery, climax control, form-section behavior, large-leap
  punishment, and rest usage.

``melody_engine.generator``
  Builds rhythm, motif targets, and note candidates, then performs weighted selection
  across multiple attempts to keep the best result.

``melody_engine.lilypond``
  Converts melodies to LilyPond and handles rendering to PDF, MIDI, and WAV.

``code/app_cli.py``
  Owns the reusable command-line workflow: parsing, harmony/form setup, render mode,
  and generation orchestration.

``code/main.py``
  Defines the default constraint stack and acts as the project entry point.

Current Design Priorities
-------------------------

- form-aware self-similarity
- harmonic awareness
- voice-compatible ranges
- thesis-friendly notation export
- future compatibility with multi-voice and chorale generation

Chorale Direction
-----------------

The current codebase already includes voice profiles and a ``ChoralePlan`` placeholder so the
melody engine can later be extended into SATB-style harmonization without rewriting the entire model.
