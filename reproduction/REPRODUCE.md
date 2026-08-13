# Reproducing the reported analyses

This guide follows four levels of increasing cost:

1. **Inspect** saved machine-readable outputs.
2. **Verify** the integrity and provenance of the deposit.
3. **Recalculate** headline results and regenerate figures from deposited records.
4. **Reevaluate or rerun** models, masks, searches, and training when required.

The inexpensive path is designed for a reviewer. The expensive paths are included for deeper
audits, not required for checking the reported summaries.

## 1. Installation

Install Python 3.11 and `uv`, then run from the artifact root:

```bash
uv sync --locked
```

The exact resolved Python dependencies are recorded in `uv.lock`. The original computations used
CPU and Apple MPS environments as recorded in the manifests. The deposited multi-seed search is a
CPU workflow; CUDA is supported only by scripts that explicitly expose a CUDA device option.

## 2. Inspect saved outputs

The principal machine-readable records are:

- `results/tables/stage18_circuits.csv`: recovered circuit membership and mask identifiers;
- `results/tables/stage18_family_summary.csv`: all 630 sensitivity cells;
- `results/tables/stage18_pairwise_overlap.csv`: structural comparisons;
- `results/tables/stage18_transfer_profiles.csv`: Q1–Q4 transfer profiles;
- `results/tables/stage20_seed_level_summaries.csv`: seed-level descriptive inference;
- `results/tables/stage21_figure_source_registry.csv`: panel-to-source mapping; and
- `results/tables/stage21_figure1_*_source.csv` through
  `stage21_figure5_*_source.csv`: plotted values.

Internal stage numbers in these frozen filenames are provenance labels. They are not steps a
reviewer must discover or run in numerical order.

## 3. Verify the deposit

```bash
uv run python reproduce.py verify
```

The verifier checks:

- required public files;
- frozen scientific-file hashes recorded by the final analysis-freeze manifest;
- the deterministic dataset and metadata;
- all 42 selected checkpoints and their recorded hashes;
- the primary-seed, sensitivity, and 35 checkpoint-level multi-seed archives;
- the independent multi-seed reproduction record and its deposited comparison log; and
- the five figure-source tables and source registry.

This verifies **the provenance of the frozen analysis snapshot and its recorded source commit**.
It deliberately does not require `git HEAD` to equal the pre-publication snapshot: documentation,
inventories, and public reproduction scripts were added afterward, and an archive downloaded from
a repository may not include `.git` at all.

Success ends with:

```text
ARTIFACT VERIFICATION: PASS
```

Any failed check produces a nonzero exit code.

## 4. Independently recalculate reported results

```bash
uv run python reproduce.py results
```

This command reads the 630 lower-level family records and per-seed behavioural landmarks. It
recalculates the number of recovered cells by behavioural phase and the five primary pre-to-post
changes, median, mean, and exact two-sided sign-test probability. It does not read a hand-written
manuscript summary table. It writes `phase_recovery_summary.csv` and
`primary_seed_changes.csv` under `reproduction/generated/tables/`.

Expected output includes:

```text
delayed        0 / 162
transition    30 / 198
stable-post  270 / 270

Primary seed changes: +6, +7, +7, 0, +7
Median change: +7
Mean change: +5.4
Exact two-sided sign test: p = 0.125
```

Zeros are reported but excluded from the exact sign test, matching the frozen analysis rule.

## 5. Regenerate Figures 1–5

```bash
uv run python reproduce.py figures
```

The command first checks the frozen SHA-256 value of each figure-source CSV, then regenerates ten
files—PNG and PDF for each figure—under `reproduction/generated/figures/`. It reads those source
CSVs directly; it neither copies the frozen figures nor reruns training or circuit search.

Validation is based on the source data and plotting completion, not byte-identical PDF files.
PDF metadata, font embedding, and rendering details can differ across platforms without changing
the plotted scientific values.

## 6. Checkpoint-level reevaluation

The deposit contains 35 selected genuine-task checkpoints and seven random-label control
checkpoints. Their paths and hashes are recorded in:

- `results/tables/stage18_checkpoint_registry.csv` (multi-seed genuine task; internal Stage 18);
- `results/tables/seed_0_stage14_random_label_checkpoints.csv` (random-label control; internal
  Stage 14).

Detailed masks and evaluation records are stored in the checkpoint-level archives under
`results/archives/stage18-scaling-24a9adb84176/`. Extract only the seed/checkpoint archive being
audited into a separate temporary directory; extracting all 35 archives requires roughly 100 GB.
The low-level reevaluation interface is:

```bash
uv run python scripts/evaluate_mask.py --help
```

It accepts a selected checkpoint manifest, checkpoint step, and a saved mask JSON. Write new
outputs outside the frozen `results/` tree.

## 7. Rerun deposited circuit analyses

The frozen analysis entry points remain under `scripts/`. Descriptive task names are listed first
below; internal stage identifiers are included only to locate the implementation:

- primary-seed sparse-family search: `scripts/run_stage12_diversity.py`;
- Q1–Q4 transfer analysis: `scripts/run_stage16_transfer.py`;
- fidelity-by-distinctness sensitivity analysis: `scripts/run_stage17_sensitivity.py`;
- five-seed, 630-cell analysis: `scripts/run_stage18_scaling.py`;
- matched comparisons and seed-level inference: `scripts/run_stage19_matched_comparisons.py` and
  `scripts/run_stage20_paired_inference.py`.

Inspect the exact interface with `--help` before an expensive run. These frozen production scripts
contain strict source-state checks used during the original analysis. For an exact search rerun,
use a Git checkout of the implementation commit recorded by the corresponding manifest, place the
deposited dataset and selected checkpoints at their recorded relative paths, and write output to a
separate reproduction directory. Do not overwrite the deposited reference outputs.

The complete multi-seed search is expensive: it covers 630 cells with fixed exact-evaluation
budgets. The deposit therefore supports the rerun but does not make it part of the inexpensive
reviewer command.

## 8. Retrain models from scratch

The deterministic dataset generator writes to paths fixed by `configs/task.yaml`. Run it only in
a disposable copy of the artifact so the deposited reference files remain unchanged:

```bash
uv run python scripts/generate_dataset.py --config configs/task.yaml
```

Then compare the regenerated archive and metadata hashes with the dataset manifest. The public
verifier performs the reference-side hash check.

Train a genuine-task model with:

```bash
uv run python scripts/train.py --seed 0 --device cpu --output-root reproduction/generated/training
```

Use seeds 0–4 for the five genuine-task models. This regenerates training trajectories and the
full checkpoint series; only the 42 selected analysis/control checkpoints are deposited. Training
is deterministic subject to the platform and framework limitations recorded in the manifests.

## Interpretation limits

The artifact reproduces results under the specified component basis, intervention, thresholds,
and search budget. Empty recovered families are procedural non-recovery. Structural diversity
does not establish distinct algorithms, and lack of separation under Q1–Q4 does not establish
mechanistic equivalence.
