# Thesis Workflow Notes

This file contains author-oriented notes for building the thesis, rendering thesis examples, and updating the example archive webpage.

## Build the thesis

From `thesis/latex/`:

```bash
latexmk -pdf main.tex
```

The build regenerates the appendix PDF snapshot of the repository `README.md` automatically through `thesis/latex/latexmkrc`, so the appendix stays in sync with the real project README.

If the build state gets messy, remove stale generated files and rebuild in the usual LaTeX order.

## Render thesis example files

The LilyPond examples used in the thesis live in `thesis/examples/`. To render a folder or a specific example:

```bash
python3 thesis/examples/script.py 04theory
python3 thesis/examples/script.py 04theory 11-diatonic_chords
python3 thesis/examples/script.py iter3
```

Rendered files are placed in `thesis/latex/examples/`.

## Build the documentation

From the repository root:

```bash
make -C docs html
```

or use the helper script if your environment is set up for it:

```bash
./docs/build_docs.zsh
```

## Rebuild the example archive webpage

From the repository root:

```bash
python3 webpage/build_archive.py
```

This regenerates `webpage/index.html` from the thesis examples and their metadata.

## Deploy notes

The repository also contains deployment helpers for the documentation and webpage:

- `docs/build_docs.zsh`
- `webpage/deploy.zsh`

These are workflow conveniences for maintaining the thesis and archive, not part of the public program interface.
