# Constraint Satisfaction Example for Procedural Generation

This folder contains a small thesis-oriented demonstration of procedural generation as a constraint satisfaction problem (CSP). The script models each grid cell as a variable, tile types as domain values, and terrain adjacency rules as binary constraints. It then applies AC-3 constraint propagation and backtracking search to generate a valid terrain map.

Run:

```bash
code/.proc-gen-examples/.venv/bin/python code/.proc-gen-examples/constraint-satisfaction/constraint_satisfaction_demo.py
```

The figures are written to `code/.proc-gen-examples/constraint-satisfaction/figures` as both `.png` and `.pdf`.

## Thesis angle

Constraint-based procedural generation separates the description of valid content from the search procedure that constructs it. Instead of hand-writing a step-by-step generator, the designer states constraints such as which terrain tiles may be adjacent, where required landmarks should appear, or which global properties the final artifact must satisfy. A solver then searches the space of possible assignments and returns content that satisfies those rules. This makes the design space explicit, inspectable, and easier to modify than many purely constructive generators, but it can also introduce computational cost when constraints conflict or when the search space becomes large.

In the included example, local constraints are expressed as allowed neighbouring terrain pairs, while a few global constraints require a settlement, a path outlet, enough water, and a connected path. The domain-propagation figure shows how constraint reasoning can reduce uncertainty before full search begins, and the final map shows one generated artifact that satisfies the declared design rules.

## Useful Sources

- Shaker, N., Togelius, J., & Nelson, M. J. (2016). *Procedural Content Generation in Games*. Springer. DOI: `10.1007/978-3-319-42716-4`, https://doi.org/10.1007/978-3-319-42716-4. The book has chapters on constraint-based and ASP-based PCG and is a good general thesis reference.
- Smith, A. M., & Mateas, M. (2011). "Answer Set Programming for Procedural Content Generation: A Design Space Approach." *IEEE Transactions on Computational Intelligence and AI in Games*, 3(3), 187-200. DOI: `10.1109/TCIAIG.2011.2158545`, https://doi.org/10.1109/TCIAIG.2011.2158545. Useful for writing about explicit design spaces and solver-based generation.
- Nelson, M. J., & Smith, A. M. (2016). "ASP with Applications to Mazes and Levels." In *Procedural Content Generation in Games*, pp. 143-157. DOI: `10.1007/978-3-319-42716-4_8`, https://doi.org/10.1007/978-3-319-42716-4_8. A directly relevant chapter for constraint/logic-based maze and level generation.
- Karth, I., & Smith, A. M. (2022). "WaveFunctionCollapse: Content Generation via Constraint Solving and Machine Learning." *IEEE Transactions on Games*, 14(3), 364-376. DOI: `10.1109/TG.2021.3076368`, https://doi.org/10.1109/TG.2021.3076368. Useful for connecting CSP-style local constraints to the well-known Wave Function Collapse family.
- Nie, Y., Zheng, S., Zhuang, Z., & Togelius, J. (2024). "Nested Wave Function Collapse Enables Large-Scale Content Generation." *IEEE Transactions on Games*. DOI: `10.1109/TG.2024.3377637`, https://doi.org/10.1109/TG.2024.3377637. A newer reference on scaling WFC-style constrained generation.
- Gumin, M. `mxgmn/WaveFunctionCollapse`, GitHub repository: https://github.com/mxgmn/WaveFunctionCollapse. The original open-source WFC implementation is useful as a practical reference, though the academic papers above are stronger for formal citation.
