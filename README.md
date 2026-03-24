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
