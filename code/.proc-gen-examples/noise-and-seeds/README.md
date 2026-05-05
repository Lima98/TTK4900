# Noise and Seed Example for Procedural Generation

This folder contains a small illustrative example of seed-based random noise for procedural generation. The script uses deterministic pseudo-random value noise, layers several octaves into fractal Brownian motion (fBm), and then transforms the continuous height map into discrete terrain classes.

Run:

```bash
code/.proc-gen-examples/.venv/bin/python code/.proc-gen-examples/noise-and-seeds/noise_seed_demo.py
```

The figures are written to `code/.proc-gen-examples/noise-and-seeds/figures` as both `.png` and `.pdf`.

## Thesis angle

Noise-based procedural generation is useful when the desired content should look organic, continuous, or naturally varied. A random seed initializes a pseudo-random number generator, which means that the same seed and parameters produce the same artifact every time. This gives the designer a compact identifier for a generated world while still allowing many possible outputs.

The method is constructive: it does not search for a solution. Instead, it generates a continuous field of values and interprets that field as height, density, moisture, temperature, or some other latent property. Layering multiple noise frequencies creates large-scale structure and small-scale detail. Thresholding then turns the continuous field into discrete content such as water, beaches, grassland, forest, mountains, and snow.

The included figures show:

- `01_seed_variation`: the same algorithm and parameters with different seeds.
- `02_noise_octaves`: how multiple octaves add detail at different scales.
- `03_noise_to_terrain`: a pipeline from noise to height map to terrain classes.
- `04_parameter_control`: how parameters affect the character of the output while keeping the same seed.

## Useful sources

- Shaker, N., Togelius, J., & Nelson, M. J. (2016). *Procedural Content Generation in Games*. Springer. DOI: `10.1007/978-3-319-42716-4`, https://doi.org/10.1007/978-3-319-42716-4. Useful as a general PCG reference.
- Shaker, N., Togelius, J., & Nelson, M. J. (2016). "Fractals, noise and agents with applications to landscapes." In *Procedural Content Generation in Games*, pp. 57-72. DOI: `10.1007/978-3-319-42716-4_4`, https://doi.org/10.1007/978-3-319-42716-4_4. The most directly relevant chapter for noise-based terrain generation.
- Perlin, K. (1985). "An Image Synthesizer." *ACM SIGGRAPH Computer Graphics*, 19(3), 287-296. DOI: `10.1145/325165.325247`, https://doi.org/10.1145/325165.325247. Classic paper introducing gradient noise for procedural textures.
- Gustavson, S. (2005). "Simplex noise demystified." Technical report. Useful for understanding simplex noise as a later alternative to classic Perlin noise.
