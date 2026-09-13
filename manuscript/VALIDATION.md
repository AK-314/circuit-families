# Revision validation

Date: 13 September 2026. Scientific source commit: `8d138b8`.

## Scope

Only manuscript prose, presentation, derived displays and publication packaging changed.
No frozen scientific file or configuration was edited. No model was trained or evaluated.
The uploaded August manuscripts and LaTeX archive remain unchanged.

## Checks performed

- Coverage and numerical assertions: 630 family cells, 78 E1 pairs, 4,200 E2 masks,
  210 E3 endpoints, 350 E4 runs, 420 E5 greedy runs, 60 E5 calibration runs and
  350 full E5 Jensen–Shannon runs. Passed.
- Source-registry validation: current source and generated-file SHA-256 hashes,
  builder identity and principal results. Passed.
- Manuscript tests: three passed. Checks cover the principal numerical claims,
  LaTeX references, citation keys, figure existence and preservation of the original
  paired endpoint and the failed margin gate.
- Focused compatibility tests: 42 passed in 4.20 seconds.
- Ruff: passed on both manuscript Python files using the analysis repository's configuration.
- Tectonic: both PDFs compiled with no warnings on the final build.
- Visual inspection: all manuscript and supplementary pages inspected; updated figure
  legends and table-caption widths checked after recompilation.

The main PDF has nine pages, including one page of references. The supplement has seven.
Page reduction also reflects moving from the original article layout to the official
TMLR style; it is not a word-for-word compression ratio.

## Commands

From the analysis repository, with its locked environment:

```sh
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_phase1_tmlr_result_registry.py \
  tests/test_phase1_e1_jaccard_null.py \
  tests/test_phase1_e2_random_mask_fidelity.py \
  tests/test_phase1_e3_greedy_endpoint_trajectory.py \
  tests/test_phase1_e4_independent_search.py \
  tests/test_phase1_e5_nonargmax_fidelity.py \
  tests/test_nonmonotone_search.py tests/test_stage22_freeze.py
```

For the manuscript directory (the authoring copy was initially outside the analysis checkout):

```sh
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python manuscript/build_manuscript.py --repo .
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python manuscript/build_manuscript.py --repo . --validate-only
PHASE1_REPO="$PWD" MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/pytest -q manuscript/test_manuscript.py
.venv/bin/ruff check --config pyproject.toml manuscript/build_manuscript.py manuscript/test_manuscript.py
tectonic -X compile manuscript/main.tex --keep-logs
tectonic -X compile manuscript/supplement.tex --keep-logs
```

The original commands used the same executables with absolute paths to the authoring
directory; the commands above are the portable checkout equivalents. The manuscript
README gives the corresponding `uv` commands for the source archive.

## Outstanding publication checks

This remains an author-review preprint, not an anonymous TMLR submission. Author review,
anonymisation, and the journal submission itself have not been performed. The new
Zenodo archival version is pending because the service returned a 504 timeout. The
original DOI has not been modified. Full compressed search traces remain available
locally; the lightweight GitHub package contains their hash-checked results and masks.
