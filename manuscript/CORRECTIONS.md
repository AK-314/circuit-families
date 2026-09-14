# Final claim and submission corrections — 14 September 2026

This is a manuscript and packaging revision, not a new experiment. E1–E5,
the exploratory evaluation, original uploads and earlier releases are unchanged.

## Corrections

- The shared-intersection result no longer excludes a sufficient proper subset.
  Its measured contribution and union failures remain prominent.
- Search endpoints are described as recovered sizes, not minimum necessary sizes.
- The abstract identifies the ten-member family finding as a retrospective audit
  of independently obtained endpoints.
- The text distinguishes a fixed Jaccard compatibility ceiling from unusual
  disjointness relative to a matched null; the stricter ceiling results remain.
- Same-mask fidelity explicitly states that seven seed-1 masks pass JS 0.05,
  although none passes calibrated JS 0.0005 or margin 0.4.
- Shi et al. (2024), Zhong et al. (2023) and McGrath et al. (2023) are cited.
  Union failures are not presented as a demonstration of Hydra self-repair.
- Supplement S4 replaces the layered provenance list with a timeline, preserving
  the per-metric calibration correction and identifying the reused calibration
  position. Informal draft feedback is distinguished from journal review.
- Anonymous review copies omit author, affiliation, acknowledgements and the
  identifying archive links. The named public version remains separate.

## Checks

- 95 focused scientific/compatibility tests passed (13.39 seconds).
- Seven manuscript tests passed, both against the original analysis root and
  against the anonymous export. One new regression test covers the claim fixes;
  the original-mask test now also checks the seven JS-0.05 successes.
- Ruff passed on the builder, manuscript tests and two packaging utilities.
- Named and anonymous main/supplement PDFs compile without warnings. Main: 13
  pages including references; supplement: 10. All anonymous pages and differing
  named pages were rendered and visually inspected; no overlaps or clipping.
- Anonymous PDF text, metadata and annotations were checked for author identifiers.
- The builder and both exploratory manifests validate within the anonymous export.
- A two-mask CPU reproduction smoke passed, including original agreement/JS,
  unchanged weights and restored hooks (0.342 seconds excluding loading).
  The first packaging smoke exposed a missing dataset metadata sidecar; it was
  included unchanged and the smoke was rerun successfully. No result was altered.

## Anonymous evidence export

The supplementary ZIP includes source, numerical tables, 1,185 E4/E5 endpoint
records and masks, the 700-stream audit, 70 fixed-mask records with per-input
arrays, four final checkpoint binaries, the dataset and its metadata, and the
27 original mask files. Nineteen identity-bearing historical metadata/document
files have separately logged export redactions. Numerical source files,
checkpoint binaries, evaluation code and protocol retain their original hashes.
Full longitudinal checkpoint binaries and proposal traces are not duplicated.

The export has its own file-hash inventory and runnable verification instructions.
It stays separate from the named public release. This is not a claim that every
historical absolute-path manifest is portable or that every search was rerun.

## Verification commands

From the analysis repository:

```sh
MPLCONFIGDIR=/private/tmp/phase1-tmlr-mpl .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_phase1_review_followup.py tests/test_phase1_tmlr_result_registry.py \
  tests/test_phase1_e1_jaccard_null.py tests/test_phase1_e2_random_mask_fidelity.py \
  tests/test_phase1_e3_greedy_endpoint_trajectory.py tests/test_phase1_e4_independent_search.py \
  tests/test_phase1_e5_nonargmax_fidelity.py tests/test_nonmonotone_search.py \
  tests/test_stage22_freeze.py tests/test_diversity_forced_search.py tests/test_masks.py \
  tests/test_fidelity.py tests/test_stage12_pipeline.py
```

The anonymous package README gives the exact self-contained validation and
reproduction commands. PDF builds use `tectonic -X compile main.tex --keep-logs`
and `tectonic -X compile supplement.tex --keep-logs` in each manuscript directory.
Visual checks use `pdftoppm -scale-to 1100 -png`.

Author sign-off and the OpenReview submission form remain. No journal submission
has been made. The original DOI is unchanged; no new Zenodo archival success is
claimed. No new mean-ablation, Fourier-mechanism or annealing-null experiment was
added in this final correction pass.
