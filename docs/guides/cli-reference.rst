CLI Reference
=============

Generation Command
------------------

The main command is:

.. code-block:: bash

   python3 code/main.py [options]

Core Options
------------

- ``--key``: tonic note, for example ``C`` or ``Eb``
- ``--mode``: scale mode such as ``major`` or ``minor``
- ``--tonic-octave``: base octave used for pitch spelling
- ``--bars``: number of bars to generate
- ``--form``: one of ``auto``, ``sentence``, ``period``, or ``phrase``
- ``--voice-profile``: voice range preset such as ``melody`` or ``tenor1``
- ``--clef``: one of ``auto``, ``treble``, ``treble_8``, or ``bass``
- ``--harmony``: explicit harmonic plan or ``auto``
- ``--seed``: random seed for reproducible generation

Rendering Options
-----------------

- ``--pdf`` renders cropped PDF output
- ``--wav`` renders WAV output through TiMidity++
- ``--with-variants`` also exports the transposed derivative examples

Examples
--------

.. code-block:: bash

   python3 code/main.py --pdf
   python3 code/main.py --voice-profile tenor1 --tonic-octave 3 --pdf
   python3 code/main.py --key Eb --bars 16 --allowed-durations 0.25,0.5,1.0,2.0 --pdf --wav

Render Mode
-----------

You can rerender existing LilyPond files without regenerating the melody:

.. code-block:: bash

   python3 code/main.py render --seed 11 --pdf
   python3 code/main.py render --seed 11 --pdf --wav
   python3 code/main.py render code/output/11/custom_file.ly --pdf

Manual Harmony Format
---------------------

Explicit harmonic plans can use one of three formats:

Compact beat format:

.. code-block:: text

   2I,2V,4I,2IV,2iv

Here the number is the duration in beats and the Roman numeral is the chord.

Alternating chord-and-dash format:

.. code-block:: text

   I -- V -- vi ----

Range format:

.. code-block:: text

   start-end:roman[:weight]

Example:

.. code-block:: bash

   python3 code/main.py --harmony "2I,2V,4I,2IV,2iv"

If the explicit harmony is longer than the generated piece, it is truncated. If it is shorter,
the remaining bars are filled automatically using the default tonal progression.
