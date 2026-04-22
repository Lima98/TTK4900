# TTK4900
Master Project Cybernetics and Robotics at NTNU, the WIP [thesis](thesis/latex/main.pdf) can be found in the `thesis/` directory. 

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Scripts](#scripts)

## Project Overview
This repository contains the code and documentation for the Master Project in Cybernetics and Robotics at NTNU. The project focuses on _[TBD: The project is in a very early stage and the scope of the project is yet to be defined.]_
To listen to generated audio files and view documentation you can visit my [NTNU-webpage](https://janoivil.folk.ntnu.no).

## Project Structure
The repository is organized as follows:
- `code/`: Code files. 
- `output/`: Generated audio files and other outputs from the code.
- `docs/_build`: Contains documentation generated using Sphinx.
- `research/`: Documents and notes on relevant theory and research papers.
- `thesis/`: Latex files and rendered [PDF](thesis/latex/main.pdf) of the thesis. 
- `webpage/`: Files related to the [NTNU-webpage](https://janoivil.folk.ntnu.no) where generated audio files and documentation can be accessed.
- `README.md`: This file.

## Getting Started
This project is in a too early stage to provide detailed instructions for getting started. However, you can explore the `code/`, `docs/`, `research/`, and `thesis/` directories to see the current state of the project. Future updates will include more detailed instructions and documentation as the project progresses.

## Scripts
There are a few scripts in the repository which to different things. 
- `webpage/deploy.zsh`: Builds documentation and deploys the webpage to my NTNU-webpage.
- `thesis/examples/script.py`: Uses lilypond to generate the files in a directory to thesis-ready format and places them in the latex directory for easy inclusion.
- `docs/build_docs.zsh`: Build the documentation. Is automatically run by the deploy script, but can be ran separately from here.
- `code/main.py`: Generates the current melody-engine iteration and can optionally call LilyPond and TiMidity++ directly.
- `code/melody_engine/render_outputs.py`: Optional helper for re-rendering existing `.ly` files.

## Iteration Three Workflow
From the project root you can now use the current iteration directly from the terminal:

```bash
python3 code/main.py
python3 code/main.py --pdf
python3 code/main.py --pdf --wav
python3 code/main.py --key D --mode major --seed 1337 --bars 8 --form period
python3 code/main.py --seed 1337 --with-variants
python3 code/main.py render --seed 1337 --pdf --wav
```

The generated LilyPond files are written to seed-named folders such as [code/output/1337](/Users/jan-oivindlima/Documents/arbeid/skole/10.%20semester/TTK4900%20-%20Masteroppgave/code/output/1337), and both scripts use stable paths relative to the repository so they work cleanly from `nvim` or `ghostty` as long as `lilypond` and `timidity` are available in your shell. By default only the main melody is exported; transposed variants are now opt-in with `--with-variants`. Exported filenames are descriptive, so different keys or settings can live in the same seed folder without overwriting each other.

Iteration three now supports:

- `--form auto|sentence|period|phrase` for form-aware reuse and development of melodic ideas.
- `--harmony auto` to derive a tonal progression from the thesis discussion of tonic, predominant, dominant, and return functions.
- `--voice-profile melody|soprano1|soprano2|alto1|alto2|tenor1|tenor2|bass1|bass2` so ranges and clefs stay compatible with later multi-voice work.
- `--pdf` for cropped thesis-ready PDFs and `--wav` for audio only when needed.
- `render --seed <n> --pdf --wav` to render existing `.ly` files later without regenerating the melody.
