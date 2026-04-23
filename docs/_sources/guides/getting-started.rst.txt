Getting Started
===============

Repository Structure
--------------------

- ``code/main.py`` is the main user-facing entry point.
- ``code/melody_engine/`` contains the reusable engine modules.
- ``code/output/<seed>/`` stores generated LilyPond, PDF, MIDI, and WAV files.
- ``thesis/latex/examples/`` stores thesis example assets used by the webpage.
- ``webpage/index.html`` presents the thesis examples with matching numbering.

Typical Workflow
----------------

Generate notation only:

.. code-block:: bash

   python3 code/main.py --key Eb --tonic-octave 3 --bars 16

Generate notation and cropped PDF:

.. code-block:: bash

   python3 code/main.py --key Eb --tonic-octave 3 --bars 16 --pdf

Generate notation, PDF, and WAV:

.. code-block:: bash

   python3 code/main.py --key Eb --tonic-octave 3 --bars 16 --pdf --wav

If you forget rendering flags, rerender later:

.. code-block:: bash

   python3 code/main.py render --seed 11 --pdf
   python3 code/main.py render --seed 11 --pdf --wav

Naming And Output
-----------------

Files are written into a seed folder such as ``code/output/11/``.

The filename stem is descriptive by default, so different keys or settings can coexist inside
the same seed folder without overwriting each other. For example:

.. code-block:: text

   eb_major_o3_16bars_melody_auto_dur025-05-10-20.ly

Voice Profiles And Clefs
------------------------

The engine supports ``melody`` plus sub-group voice profiles:

- ``soprano1``, ``soprano2``
- ``alto1``, ``alto2``
- ``tenor1``, ``tenor2``
- ``bass1``, ``bass2``

Clef choice is automatic by default, but you can override it with ``--clef treble``,
``--clef treble_8``, or ``--clef bass``.
