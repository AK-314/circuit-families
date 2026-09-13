# Phase I TMLR manuscript revision

**Sparse Circuit Families Across Grokking** — working author revision, 13 September 2026.

This replaces the presentation, not the frozen scientific record. The uploaded August
LaTeX archive and PDFs remain untouched. No training, circuit search, thresholds, phase
labels or result tables were changed for this revision. Phase II is not included.

## Read and edit

- `main.pdf`: revised paper, including references.
- `supplement.pdf`: methods, full tolerance grids, calibration, checkpoint-level results
  and the original secondary analyses.
- `paper.tex`: main prose; `main.tex`: author/title and build entry point.
- `supplement.tex`: supplementary prose and build entry point.
- `references.bib`: original bibliography with the directly relevant DeMoss et al. paper added.
- `generated/` and `figures/`: reproducibly generated displays, not manually edited results.

Both PDFs use the official TMLR **preprint** style and retain the author name. They are
author-review versions, not anonymous submission files and not submitted to TMLR.
Before submission, use the review style, remove identifying availability links and
acknowledgements, and provide an anonymised supplement/code package. The final prose,
references and AI-use statement still require the author's review.

The official style files are vendored unchanged from
<https://github.com/JmlrOrg/tmlr-style-file>, revision
`7bf90efe3a0debbba703c05c43f3ff7e4d4a2992`; their licence is `TMLR-STYLE-LICENSE`.

## Build

The main and supplement share one directory and compile independently. On Overleaf,
upload `phase1-tmlr-manuscript.zip` and select `main.tex` or `supplement.tex`. Use the
ordinary pdfLaTeX/BibTeX sequence. Locally, with Tectonic installed:

```sh
tectonic -X compile main.tex --keep-logs
tectonic -X compile supplement.tex --keep-logs
```

The included generated files are sufficient to compile; no scientific rerun is needed.

## Rebuild and validate figures/tables

Use the Phase I TMLR analysis checkout, or extract the matching
`phase1-tmlr-followup-source.zip` from the revision release. It contains the versioned
analysis source, configurations, result tables and provenance at scientific commit
`8d138b8`, without large checkpoints. In that analysis root:

```sh
uv sync --locked
uv run python /path/to/manuscript/build_manuscript.py --repo .
uv run python /path/to/manuscript/build_manuscript.py --repo . --validate-only
PHASE1_REPO="$PWD" uv run pytest -q /path/to/manuscript/test_manuscript.py
```

The builder performs no model evaluations. It validates coverage and headline counts,
reconstructs three figures and five supplementary tables, and records SHA-256 hashes
in `source_registry.json`. The validate-only mode checks the current inputs, generated
outputs and builder against that registry without writing anything. Position-level and
search-summary display data are also exported as CSV. Pairwise and random-mask displays
read the unchanged source tables directly.

The original v1.0.0 artifact DOI, `10.5281/zenodo.21917638`, identifies the earlier
frozen family study, not the E1–E5 extension. It remains the source of the selected
checkpoints and original detailed search archives. The revision release adds the
follow-up source and eligible E4/E5 per-run results and masks separately; it does not replace
that archive. The large compressed proposal traces have been hash-checked locally and
are reserved for the pending archival update, not included in the lightweight GitHub
package. Absolute paths inside old manifests are historical provenance, not
portable commands. Checkpoint-based reruns use the supplied scripts/configurations
with paths resolved in the extracted original artifact; manuscript rebuilding needs
only the lightweight result tables.

## Editorial changes

The main paper now follows the recovery trajectory, then the family and matched-null
evidence, then non-argmax preservation. Repeated operational definitions, redundant
heatmaps, separate research-question lists, and repeated scope paragraphs were removed.
The original paired endpoint and its `p = 0.125` are retained. The full margin grid and
failed margin calibration remain visible. Details of masking, stopping, calibration
and original secondary analyses are consolidated in the supplement.

The title is changed from *Grokking Opens a Family of Sparse Circuits* to avoid implying
a demonstrated causal mechanism. The main argument preserves multiplicity while
distinguishing it from first-circuit compression. E4/E5 are not described as independent
replications of entire families. The plateau and censoring fields are explicitly
distinguished; neither the search implementation nor its stored flags were altered.

## Publication state

This directory is an author-review revision. The GitHub update is additive and leaves
the v1.0.0 tag and original scientific files intact. A separate release guide records
the publication URLs and checksums. Zenodo publication is pending while its record
endpoint returns a gateway timeout; no new DOI is claimed here.
