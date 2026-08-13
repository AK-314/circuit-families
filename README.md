# Grokking Opens a Family of Sparse Circuits

Code, data, selected checkpoints, and recorded outputs accompanying **“Grokking Opens a
Family of Sparse Circuits.”** The study evaluates sparse circuit recoverability across
grokking in five independently trained one-layer transformers performing modular addition.

This GitHub repository is the lightweight source view. The complete version 1.0.0 artifact is archived at
[https://doi.org/10.5281/zenodo.21917638](https://doi.org/10.5281/zenodo.21917638). The GitHub
repository omits the large checkpoints and detailed analysis archives; the Zenodo DOI identifies
the complete frozen release.

Recovered circuit families are outputs of the deposited component basis, intervention, and
search procedure. An empty result means procedural non-recovery under that procedure, not
mathematical absence. Multiple recovered masks do not establish algorithmic identity or causal
interchangeability, and similarity under the fixed Q1–Q4 transfer probe does not prove equivalent
internal computation.

## What can be reproduced?

The artifact supports:

- inspection of saved training trajectories and checkpoint evaluations;
- independent recalculation of the headline phase-level and seed-level results;
- regeneration of Figures 1–5 from deposited figure-source CSV files;
- verification of the 630-cell sensitivity analysis and machine-readable circuit listings;
- structural-overlap and Q1–Q4 transfer analyses;
- checkpoint-level reevaluation using 42 selected checkpoints;
- reruns of the deposited circuit searches and analyses; and
- from-scratch model retraining.

This is **rerun capability for the deposited analyses, plus from-scratch model retraining**. It
does not attempt to replay every historical development run or intermediate project state.

## Quick start

Requirements: Python 3.11 and [`uv`](https://docs.astral.sh/uv/). The locked environment is
defined by `pyproject.toml` and `uv.lock`.

```bash
uv sync --locked
uv run python reproduce.py results
uv run python reproduce.py figures
```

These commands independently recalculate the principal reported counts and seed-level statistics
under `reproduction/generated/tables/`, and regenerate Figures 1–5 under
`reproduction/generated/figures/` from the lightweight source tables.

After downloading and extracting the complete Zenodo artifact, run the full inexpensive reviewer
workflow with `uv run python reproduce.py`. That command additionally verifies the selected
checkpoints, detailed archives, and frozen records. The full artifact is required for checkpoint
reevaluation and expensive search reruns.

Individual inexpensive steps are also available:

```bash
uv run python reproduce.py verify
uv run python reproduce.py results
uv run python reproduce.py figures
```

The verifier returns a nonzero exit code if any required file, recorded hash, selected checkpoint,
archive, figure source, or frozen validation record fails inspection.

## Artifact map

| Content | Location |
|---|---|
| Machine-readable circuit listings | `results/tables/stage18_circuits.csv` |
| 630-cell sensitivity summaries | `results/tables/stage18_family_summary.csv` |
| Structural overlap records | `results/tables/stage18_pairwise_overlap.csv` |
| Q1–Q4 transfer records | `results/tables/stage18_transfer_profiles.csv` |
| Figure-source registry | `results/tables/stage21_figure_source_registry.csv` |
| Figure 1–5 source CSVs | `results/tables/stage21_figure*_source.csv` |
| Reference Figures 1–5 | `figures/stage21_figure*` |
| Selected model checkpoints | `checkpoints/` |
| Checkpoint registries and hashes | `results/tables/stage18_checkpoint_registry.csv` and `results/tables/seed_0_stage14_random_label_checkpoints.csv` |
| Checkpoint-level analysis archives | `results/archives/stage18-scaling-24a9adb84176/` |
| Execution and validation records | `manifests/` and `reproduction/records/` |
| Detailed reproduction instructions | `reproduction/REPRODUCE.md` |
| Paper availability and artifact citation text | `reproduction/PAPER_AVAILABILITY.md` |

Names containing `stageNN` are retained internal provenance identifiers. Public instructions use
scientific task names; stage identifiers are given only where needed to locate frozen files.

## Compute and storage

Verification, result recalculation, and figure regeneration require no model training or circuit
search. Verification reads roughly 10 GB of compressed analysis archives and selected
checkpoints. Extracting every checkpoint-level archive requires roughly 100 GB of free space.
Checkpoint reevaluation and circuit-search reruns are substantially more expensive and are
documented separately in `reproduction/REPRODUCE.md`.

## Repository organisation

- `configs/`: frozen task, model, training, search, transfer, and sensitivity configurations.
- `src/circuit_families/`: implementation.
- `scripts/`: experiment and analysis entry points; historical stage labels are retained here.
- `data/generated/`: deposited deterministic modular-addition dataset and metadata.
- `checkpoints/`: the 42 selected checkpoints needed for deposited analyses and controls.
- `results/tables/`: machine-readable results and figure sources.
- `results/archives/`: detailed analysis records.
- `figures/`: frozen reference figures.
- `manifests/`: provenance, hashes, execution records, and validation records.
- `reproduction/`: public verification and reproduction interface.

## Tests

```bash
uv run pytest
uv run ruff check .
```

Run the complete test suite from the extracted Zenodo artifact; some tests validate files omitted
from the lightweight GitHub view. Internal provenance names remain in some test and source filenames.

## License

Source code is available under the [MIT License](LICENSE). Except where otherwise noted, the
deposited data, checkpoints, results, tables, figures, manifests, and public reproduction
documentation are available under the [Creative Commons Attribution 4.0 International License](LICENSE-DATA).

## Citation

Please cite the archived artifact:

> Kolesnikov, A. (2026). *Grokking Opens a Family of Sparse Circuits: Code, Data, and
> Reproducibility Artifact* (Version 1.0.0) [Software and dataset]. Zenodo.
> <https://doi.org/10.5281/zenodo.21917638>

Machine-readable citation metadata are provided in [`CITATION.cff`](CITATION.cff).
