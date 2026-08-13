# Stage 19 matched comparisons

- Run ID: `stage19-matched-02b89bd79ed8`
- Lifecycle status: `provisionally_validated`
- Matched-fidelity comparisons: 105
- Matched-sparsity comparisons: 105
- Explicit empty cells: 330
- Pareto-frontier rows: 178
- Complete Stage 18 input cells: 630
- Nonempty / empty / singleton cells: 300 / 330 / 3.
- Fidelity matching tolerance: 0.01 exact global fidelity.
- Sparsity matching tolerance: five retained components.
- Matching maximises valid cardinality and then minimises total absolute difference.
- Matching is symmetric joint one-to-one selection without replacement. Exact observed circuit values are used; interpolation and rounded-display matching are prohibited. Remaining ties are broken by deterministic circuit identity order.
- Empty families are reported directly, never imputed, and excluded only where the metric is undefined.
- Circuits and search restarts are not treated as independent experimental units.
- Pareto axes are exact circuit fidelity (higher is better) and retained component count (fewer is better); duplicate masks are canonicalised deterministically and no smoothing is used.

These outputs were generated from the definitive Stage 18 run. Independent Stage 18 reproduction comparison was pending at the time of generation. The results are therefore provisionally validated and must be revalidated after reproduction completes.
