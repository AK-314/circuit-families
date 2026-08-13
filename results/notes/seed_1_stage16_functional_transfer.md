# Stage 16 genuine-task functional-transfer analysis

- Stage 16 run: `stage16-transfer-s1-cc55bd4162c8`
- Source training run: `modular-addition-training-s1-5f1bc9dee7ab`
- Model seed: `1`
- Stable post-grokking checkpoint: step `9050`
- Source structural family: Stage 12 primary `cutoff-0.50` cell
- Structural family size: `7`
- Fidelity threshold: `0.99`
- Sparsity boundary: at most `258 / 516` components
- Transfer subsets: Q1 lower/lower, Q2 lower/higher, Q3 higher/lower, Q4 higher/higher
- Transfer-distinct group counts (0.025: 1, 0.050: 1, 0.100: 1)

## Subset-discovery outcomes

- Q1: `valid_meaningfully_sparse`
- Q2: `valid_meaningfully_sparse`
- Q3: `valid_meaningfully_sparse`
- Q4: `valid_meaningfully_sparse`

## Primary conclusion

The seven structurally distinct circuits are largely functionally interchangeable under the frozen transfer rule.

The group count is procedure-dependent: it is the transfer-distinct group count under the frozen fidelity profile, maximum-distance rule, complete linkage and tolerance. It is not the true number of mechanisms. Transfer-equivalent circuits are not thereby mechanistically identical.

Subset discovery is a bounded greedy search. Failure or budget exhaustion does not establish that no eligible sparse circuit exists. Stage 15 remains unavailable rather than an executed empty family. Stage 17 was not begun.
