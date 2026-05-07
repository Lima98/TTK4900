# Wave Function Collapse Example for Procedural Generation

This folder contains a small illustrative tiled-model Wave Function Collapse (WFC) example. The script uses a hand-made exemplar tile map, learns which tile types may appear next to each other, and then generates new maps that preserve those local adjacency rules.

Run:

```bash
code/.proc-gen-examples/.venv/bin/python code/.proc-gen-examples/wave-function-collapse/wfc_demo.py
```

The figures are written to `code/.proc-gen-examples/wave-function-collapse/figures` as both `.png` and `.pdf`.

## Thesis angle

Wave Function Collapse is a procedural generation method that combines example-driven learning with constraint propagation. The designer provides a small exemplar. The algorithm extracts local patterns or adjacency rules from that exemplar, then generates new content by maintaining a domain of possible tiles for every output cell.

Generation alternates between observation and propagation. Observation chooses a cell with low entropy, meaning a cell with few remaining possibilities, and collapses it to one tile. Propagation then removes incompatible possibilities from neighbouring cells. Repeating this process produces an output that is new, but still locally consistent with the exemplar.

This makes WFC useful as a bridge between the other examples:

- Like noise-based generation, WFC can produce variation from a seed.
- Like constraint satisfaction, WFC maintains domains and propagates constraints.
- Like constructive methods, it incrementally builds a concrete artifact.
- Unlike pure hand-authored rules, it can learn many of its local constraints from an example.

The included figures show:

- `01_exemplar_and_rules`: a small exemplar and the local tile adjacencies learned from it.
- `02_observe_propagate_steps`: cell domains shrinking through observation and propagation.
- `03_generated_wfc_map`: one generated output satisfying the learned local rules.
- `04_seed_variations`: different outputs from the same learned rules and different seeds.

## Useful sources

- Karth, I., & Smith, A. M. (2022). "WaveFunctionCollapse: Content Generation via Constraint Solving and Machine Learning." *IEEE Transactions on Games*, 14(3), 364-376. DOI: `10.1109/TG.2021.3076368`, https://doi.org/10.1109/TG.2021.3076368. A strong academic source for explaining WFC as a family of algorithms.
- Gumin, M. `mxgmn/WaveFunctionCollapse`, GitHub repository: https://github.com/mxgmn/WaveFunctionCollapse. The original reference implementation and practical source for tiled and overlapping WFC.
- Shaker, N., Togelius, J., & Nelson, M. J. (2016). *Procedural Content Generation in Games*. Springer. DOI: `10.1007/978-3-319-42716-4`, https://doi.org/10.1007/978-3-319-42716-4. Useful as a general PCG framing source.
