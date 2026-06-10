## 0.16.0 (2026-06-10)

### Feat

- **thesis**: updated music theory section while re-writing
- **iter3-and-thesis**: updated iter3 to have a smaller main file and separate cli file and thesis changes up to subsection 2.2.2
- **thesis**: updated theory section, moved figures and added content to the conclusion
- **thesis-figure**: figure update to not have overlapping text
- **thesis**: updated example captions to look better in list of examples while still having the link in the actual thesis
- **thesis**: updated sections tried to fix contencts numbering being off
- **thesis**: added new figures in the third iteration, updated harmonic dictation for the CLI
- **thesis**: filled out the missing setions all sections have text proofreading is up next
- **thesis-figure**: updated bad figure and changed some text
- **thesis**: lots of added text to the thesis and some figures too
- **thesis**: new examples and figure updates for cleaner look and representation
- **thesis-background**: updated a lot in the background section and converted some figures to examples
- **thesis**: updated lots of figures, increased text size to make sure legends are readable also deleted sandbox folder in the code section

### Fix

- **thesis-figure-and-music-theory**: changed some figures and updated music theory section also renamed some examples to avoid deletion when runing example generator script
- **updated-brokes-files**: abbreviations file was deleted due to swapfile error, remade it and thesis now compiles correctly

## 0.15.0 (2026-05-10)

### Feat

- **thesis**: updated introduction and new example in the proc-gen section
- **thesis**: new figures and illustrations for the procedural generation part, also started finishing up the introduction
- **thesis**: updated discussion with some comparisons between the iterations
- **thesis**: new figures and updated sections

### Fix

- **thesis-figures**: more updates on figures
- **thesis**: lots of figure cleanup in the proc-gen section

## 0.14.0 (2026-05-05)

### Feat

- **thesis-chorale-module**: lots of new figues in thesis and code now can generate chorale

### Fix

- **thesis**: updated conclusion and theory chapter with examples of constraint based procedural generation
- **thesis-and-plan**: updated thesis and added ganttchart for the plan for finishing the procjet

## 0.13.0 (2026-04-22)

### BREAKING CHANGE

- complete refactor, iteration three is incompatible, but inspired by the first two iterations.

### Feat

- **webpage-and-documentation**: updates to webpage and documentation with a new script for pushing code to my folk webpage at ntnu
- **third-iteration-improvements**: lots of new features, clef selection, voice types etc
- **iteration-3**: lots of features for the third iteration implemented

### Fix

- **pdf**: re-ran PDF file
- **aux-files**: remved aux files to push to main

## 0.12.0 (2026-04-21)

### Feat

- **updated-iter2**: few changes to iter2 to make it easier to discuss

### Fix

- **thesis**: updated section about second iteration and procedural generation.
- **thesis-updates**: written more in thesis
- **small-changes**: tiny changes to a few files, moved proc-gen folder
- **thesis**: updated theory part regarding pcg
- **thesis**: added text and figures to random-walk section of the thesis
- **aux-files**: removed loe file
- **aux-files**: removed aux files and updated gitignore
- **thesis**: updates thesis text
- **thesis**: updated theory and figures
- **thesis**: added figures to music theory section

## 0.11.0 (2026-04-06)

### BREAKING CHANGE

- All files form 2nd iteration removed, starting with a fresh 3rd iteration

### Fix

- **second-iteration**: fixed generation and outputfiles

### Refactor

- **all-code-files**: finished 2nd iteration =

## 0.10.5 (2026-04-05)

### Fix

- **generator-and-output**: now generates full measures every time
- **bar-generator**: fixed bar generator not filling the bar
- **thesis-iter2**: new figure for thesis WIP on iteration 2
- **melody-generator**: generated melody now in correct key and uses motifs correctly and ends on tonic

## 0.10.4 (2026-03-29)

### Fix

- **updated-second-iteration**: promitive phrase generator working

## 0.10.3 (2026-03-27)

### Fix

- **thesis**: written more on thesis and converted figures to examples

## 0.10.2 (2026-03-27)

### Fix

- updated thesis
- **thesis:-first-iteration**: written draft of first iteration

## 0.10.1 (2026-03-26)

### Fix

- **update-latex-files**: written more on the thesis, added figures and changed structure
- cleanup of outdated files and updated readme
- deleted aux files
- aux files problem fixing
- remove aux files
- updated gitignore to fix issues with commiting while latex is running. All auxillary files are now ignored
- **updated-second-iteration**: trying to get a grasp of how to create these models

### Refactor

- wip changes

## 0.10.0 (2026-03-19)

### Feat

- **started-2nd-iteration**: 2nd iteration underway, better structures

## 0.9.1 (2026-03-18)

### Fix

- experiments with WFC in generation

### Refactor

- **moved-files-for-2nd-iteration**: moved files

## 0.9.0 (2026-03-09)

### Feat

- **all-files**: started refactor, got some working generation, no output files yet

## 0.8.0 (2026-03-09)

### BREAKING CHANGE

- Everything is begin re-written, nothing work as of right now

### Refactor

- **all-files**: moved old code to another folder to restart

## 0.7.0 (2026-03-02)

### Feat

- **scripts**: new scripts to put examples in latex folders for easy inclusion in the thesis

## 0.6.0 (2026-02-27)

### Feat

- WIP on phrase generator

### Fix

- **most-files**: broken shit while trying to make melody generator

## 0.5.1 (2026-02-25)

### Refactor

- cleaned up a bit in main

## 0.5.0 (2026-02-24)

### BREAKING CHANGE

- No code is compatible with earlier versions...

### Feat

- **entire-project-refactor**: all code rewritten to use objects to make manipulation easier

## 0.4.1 (2026-02-24)

### Refactor

- **sandbox/**: added sandbox/ folder to experiment with using objects for representing melodies etc

## 0.4.0 (2026-02-24)

### Feat

- updated webpage to look more complete and easy to use

## 0.3.3 (2026-02-24)

### Fix

- Fix conflict for main push

### Refactor

- Updated thesis and some code

## 0.3.2 (2026-02-23)

### Refactor

- ran new files to fix merge conflicts

## 0.3.1 (2026-02-20)

### Fix

- Re-added rhythm capability with more voices

## 0.3.0 (2026-02-20)

### BREAKING CHANGE

- Usage of the lilyconvert module is completely rewritten, will not be able to handle input from older versions

### Feat

- Lilypond module rewritten

## 0.2.0 (2026-02-20)

### Feat

- Code supports multiple voices

## 0.1.0 (2026-02-20)

### Feat

- **Rewritten-music-module**: Music module now handles all keys

### Refactor

- **EOD-18.02**: Updated code, thesis and started documentation
- **WIP-from-18.02**: Updated some code, added more intuitive rhythm generation
