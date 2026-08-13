# Stage 18 main-seed scaling

Run ID: `stage18-scaling-24a9adb84176`.

## Design and execution

The five-seed target and realised registry are seeds 0, 1, 2, 3 and 4. No reserve seed was required. Seed 1 is the exact Stage 17 reference at step 9050; all other registered positions were executed under Stage 18. The frozen checkpoint grid is 200, 3400, 7450, 8150, 8500, 8650 and 9050.

The analysis contains 630 registered fidelity-by-distinctness cells: 612 fresh executions and 18 exact Stage 17 references. Production used 12 isolated workers with one intra-op and one inter-op thread per worker. Worker output directories were disjoint and final merging and archive construction were serial.

Additional random-label seeds are frozen at zero because resources are prioritised for the five required main seeds. Stage 15 remains unavailable.

## Training outcomes

- seed 0: `complete_grokking_seed` at step 40000 using `stage18-main-training-s0-58b8c1235464` (fresh_execution)
- seed 1: `complete_grokking_seed` at step 40000 using `modular-addition-training-s1-5f1bc9dee7ab` (reference_existing_result)
- seed 2: `complete_grokking_seed` at step 40000 using `stage18-main-training-s2-c70f62c0fa7c` (fresh_execution)
- seed 3: `complete_grokking_seed` at step 40000 using `stage18-main-training-s3-4c0c7c63ce2f` (fresh_execution)
- seed 4: `complete_grokking_seed` at step 40000 using `stage18-main-training-s4-c2881c226349` (fresh_execution)

## Primary descriptive trajectories

Each entry is `checkpoint:family size,transfer-group count` at fidelity 0.990 and Jaccard cutoff 0.50.

- seed 0: 200:family=0,groups=NA, 3400:family=0,groups=NA, 7450:family=7,groups=1, 8150:family=7,groups=1, 8500:family=7,groups=1, 8650:family=6,groups=1, 9050:family=6,groups=1
- seed 1: 200:family=0,groups=NA, 3400:family=0,groups=NA, 7450:family=0,groups=NA, 8150:family=0,groups=NA, 8500:family=0,groups=NA, 8650:family=0,groups=NA, 9050:family=7,groups=1
- seed 2: 200:family=0,groups=NA, 3400:family=0,groups=NA, 7450:family=0,groups=NA, 8150:family=7,groups=1, 8500:family=7,groups=1, 8650:family=7,groups=1, 9050:family=7,groups=1
- seed 3: 200:family=0,groups=NA, 3400:family=0,groups=NA, 7450:family=0,groups=NA, 8150:family=0,groups=NA, 8500:family=0,groups=NA, 8650:family=0,groups=NA, 9050:family=0,groups=NA
- seed 4: 200:family=0,groups=NA, 3400:family=0,groups=NA, 7450:family=7,groups=1, 8150:family=7,groups=1, 8500:family=6,groups=1, 8650:family=6,groups=1, 9050:family=7,groups=1

## Surface outcomes and limitations

Observed empty-family cells: 330. Non-complete search-status cells: 630. Right-censored cells: 0. Every nonempty fresh family received transfer evaluation and deterministic complete-linkage grouping at tolerance 0.05. Empty-family transfer counts remain absent rather than zero.

These raw within-seed checkpoint trajectories are descriptive. The analysis does not establish an across-seed inferential conclusion, does not repair the unavailable Stage 15 control, and adds no further random-label control seed. Matched comparisons, sign tests, permutation summaries and across-seed inference are deferred to Stages 19-20.
