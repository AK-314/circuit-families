# Circuit families across grokking

Code and data for a longitudinal study of sparse circuit recovery in five
modular-addition transformers.

**Paper:** [Sparse Circuit Families Across Grokking](manuscript/main.pdf)
([supplement](manuscript/supplement.pdf), [LaTeX and figure builder](manuscript/)).

The study finds a large reduction in recovered circuit size after stable
generalisation, together with several distinct masks that preserve the model's
predictions. The revised paper includes matched random-mask controls, independent
families, shared-core interventions, and distributional and margin fidelity analyses.

## Data and reproduction

The [original v1.0.0 archive](https://doi.org/10.5281/zenodo.21917638)
contains the selected checkpoints and detailed original search records.
The [follow-up release](https://github.com/AK-314/circuit-families/releases/tag/phase1-tmlr-review-followup-2026-09-13)
adds E1–E5 source, results and saved masks, plus the post-review evaluations and
current manuscripts. Earlier releases are preserved.

With Python 3.11 and [uv](https://docs.astral.sh/uv/):

```sh
uv sync --locked
uv run python reproduce.py results
uv run python reproduce.py figures
```

These inexpensive commands reproduce the original headline results and Figures 1–5
from the tables included here. To rebuild the revised paper's figures, use the
[manuscript instructions](manuscript/README.md).

See [REPRODUCE.md](reproduction/REPRODUCE.md) for checkpoint evaluation,
search reruns and training. Full verification (`uv run python reproduce.py`)
requires the complete original archive.

## Citation and licence

Citation metadata: [CITATION.cff](CITATION.cff).
Code: [MIT](LICENSE). Data, checkpoints, results and reproduction documentation:
[CC BY 4.0](LICENSE-DATA), except where otherwise noted.
