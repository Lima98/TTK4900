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

Before copying files, the deploy script rebuilds the thesis PDF, regenerates the archive page
from the LaTeX ``example`` environments and ``main.aux`` labels, and rebuilds the documentation.
That means newly added thesis examples are picked up by the webpage during deployment instead of
being maintained by hand.

GitHub Pages Deployment
-----------------------

The GitHub Pages deployment script in ``webpage/deploy_github_pages.zsh`` builds the same archive
and documentation, copies the static files into a separate ``gh-pages`` worktree, commits them,
and pushes the branch to GitHub.

Run it from the repository root:

.. code-block:: bash

   ./webpage/deploy_github_pages.zsh

You can also provide the commit message directly:

.. code-block:: bash

   ./webpage/deploy_github_pages.zsh "Deploy updated thesis examples"

The first time this is used, GitHub Pages still needs to be enabled once in the repository
settings with the source set to the ``gh-pages`` branch root.
