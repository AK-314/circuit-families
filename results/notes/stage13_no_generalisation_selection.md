# Stage 13 no-generalisation selection

- Stage 13 run ID: `stage13-no-generalisation-s0-154f43de1214`
- Matched horizon: `9050`
- Candidate execution and selection order: `0.25, 0.20, 0.15, 0.10, 0.05`
- Selection rule: choose the largest candidate satisfying all five frozen qualification criteria.
- Selection outcome: `no_qualifying_fraction`
- Permitted evidence: saved training accuracy, test accuracy and test cross-entropy curves only.
- Control circuit-family metrics inspected: `false`
- Stage 14 started: `false`
- Stage 15 started: `false`

## Qualification summary

| Fraction | Count | First ≥99.9% step | Persistence | Max test accuracy | Loss fall | Qualified | Selected |
|---:|---:|---:|---:|---:|---:|:---:|:---:|
| 0.25 | 3192 | 200 | 174/177 (0.983050847458) | 0.0645486041903 | 0.12972387996 | false | false |
| 0.20 | 2553 | 200 | 174/177 (0.983050847458) | 0.0154379680753 | 0.198286642863 | false | false |
| 0.15 | 1915 | 150 | 175/178 (0.983146067416) | 0.0108513254672 | 0.326686763783 | false | false |
| 0.10 | 1276 | 150 | 176/178 (0.988764044944) | 0.0214789118618 | 0.541510777154 | false | false |
| 0.05 | 638 | 100 | 175/179 (0.977653631285) | 0.0149904908612 | 0.507380671796 | false | false |

## Resolved interval ambiguity

The frozen mathematical inequalities are followed: `8050 < step <= 9050` gives checkpoints `8100, 8150, ..., 9050`, while `7050 < step <= 8050` gives `7100, 7150, ..., 8050`. Both windows contain 20 disjoint saved checkpoints.

## Data-coverage limitation

The matched no-generalisation control changes the fraction of the original training partition available to the model. It therefore controls for training time, architecture, optimiser and regularisation while deliberately changing data coverage. Any later difference between the main condition and this control cannot be attributed solely to generalisation without acknowledging the reduced-data intervention.
