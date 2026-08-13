# Stage 12 diversity-search validation

- Stage 12 run ID: `stage12-diversity-s1-020ebf1b5814`
- Scientific runtime telemetry is excluded from deterministic hashes.
- Exact distinctness uses maximum pairwise Jaccard over retained components.
- Unused restart slots are recorded explicitly.
- No pre-grokking or transition family search was run.
- Stage 13 has not begun.

## Completed cells

- `cutoff-0.50`: cutoff `0.50`, status `budget_exhaustion`, family size `7`, exact evaluations `50000`.
- `cutoff-0.25`: cutoff `0.25`, status `budget_exhaustion`, family size `3`, exact evaluations `28292`.
- `cutoff-0.75`: cutoff `0.75`, status `budget_exhaustion`, family size `7`, exact evaluations `50000`.

## C1 exact reproduction

- `cutoff-0.50`: passed (146 components; 6098 exact evaluations).
- `cutoff-0.25`: passed (146 components; 6098 exact evaluations).
- `cutoff-0.75`: passed (146 components; 6098 exact evaluations).

## Negative controls

- `stage11_matched_size_random_masks`: `rejection`.
- `degraded_c1_terminal_deletion`: `rejection`.
- `shuffled_ranking`: `budget_exhaustion`.
- `fidelity_impossible`: `no_feasible_candidate_discovered_within_tested_search`.
- `distinctness_impossible`: `distinctness_failure`.

## Method stress tests

- `stress_hard_component_exclusion`: `excluded_component_retained`.
- `stress_hard_overlap_constraint`: `candidate_rejected`.
- `stress_soft_overlap_penalty`: `formula_verified`.
