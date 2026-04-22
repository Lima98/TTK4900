Procedural Music Generation
===========================

This documentation covers the current melody-generation engine, the command-line workflow in
``code/main.py``, and the internal modules that power form, harmony, notation, and rendering.

The guides are written to match the current repository layout, while the API reference is
generated directly from the Python modules and docstrings in ``code/main.py`` and
``code/melody_engine/``.

The goal is to make the codebase easy to navigate whether you want to:

- generate a melody for thesis examples,
- render cropped PDFs and WAV files,
- experiment with voice profiles and clefs,
- or extend the project toward multi-voice and chorale generation.

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/getting-started
   guides/cli-reference
   guides/architecture
   guides/thesis-workflow

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/melody-engine
   api/main-module

Quick Start
-----------

Generate LilyPond only:

.. code-block:: bash

   python3 code/main.py

Generate a melody and also render thesis-ready PDF output:

.. code-block:: bash

   python3 code/main.py --pdf

Render audio later without regenerating:

.. code-block:: bash

   python3 code/main.py render --seed 11 --wav

Useful Entry Points
-------------------

- ``code/main.py``: primary CLI for generation and rerendering
- ``code/melody_engine/``: reusable engine modules
- ``webpage/index.html``: thesis example archive for examiners
- ``thesis/latex/main.pdf``: thesis document referenced by the webpage and examples

Documentation Workflow
----------------------

Build the HTML documentation locally:

.. code-block:: bash

   cd docs
   ./build_docs.zsh

The generated site is written to ``docs/_build/html/`` and is the same material deployed by
``webpage/deploy.zsh``.
