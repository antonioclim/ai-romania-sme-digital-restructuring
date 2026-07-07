# Figure generation and visual quality

The manuscript-facing figures are reproducible from code rather than manually edited image files.

Run:

```bash
python scripts/06_generate_figures.py
```

The command writes:

- `outputs/figures_editorial/` — high-resolution PNG files intended for manuscript embedding;
- `outputs/figures/` — compatibility PNG copies;
- `outputs/figure_source_data/` — per-figure source-data CSV files;
- `outputs/FIGURE_MANIFEST.csv` — figure provenance, input files, output files and SHA-256 checksums;
- `outputs/FIGURE_VISUAL_QA.csv` — basic image-resolution and edge-clipping checks.

Design rules:

- no titles inside image panels; titles belong in captions;
- grayscale-compatible bars;
- wrapped labels and expanded left margins;
- value labels placed inside the plotting region;
- confidence-interval labels offset away from whiskers;
- optional conceptual arrows terminate at box boundaries and do not cross unrelated boxes.
