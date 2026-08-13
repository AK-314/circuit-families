# Stage 14 random-label training control

- Stage 14 run ID: `stage14-random-label-training-s0-df790c07a988`
- Implementation commit: `83ac9bdf42b79cf097b7cfc1b6843bd274b7dbcb`
- Model seed: `0`
- Random-label seed: `1`
- Device: `cpu`
- Matched training horizon: `9050`
- Evaluation interval: `50`
- Checkpoint interval: `50`
- Saved metric records: `182`
- Saved checkpoints: `182`
- Reload-verified checkpoints: `182`
- Random-label classification threshold: `0.99`
- Control classification: `memorisation_control`

## Frozen random-label data

- Input pairs: `12,769`
- Training examples: `3,830`
- Test examples: `8,939`
- Random-label construction: deterministic PCG64 permutation of the complete true-label vector
- Global class balance: exactly `113` examples for each of the `113` output classes
- Accidental matches to true labels: `129`
- Canonical dataset SHA-256: `af13d2181f5f1122bc528c6dfadbdc67b0a38ea02c10b4fd504a492aca8afafa`
- Split SHA-256: `c83ac398724817fae6a0d137d0f1c6d0b8786eee43efaff5c3d34de0a891b7f2`
- Random-label permutation SHA-256: `6133ae3b6535595aae903ba9197c6b136b2667a50553fbda3a49331765cb30e5`
- Random-label vector SHA-256: `5a4f92635efff86f168c8999b426be000cbdf5e6194e6e7b5d537243583ac5c9`

## Training outcome

- First saved step reaching at least 99% training accuracy: `200`
- Final training accuracy: `1`
- Final test accuracy: `0.010403848253190517`
- Chance accuracy: `0.0088495575221238937`
- Maximum saved test accuracy: `0.011186934076249599` at step `6750`
- Final training cross-entropy: `9.9223780125612393e-07`
- Final test cross-entropy: `32.369037628173828`
- Minimum saved test cross-entropy: `4.7345380783081055` at step `0`

The model memorised the frozen random labels within the matched horizon and therefore qualifies as a `memorisation_control`. Test accuracy remained close to chance in accuracy terms, so the run does not show learning of the underlying modular-addition mapping.

## Exact checkpoint matching

The random-label checkpoints were matched by exact saved training step to the seven main-model reference landmarks:

`200, 3400, 7450, 8150, 8500, 8650, 9050`

Every absolute step mismatch was `0`. Main-model phase names are retained only as reference labels and are not assigned as phases of the random-label model.

## Masking-machinery validation

The existing Stage 8 masking machinery was validated on all seven matched checkpoints using all `12,769` examples and evaluation batch size `256`.

- Seven all-retained cases reproduced the full-model outputs exactly.
- Stable-step all-ablated, H0-ablated and N0-ablated interventions executed successfully.
- The arbitrary saved mask reloaded exactly.
- Model-state hashes were unchanged.
- Parameter gradients remained absent.
- Temporary hooks were removed.
- Output classes were restricted to `0–112`; the equals token was excluded.
- Evaluation used the final token position.

This validates the masking machinery only. No random-label sparse circuit or diversity family was searched.

## Independent reproduction

A second complete CPU execution at the same frozen implementation commit reproduced:

- all `182` metric records;
- all `182` checkpoint-file hashes;
- all `182` model-state hashes;
- all `182` optimiser-state hashes;
- all reload-verification flags;
- all seven exact checkpoint matches;
- the `memorisation_control` classification;
- all three deterministic tables; and
- all five saved mask files.

The independent reproduction status is `passed`.

## Scope boundary

- Random-label sparse search started: `false`
- Diversity search started: `false`
- Stage 15 started: `false`

Stage 14 establishes the random-label training and checkpoint-matching foundation only. Circuit-family recovery remains outside this stage.
