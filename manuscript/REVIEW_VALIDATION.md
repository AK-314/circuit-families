# Post-review revision validation

13 September 2026. Scientific results commit `145f991`; protocol/evaluator frozen
before new evaluation at `8396674`. Earlier E1–E5 baseline: `8d138b8`.

## Completed

The exploratory follow-up audits 700 E4/E5 streams and evaluates 70 fixed masks.
No training, new search, MPS use or E1–E5 modification. The 2-mask smoke took
0.320 seconds and the 70-mask evaluation 8.537 seconds, excluding source loading
and hashing. A complete repeat reproduced the evaluation CSV byte for byte, all
masks, and every per-input array; only runtime metadata varies. Both validate-only
paths pass. Original agreement/JS values, full-mask outputs, unchanged weights
and restored hooks pass their checks.

The paper adds independently recovered families, shared-core interventions,
same-mask confidence diagnostics and descriptive longitudinal correlations.
Supplement S2 now specifies the exact reuse score, tie ordering, seed derivation,
restart acceptance and shared evaluation budgets. Related work adds Manning-Coe,
Tigges and Miller, and updates Bayat Makou to its TMLR publication.

The main paper is 12 pages including references; the supplement is 10. All 22 pages
were rendered and inspected, including the new tables and all five figures.
Final TeX builds are warning-free. Table fidelities use four decimals to avoid
rounding the seed-1 union to perfect agreement. Original uploads are untouched.

## Verification

- 47 focused follow-up/E1–E5 compatibility tests: passed.
- 48 original diversity-search, mask, fidelity and Stage 12 pipeline tests: passed.
- 6 manuscript tests: passed. Total: 101 tests.
- Ruff on the four edited/new Python files: passed.
- Builder coverage, source/output hashes and builder identity: passed.
- Both evaluation manifests and complete repeatability: passed.
- Scientific diff from `8d138b8`: 13 new follow-up files, no edited frozen files.
- Publication changes: manuscript material and a brief README update only.

## Exact verification commands

From `/Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr`:

```sh
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_phase1_review_followup.py tests/test_phase1_tmlr_result_registry.py \
  tests/test_phase1_e1_jaccard_null.py tests/test_phase1_e2_random_mask_fidelity.py \
  tests/test_phase1_e3_greedy_endpoint_trajectory.py tests/test_phase1_e4_independent_search.py \
  tests/test_phase1_e5_nonargmax_fidelity.py tests/test_nonmonotone_search.py \
  tests/test_stage22_freeze.py

MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_diversity_forced_search.py tests/test_masks.py tests/test_fidelity.py \
  tests/test_stage12_pipeline.py

.venv/bin/python scripts/run_phase1_review_followup.py --repository-root . \
  --source-root /Users/alexkolesnikov/Projects/circuit-families \
  --contract results/notes/phase1_review_followup_v1/CONTRACT.md \
  --mode audit --output-directory results/raw/phase1-review-followup-v1/audit --validate-only

.venv/bin/python scripts/run_phase1_review_followup.py --repository-root . \
  --source-root /Users/alexkolesnikov/Projects/circuit-families \
  --contract results/notes/phase1_review_followup_v1/CONTRACT.md \
  --mode evaluate --output-directory results/raw/phase1-review-followup-v1/evaluation --validate-only
```

From the ChatGPT project directory (parent of `output/`):

```sh
PHASE1_REPO=/Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr \
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl \
/Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr/.venv/bin/python -m pytest \
  -q -p no:cacheprovider output/phase1-tmlr/test_manuscript.py

MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl \
/Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr/.venv/bin/python \
  output/phase1-tmlr/build_manuscript.py \
  --repo /Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr \
  --out output/phase1-tmlr --validate-only

/Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr/.venv/bin/ruff check --no-cache \
  --config /Users/alexkolesnikov/Projects/circuit-families-phase1-tmlr/pyproject.toml \
  output/phase1-review-followup/run_phase1_review_followup.py \
  output/phase1-review-followup/test_phase1_review_followup.py \
  output/phase1-tmlr/build_manuscript.py output/phase1-tmlr/test_manuscript.py
```

From `output/phase1-tmlr`:

```sh
/opt/homebrew/bin/tectonic -X compile main.tex --keep-logs
/opt/homebrew/bin/tectonic -X compile supplement.tex --keep-logs
pdftoppm -scale-to 1300 -png main.pdf /private/tmp/phase1-review-main
pdftoppm -scale-to 1300 -png supplement.pdf /private/tmp/phase1-review-supplement
```

## Publication status

These remain named author-review PDFs. Author sign-off, anonymous review packaging
and actual journal submission remain. The new GitHub prerelease preserves earlier
releases and includes asset hashes. Zenodo timed out again on September 13; no
new DOI or archival success is claimed. The original DOI remains unchanged.
Compressed search proposal traces are not duplicated in the lightweight release;
their endpoints and masks are included. No acceptance probability is inferred.
