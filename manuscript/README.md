# Sparse Circuit Families Across Grokking

Read the [paper](main.pdf) and [supplement](supplement.pdf).
Edit `paper.tex` for the main text and `supplement.tex` for the supplement.

## Compile

The included figures and tables are sufficient; no experiment rerun is needed.
On Overleaf, upload this directory and select `main.tex` or `supplement.tex`.
Locally:

```sh
tectonic -X compile main.tex --keep-logs
tectonic -X compile supplement.tex --keep-logs
```

## Rebuild figures and tables

Extract `phase1-tmlr-followup-source.zip` from the
[follow-up release](https://github.com/AK-314/circuit-families/releases/tag/phase1-tmlr-revision-2026-09-13).
From that extracted analysis root:

```sh
uv sync --locked
uv run python /path/to/manuscript/build_manuscript.py --repo .
uv run python /path/to/manuscript/build_manuscript.py --repo . --validate-only
PHASE1_REPO="$PWD" uv run pytest -q /path/to/manuscript/test_manuscript.py
```

The builder reads frozen tables at scientific commit `8d138b8`, produces four
main figures, one supplementary figure and five supplementary tables, and records
input/output hashes in `source_registry.json`. It does not evaluate a model.
Display summaries are also exported under `generated/`.

## Submission preparation

These are named author-review PDFs in TMLR preprint style. Before submission,
switch to review style and anonymise the paper, supplement and code links.
The original [v1.0.0 DOI](https://doi.org/10.5281/zenodo.21917638) is unchanged;
Zenodo archival of the follow-up remains pending.

Build and numerical checks are recorded in [VALIDATION.md](VALIDATION.md).
Official TMLR style files are retained unchanged from
[revision 7bf90ef](https://github.com/JmlrOrg/tmlr-style-file/tree/7bf90efe3a0debbba703c05c43f3ff7e4d4a2992);
see `TMLR-STYLE-LICENSE`.
