# Binary Space Partitioning Example for Procedural Generation

This folder contains a small illustrative example of binary space partitioning (BSP) as a procedural generation method. BSP recursively splits a rectangular space into two smaller regions, producing a hierarchy of partitions. In game-like level generation, each final partition can host a room, and the split hierarchy can be reused to connect rooms with corridors.

Run:

```bash
code/.proc-gen-examples/.venv/bin/python code/.proc-gen-examples/binary-space-partitioning/bsp_demo.py
```

The figures are written to `code/.proc-gen-examples/binary-space-partitioning/figures` as both `.png` and `.pdf`.

## Thesis angle

Binary space partitioning is a constructive procedural generation technique: the algorithm directly builds content by applying a sequence of spatial rules. In contrast to constraint satisfaction, which searches for assignments that satisfy declared conditions, BSP progressively subdivides a design space and then fills the resulting regions.

For a thesis explanation, BSP is useful because it demonstrates how simple recursive rules can impose large-scale structure. The initial rectangle represents the available design space. Each split creates two subspaces, and repeated splitting produces a tree-shaped hierarchy. The final leaves of the tree can then be interpreted as rooms, areas, or zones. Because the hierarchy records which regions were separated by each split, it also provides a natural way to create connectivity: sibling regions can be connected with corridors.

The included figures show:

- `01_bsp_partitions`: the recursive spatial subdivision.
- `02_rooms_and_corridors`: rooms placed inside leaf partitions and connected through the BSP hierarchy.
- `03_final_bsp_dungeon`: the rasterized artifact that could be used as a simple dungeon or level layout.

## Useful sources

- Shaker, N., Togelius, J., & Nelson, M. J. (2016). *Procedural Content Generation in Games*. Springer. DOI: `10.1007/978-3-319-42716-4`, https://doi.org/10.1007/978-3-319-42716-4. Useful as a general PCG reference.
- Shaker, N., Liapis, A., Togelius, J., Lopes, R., & Bidarra, R. (2016). "Constructive Generation Methods for Dungeons and Levels." In *Procedural Content Generation in Games*, pp. 31-55. DOI: `10.1007/978-3-319-42716-4_3`, https://doi.org/10.1007/978-3-319-42716-4_3. Useful for positioning BSP as a constructive dungeon or level generation method.
- RogueBasin. "Basic BSP Dungeon generation", https://www.roguebasin.com/index.php/Basic_BSP_Dungeon_generation. A practical explanation of BSP dungeon generation used in roguelike development.
