# Stage 17 two-dimensional sensitivity analysis

Scientific robustness classification: **robust across the frozen sensitivity grid**.

The frozen primary cell remains fidelity 0.990 and maximum Jaccard overlap 0.50. It recovered 7 circuits under a fixed 50,000-evaluation cell budget. Reference cells reproduce Stage 12 rather than counting as fresh searches; the primary transfer profile reproduces Stage 16.

| Fidelity | cutoff 0.25 | cutoff 0.50 | cutoff 0.75 |
|---:|---:|---:|---:|
| 0.800 | 3 | 6 | 6 |
| 0.850 | 2 | 6 | 6 |
| 0.900 | 3 | 7 | 7 |
| 0.950 | 4 | 7 | 7 |
| 0.975 | 4 | 7 | 7 |
| 0.990 | 3 | 7 | 7 |

All values are fixed-budget recovered family sizes. A value of ten is right-censored at the family target, not a complete enumeration. Zero-family cells are scientific outcomes. Lower-fidelity expansion is weaker evidence than persistence at 0.990, and growth at cutoff 0.75 permits more structural reuse rather than proving more distinct mechanisms. Structural and transfer-distinct groups do not establish different algorithms.

Stage 15 remains unavailable with null endpoints. No checkpoint-grid decision was made, and Stage 18 was not started.
