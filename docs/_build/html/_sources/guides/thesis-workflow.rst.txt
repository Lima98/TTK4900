Thesis Workflow
===============

Why This Documentation Exists
-----------------------------

The project has two public-facing entry points:

- the command-line tool in ``code/main.py`` for generating and rendering material
- the thesis companion page in ``webpage/index.html`` for browsing numbered examples

This documentation sits between those two layers. It explains how code, generated assets,
and thesis references fit together so you can update one part of the project without losing
track of the others.

Main Asset Paths
----------------

- ``code/output/<seed>/`` stores generated LilyPond, PDF, MIDI, and WAV files
- ``thesis/latex/examples/`` stores curated example assets referenced from the thesis
- ``thesis/latex/main.pdf`` is the thesis document itself
- ``webpage/index.html`` links examples back into the thesis by page number

Typical Example Workflow
------------------------

1. Generate a melody or example asset with ``code/main.py``.
2. Render the cropped PDF and optional WAV output.
3. Copy or curate the relevant files into ``thesis/latex/examples/`` when the example becomes part of the thesis.
4. Add the numbered example to ``webpage/index.html`` so the browser archive mirrors the thesis structure.
5. Rebuild the docs if the CLI, engine structure, or workflow description changed.

Deployment Workflow
-------------------

The deploy script in ``webpage/deploy.zsh`` publishes four things together:

- the webpage itself
- the thesis PDF
- the generated documentation in ``docs/_build/html/``
- the thesis example assets

That means the archive page, thesis PDF, and technical documentation stay synchronized instead
of drifting apart.
