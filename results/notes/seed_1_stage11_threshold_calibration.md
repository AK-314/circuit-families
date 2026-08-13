# Stage 11 threshold calibration

- Stage 11 run ID: `stage11-calibration-s1-c2856467c00f`
- Source training run: `modular-addition-training-s1-5f1bc9dee7ab`
- Stable-post checkpoint: `9050`
- Random masks evaluated: `600`
- Random masks per threshold: `100`
- Sampling: uniform subset without replacement over all 516 searchable components; no head/neuron stratification
- Primary fidelity: exact prediction agreement with the full model
- Random-control pass rule: exact integer comparison to each candidate threshold
- Qualification: retained components <=258; random passes <=5; Stage 10 compatible or explained; Stage 9 exact evaluations <=10000
- Selected primary threshold: `0.990000`

No pre-grokking, transition, diversity-family, control-task, across-seed, Stage 12, or hypothesis-effect outcomes entered the selection.
