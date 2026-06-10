Procedural Music Generation
===========================

`Back to the thesis example archive <../index.html>`_

This documentation covers the current melody-generation engine, the default entry point in
``code/main.py``, the reusable CLI workflow in ``code/app_cli.py``, and the internal modules
that power form, harmony, notation, and rendering.

The guides are written to match the current repository layout, while the API reference is
generated directly from the Python modules and docstrings in ``code/main.py`` and
``code/melody_engine/``.

The goal is to make the codebase easy to navigate whether you want to:

- generate melodies or chorales,
- render cropped PDFs and WAV files,
- experiment with form, harmony, voice profiles, and clefs,
- or extend the project toward richer multi-voice generation.

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/getting-started
   guides/cli-reference
   guides/architecture

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/melody-engine
   api/main-module

.. toctree::
   :hidden:

   guides/thesis-workflow

Quick Start
-----------

Generate LilyPond only:

.. code-block:: bash

   python3 code/main.py

Generate a melody and also render cropped PDF output:

.. code-block:: bash

   python3 code/main.py --pdf

Render audio later without regenerating:

.. code-block:: bash

   python3 code/main.py render --seed 11 --wav

Useful Entry Points
-------------------

- ``code/main.py``: default project entry point and constraint configuration
- ``code/app_cli.py``: reusable CLI workflow for generation and rerendering
- ``code/melody_engine/``: reusable engine modules
- ``docs/``: documentation source
- ``webpage/index.html``: static example archive and project page

Documentation Workflow
----------------------

Build the HTML documentation locally:

.. code-block:: bash

   cd docs
   ./build_docs.zsh

The generated site is written to ``docs/_build/html/`` and is the same material deployed by
``webpage/deploy.zsh``.

Author Reference
----------------

`Open author-only workflow notes <guides/thesis-workflow.html>`_

This material covers thesis-specific example curation and deployment details that are useful
for maintaining the project, but not required for normal program usage.
