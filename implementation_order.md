# **Lumiere Grokking Project: Implementation Order**

## **Governing principle**

First establish that diversity-forced circuit-family recovery works end to end on one grokking model. Then run the identical fixed-budget procedure on one random-label control and one matched no-generalisation control. Only after the method and controls work should the project scale across seeds, checkpoints, thresholds, matched comparisons, and robustness analyses.

The plan must prioritise scientific validity over package completeness. The core output is the experiment, not a general-purpose interpretability library.

---

# **Scope hierarchy**

## **Core — cannot be removed**

* One complete grokking seed.  
* Dense training checkpoints.  
* Rule-based pre-, transition-, and post-grokking selection.  
* Component masking and exact fidelity evaluation.  
* Sparse-circuit recovery.  
* Early Fourier-style sanity check.  
* Primary fidelity-threshold freeze before family search.  
* Diversity-forced circuit-family search.  
* Search-validation and negative controls.  
* One random-label control.  
* One matched no-generalisation control.  
* Functional-transfer tests.  
* Fidelity-threshold sensitivity.  
* Structural-distinctness sensitivity.  
* Matched-fidelity and matched-sparsity analyses.  
* Seed-level paired aggregation.  
* Reproducible figures and tables.

## **Important but reducible**

* Full six-landmark analysis on every seed.  
* Five complete main seeds.  
* Multiple seeds for both controls.  
* Large threshold and distinctness grids.  
* Comprehensive automated testing.  
* Full clean-environment reproduction.

## **Stretch**

* Edge-level circuit analysis.  
* Large robustness grids.  
* Full OSF packaging before the paper draft.  
* General-purpose software infrastructure.

---

# **Stage 1 — Freeze all pre-results scientific decisions**

## **Implement**

Create `experimental_protocol.md` and timestamp it before examining circuit-family results.

Freeze:

* research question;  
* H1, H2, and mixed prediction;  
* hypothesis-prediction table;  
* modular-addition task;  
* modulus;  
* data split procedure;  
* model architecture;  
* optimiser;  
* weight decay;  
* checkpointing strategy;  
* model-seed definition;  
* phase-definition rules;  
* component granularity;  
* fidelity definitions;  
* search-budget definition;  
* structural-distinctness definition;  
* transfer subsets;  
* control-selection procedure;  
* statistical-analysis plan.

## **Predictions table**

The predictions table must be written now, not at the final analysis freeze.

It should specify expected patterns for:

* recovered structural family size;  
* circuit size;  
* pairwise overlap;  
* transfer-distinct group count;  
* cross-subset transfer;  
* controls;  
* matched-fidelity results;  
* matched-sparsity results.

Any later alteration must be dated and recorded as an amendment or exploratory analysis.

## **Statistical plan**

Use the trained model seed as the independent unit.

The primary across-seed comparisons should be **within-seed phase changes**, for example:

\[  
\\Delta\_s \=  
M\_{s,\\mathrm{post}}-M\_{s,\\mathrm{pre}}  
\]

where (M) is family size, overlap, circuit size, transfer score, or transfer-distinct group count.

Report:

* each seed’s paired delta;  
* sign consistency;  
* median or mean paired delta;  
* full seed-level range;  
* exact sign or permutation reasoning where appropriate.

With five seeds, do not make bootstrap confidence intervals or conventional significance thresholds carry the argument.

### **Statistical handling of empty circuit families**

Recovered structural family size is defined as zero when no valid circuit family is recovered under the fixed search procedure and budget. Family-size deltas are therefore computed normally.

Metrics that require one or more recovered circuits—such as median circuit size, median pairwise overlap and transfer-distinct group count—are recorded as undefined when the relevant family is empty. Undefined values are not converted to zero and are excluded from paired deltas requiring that metric. The empty-family outcome must be reported alongside the remaining seed-level results and retained in family-size and search-failure analyses.

## **Deliverables**

* `experimental_protocol.md`  
* frozen hypothesis-prediction table;  
* task and model specification;  
* phase-selection rules;  
* fidelity definitions;  
* structural-distinctness definition;  
* control-selection protocol;  
* statistical-analysis note;  
* dated amendment log.

## **Acceptance gate**

No primary scientific hypothesis or comparison is created after its result is visible.

---

# **Stage 2 — Freeze the calibration and sensitivity rules**

## **Fidelity threshold**

Before circuit search, freeze:

* the fidelity-threshold grid;  
* the rule for calibrating the primary threshold;  
* the pilot information permitted for calibration.

Example grid:

80%, 85%, 90%, 95%, 97.5%, 99%

The exact grid must be recorded before calibration.

## **Primary-threshold calibration rule**

Calibrate the primary threshold using:

* the first post-grokking sparse-circuit pilot;  
* exact fidelity evaluation;  
* circuit sparsity;  
* matched-size random-mask failure.

Choose a threshold that:

* permits recovery of a meaningfully sparse post-grokking circuit;  
* is not so permissive that matched-size random masks frequently pass;  
* remains computationally feasible.

For primary-threshold calibration, a circuit is provisionally defined as meaningfully sparse when it retains no more than 50% of the searchable components while satisfying the exact fidelity requirement.

This cutoff must be frozen in the protocol before threshold calibration. Any alternative sparsity cutoff is treated as a sensitivity analysis rather than grounds for changing the primary threshold.

Do **not** require a sparse pre-grokking circuit to exist.

A failure to recover a pre-grokking circuit at the frozen threshold is a potentially meaningful result, not a calibration failure.

## **Structural-distinctness rule**

Freeze:

* one primary maximum-overlap cutoff;  
* at least two sensitivity cutoffs;  
* the overlap metric, provisionally Jaccard overlap.

For example, the protocol might examine stricter, primary, and looser maximum-overlap rules. The exact values must be chosen before the diversity-family result is examined.

Recovered family size will later be reported as a function of:

\[  
\\text{fidelity threshold}  
\\quad\\text{and}\\quad  
\\text{distinctness cutoff}.  
\]

## **Deliverables**

* frozen fidelity grid;  
* written primary-threshold calibration rule;  
* primary structural-distinctness cutoff;  
* distinctness-sensitivity grid;  
* random-mask calibration procedure.

## **Acceptance gate**

Neither the fidelity threshold nor the distinctness criterion is selected to maximise the observed pre-to-post difference.

---

# **Stage 3 — Build the minimal repository**

## **Implement**

Create:

lumiere-grokking/  
├── configs/  
├── src/  
├── scripts/  
├── data/  
├── checkpoints/  
├── results/  
├── figures/  
├── manifests/  
├── tests/  
├── pyproject.toml  
├── README.md  
├── LICENSE  
└── .gitignore

Immediately implement only:

* config loading;  
* deterministic seed handling;  
* run IDs;  
* structured result saving;  
* manifest creation;  
* minimal smoke tests.

Defer:

* comprehensive dependency locking;  
* continuous integration;  
* extensive unit-test coverage;  
* polished library abstractions.

## **Parallel protocol rule**

Stage 1 and Stage 3 may continue in parallel during early implementation.

However:

* predictions must be frozen before any result exists;  
* fidelity definitions must be frozen before sparse search;  
* distinctness rules must be frozen before diversity search;  
* control-selection rules must be frozen before inspecting control circuits.

## **Deliverables**

* runnable repository;  
* installation instructions;  
* configuration loader;  
* run-ID system;  
* manifest format;  
* minimal smoke test.

## **Acceptance gate**

The first model can be trained and its outputs saved without requiring a mature software package.

---

# **Stage 4 — Generate the task data**

## **Implement**

Generate:

* all ordered modular-addition operand pairs;  
* correct modular labels;  
* fixed train/test assignments;  
* random-label versions using the same inputs and split structure.

Record:

* modulus;  
* dataset seed;  
* split seed;  
* dataset hash;  
* exact split membership.

Define transfer subsets before inspecting circuit results.

Possible subsets:

* operand ranges;  
* residue classes;  
* diagonal versus off-diagonal inputs;  
* structured held-out regions;  
* balanced random partitions.

## **Deliverables**

* `modular_addition.py`  
* `random_labels.py`  
* `splits.py`  
* `input_subsets.py`  
* dataset manifest;  
* saved splits;  
* reproducibility test.

## **Acceptance gate**

Regenerating the dataset from the same config produces the same hash.

---

# **Stage 5 — Implement training and dense checkpointing**

## **Implement**

Use a small configurable transformer, preferably through TransformerLens unless that becomes an obstacle.

Record:

* train loss;  
* test loss;  
* train accuracy;  
* test accuracy;  
* training step;  
* learning rate;  
* weight norm;  
* gradient norm where practical;  
* checkpoint path.

## **Checkpoint policy**

Save very densely throughout training.

Use either:

* a fixed small checkpoint interval; or  
* a fixed interval plus denser saving once test loss or accuracy begins changing.

The interval must be recorded before the main runs.

Dense saving is necessary because a sharp grokking transition may pass between sparse checkpoints.

## **Deliverables**

* training script;  
* model config;  
* checkpoint saver;  
* checkpoint loader;  
* metric logger;  
* reload test.

## **Acceptance gate**

Every saved checkpoint reproduces its recorded evaluation metrics.

---

# **Stage 6 — Train the first grokking seed**

## **Implement**

Train one main model until it shows:

* near-perfect training accuracy;  
* delayed low test performance;  
* a clear rise in test performance;  
* stable high test accuracy.

Check:

* train/test leakage;  
* incorrect labels;  
* evaluation errors;  
* checkpoint corruption;  
* unstable optimisation.

## **Deliverables**

* complete first training run;  
* training and test curves;  
* dense checkpoint collection;  
* provisional Figure 1;  
* training manifest.

## **Acceptance gate**

The observed transition is credible grokking rather than a logging or evaluation artefact.

---

# **Stage 7 — Select checkpoints for circuit-family dynamics**

## **Primary phase checkpoints**

Select:

* one pre-grokking checkpoint with very high training accuracy and low test accuracy;  
* transition checkpoints nearest the target accuracy landmarks;  
* one stable post-grokking checkpoint.

## **Landmark grid**

The preferred dynamic grid is:

pre-grokking  
10%  
25%  
50%  
75%  
90%  
99% / stable post-grokking

For each target, record:

* target accuracy;  
* nearest achieved accuracy;  
* training step;  
* checkpoint path;  
* phase label.

## **Prospective compute fallback**

The diversity-forced analysis should be run at every landmark where computationally feasible.

If the Stage 12 compute projection shows this is infeasible, apply one uniform reduced grid to all main seeds, for example:

pre-grokking  
50%  
stable post-grokking

or:

10%  
50%  
99%

The reduced grid must be selected before scaling and applied uniformly. Do not analyse dense landmarks for convenient seeds and sparse landmarks for difficult ones.

## **Deliverables**

* `phase_detection.py`  
* checkpoint manifest;  
* target-versus-achieved accuracy table;  
* dynamic-grid specification;  
* fallback-grid rule.

## **Acceptance gate**

The experiment contains enough checkpoints to support a transition or dynamics claim, not merely an endpoint comparison.

---

# **Stage 8 — Implement component masking and fidelity evaluation**

## **Implement**

Support independent masking of:

* attention heads;  
* individual MLP neurons.

Required tests:

1. all components retained;  
2. all components ablated;  
3. one head ablated;  
4. one neuron ablated;  
5. saved mask reloaded.

Evaluate:

* agreement with full-model predictions;  
* ground-truth accuracy;  
* cross-entropy;  
* output-distribution divergence where practical;  
* number and proportion of retained components.

## **Computational fallback**

Preferred:

attention heads \+ individual MLP neurons

Fallback:

Stage 1: attention heads \+ whole MLP blocks  
Stage 2: neuron-level refinement within retained blocks

Hierarchical results must be labelled as hierarchical search results.

## **Deliverables**

* `masks.py`  
* `component_ablation.py`  
* `fidelity.py`  
* mask format;  
* ablation tests;  
* standard circuit record.

## **Acceptance gate**

The all-retained mask reproduces the full model exactly within numerical tolerance.

---

# **Stage 9 — Recover the first sparse circuits**

## **Implement**

Use a transparent greedy search:

1. begin with all components;  
2. rank possible removals;  
3. exactly test the best-ranked candidates;  
4. remove the least damaging valid candidate;  
5. repeat until the fidelity threshold would be violated;  
6. optionally perform local refinement.

## **Search acceleration**

Use attribution or first-order damage estimates to rank components if exact leave-one-out scoring is too expensive.

Approximate scoring may rank candidates, but every accepted removal must pass exact forward evaluation.

Run on:

* the first post-grokking checkpoint;  
* the first pre-grokking checkpoint;  
* one transition checkpoint where practical.

## **Deliverables**

* `sparse_search.py`  
* first post-grokking circuit;  
* first pre-grokking result, including a valid empty outcome if no sparse circuit is recovered;  
* first transition result;  
* search trajectories;  
* runtime and evaluation counts.

## **Acceptance gate**

Every reported circuit independently satisfies the candidate threshold used for calibration.

---

# **Stage 10 — Run the early Fourier-style sanity check**

## **Implement**

Check whether:

* the full post-grokking model exhibits expected Fourier-style structure;  
* the recovered sparse circuit retains components associated with that structure;  
* removing relevant retained components damages the expected behaviour.

This is a pipeline diagnostic, not proof of uniqueness.

A mismatch should trigger investigation of:

* checkpoint identity;  
* masking;  
* fidelity evaluation;  
* component indexing;  
* search objective;  
* distributed or alternative implementations.

## **Deliverables**

* `fourier_sanity_check.py`  
* Fourier diagnostic figures;  
* component-association analysis;  
* debugging note where necessary.

## **Acceptance gate**

Any conflict between known model structure and the recovered circuit is investigated before diversity search begins.

---

# **Stage 11 — Freeze the primary fidelity threshold**

## **Ordering rule**

The primary threshold must be frozen **now**, after:

* the first post-grokking sparse-circuit pilot;  
* the random-mask permissiveness check;  
* the early Fourier sanity check.

It must be frozen **before diversity-forced family search**.

The threshold calibration must not use:

* pre-to-post family-size differences;  
* control family results;  
* diversity-forced family counts;  
* across-seed outcomes.

If an early diversity-search prototype is required for software debugging, label it:

method-development output, excluded from all scientific family comparisons.

After the threshold is frozen, regenerate every reported diversity-family result from scratch.

## **Deliverables**

* calibration record;  
* frozen primary fidelity threshold;  
* threshold-freeze timestamp or commit;  
* excluded-development-output register.

## **Acceptance gate**

No reported circuit family was created under an unfrozen primary threshold.

---

# **Stage 12 — Implement and validate diversity-forced search**

## **Implement**

Recover circuits sequentially:

1. find (C\_1);  
2. search for (C\_2) while limiting overlap with (C\_1);  
3. search for (C\_3) while limiting overlap with (C\_1) and (C\_2);  
4. continue until the family target or budget is exhausted.

Every alternative must satisfy:

* exact fidelity validity;  
* structural-distinctness rule.

Test:

* soft overlap penalties;  
* reuse costs;  
* hard overlap limits;  
* hard exclusions as stress tests.

## **Negative-control validation**

Test:

* matched-size random masks;  
* degraded valid circuits;  
* shuffled component rankings;  
* settings where fidelity cannot be preserved.

Classify outcomes:

* valid distinct circuit;  
* fidelity failure;  
* distinctness failure;  
* optimiser failure;  
* budget exhaustion;  
* no feasible candidate discovered within the tested search.

## **Compute projection**

Record:

* evaluations per circuit;  
* runtime per circuit;  
* circuits requested per checkpoint;  
* planned checkpoint count;  
* threshold count;  
* distinctness-cutoff count;  
* seed count;  
* control count.

Project the total compute before scaling.

## **Deliverables**

* `diversity_forced_search.py`  
* `overlap_constraints.py`  
* search diagnostics;  
* validated pilot family;  
* fidelity–sparsity–overlap–effort frontier;  
* compute projection.

## **Acceptance gate**

The search produces valid distinct alternatives and cannot easily manufacture families from degraded or random masks.

---

# **Stage 13 — Select the matched no-generalisation control**

## **Hold fixed**

* architecture;  
* optimiser;  
* optimiser settings;  
* weight decay;  
* evaluation procedure;  
* checkpoint procedure;  
* circuit-search procedure.

Do not change weight decay, because regularisation-driven compression is one of the confounds the control is meant to address.

## **Primary intervention**

Use a prespecified training-fraction grid to identify a regime that:

* reaches very high training accuracy;  
* remains at low test accuracy;  
* does not show an incipient generalisation transition within the matched budget.

Use training and test curves only.

Freeze the selected regime before inspecting any circuit-family metric.

## **Deliverables**

* training-fraction pilot grid;  
* control-selection record;  
* frozen no-generalisation config;  
* explicit data-coverage limitation.

## **Acceptance gate**

The control was selected independently of its circuit-family outcome.

---

# **Stage 14 — Run the random-label control**

## **Checkpoint matching**

Random-label models do not have meaningful test-accuracy landmarks.

Match their checkpoints by **training step** to the main run’s selected landmark steps.

For each main checkpoint step, use the random-label checkpoint at the same or nearest saved step.

Record any mismatch.

## **Pipeline**

Run the identical:

* masking;  
* sparse search;  
* diversity search;  
* fidelity evaluation;  
* transfer analysis;  
* threshold and distinctness sensitivity.

## **Deliverables**

* random-label training run;  
* step-matched checkpoints;  
* sparse circuits;  
* circuit families;  
* transfer results;  
* search diagnostics.

## **Acceptance gate**

The random-label model received the same search budget and was evaluated at matched training times.

---

# **Stage 15 — Run the matched no-generalisation control**

## **Checkpoint matching**

The matched no-generalisation control is evaluated at checkpoints matched by training step to the main run’s selected landmark checkpoints. For each main-run landmark, use the control checkpoint saved at the same step or the nearest available step, and record the absolute step difference.

Test-accuracy landmarks are not used for matching because the control is selected specifically not to undergo the corresponding generalisation transition.

## **Implement**

Apply the complete frozen pipeline:

* checkpoint selection;  
* component masking;  
* sparse search;  
* diversity-forced search;  
* transfer;  
* threshold sweep;  
* distinctness sweep.

Use behaviourally comparable stages and matched training budgets.

## **Deliverables**

* no-generalisation training curve;  
* selected checkpoints;  
* circuit families;  
* transfer results;  
* sensitivity results;  
* diagnostics.

## **Acceptance gate**

The control differs through the frozen training-fraction intervention rather than altered regularisation.

---

# **Stage 16 — Run functional-transfer analysis**

## **Implement**

For every discovery subset:

1. discover a circuit on subset (A);  
2. evaluate it on (A);  
3. transfer it unchanged to subsets (B), (C), and (D);  
4. record fidelity and accuracy.

Construct:

# **\[**

# **T\_{ij}**

\\text{fidelity of a circuit discovered on subset }i  
\\text{ when tested on subset }j.  
\]

## **Two family quantities**

### **Recovered structural family size**

Number of valid circuits satisfying the structural-distinctness rule.

### **Transfer-distinct group count**

Group circuits by prespecified transfer-profile similarity.

Report:

* the primary grouping tolerance;  
* sensitivity across alternative tolerances.

Do not describe this as the true number of mechanisms.

## **Deliverables**

* `transfer.py`  
* transfer matrices;  
* structural-overlap versus transfer-similarity analysis;  
* structural family size;  
* transfer-distinct group count;  
* grouping-tolerance sensitivity.

## **Acceptance gate**

Structurally different circuits are not automatically treated as functionally different explanations.

---

# **Stage 17 — Run two-dimensional sensitivity analysis**

## **Fidelity sweep**

Run the frozen fidelity grid.

## **Structural-distinctness sweep**

Run the frozen overlap-cutoff grid.

Report recovered family size as:

\[  
F(\\tau\_f,\\tau\_d)  
\]

where:

* (\\tau\_f) is the fidelity threshold;  
* (\\tau\_d) is the structural-distinctness cutoff.

At minimum produce:

* family-size-versus-fidelity curves at several distinctness cutoffs;  
* family-size-versus-distinctness curves at several fidelity thresholds;  
* search-failure rates;  
* circuit-size summaries;  
* transfer-distinct group counts where available.

## **Empty-family rule**

A zero recovered family is a result, not missing data.

If a condition has no valid circuits at a threshold:

* report zero;  
* retain it in threshold curves;  
* report the failure reason;  
* do not fabricate matched comparisons.

## **Deliverables**

* `threshold_sweep.py`  
* `distinctness_sweep.py`  
* two-dimensional sensitivity tables;  
* curves and heatmaps;  
* empty-family records.

## **Acceptance gate**

The headline conclusion is not dependent on one arbitrary fidelity or overlap cutoff.

---

# **Stage 18 — Scale across dynamics checkpoints and seeds**

## **Checkpoint requirement**

For the pilot main seed, run diversity-family recovery at the full preferred landmark grid.

For scaled main seeds, use either:

* the full landmark grid; or  
* the prospectively selected reduced grid from the compute projection.

Use the same grid for all scaled seeds.

## **Main seeds**

Run at least five main model seeds where feasible.

For each seed, perform:

* training;  
* phase selection;  
* sparse search;  
* diversity search;  
* transfer;  
* sensitivity analysis.

## **Controls**

Scale controls as resources permit.

Priority:

1. second no-generalisation seed;  
2. second random-label seed;  
3. further control seeds.

If only one control seed exists, comparisons remain descriptive.

## **Deliverables**

* complete main-seed manifests;  
* per-seed dynamic curves;  
* per-seed paired phase results;  
* available multi-seed controls;  
* compute-use record.

## **Acceptance gate**

A dynamics claim is supported by repeated checkpoint measurements, and an across-seed claim is not based on one unusually clean run.

---

# **Stage 19 — Run matched comparisons and handle degenerate cells**

## **Matched fidelity**

Compare circuits at approximately equal fidelity.

## **Matched sparsity**

Compare circuits at approximately equal size.

## **Degenerate-cell rule**

Matched comparisons are reported only where both relevant conditions contain valid circuits under the matching rule.

When a condition has no valid family:

* report the empty outcome directly;  
* show where it becomes non-empty in the sensitivity curves;  
* do not treat the cell as ordinary missing data;  
* do not impute a circuit family.

An empty family may itself support a substantive conclusion, but it cannot enter a matched-size or matched-fidelity estimate that requires existing circuits.

## **Deliverables**

* `matched_comparisons.py`  
* matched-fidelity tables;  
* matched-sparsity tables;  
* Pareto frontiers;  
* explicit empty-cell table.

## **Acceptance gate**

No comparison silently excludes conditions because valid circuits were difficult or impossible to recover.

---

# **Stage 20 — Aggregate with paired seed-level inference**

## **Primary summaries**

For every seed, compute paired changes across checkpoints, particularly:

* pre to post;  
* pre to transition;  
* transition to post;  
* adjacent landmark changes.

Metrics:

* recovered structural family size;  
* transfer-distinct group count;  
* median overlap;  
* median circuit size;  
* transfer score;  
* matched-fidelity diversity;  
* matched-sparsity fidelity.

## **Report**

* raw seed trajectories;  
* paired deltas;  
* sign consistency;  
* median or mean delta;  
* seed-level range;  
* exact sign or permutation summaries where meaningful.

A “four of five seeds in the same direction” pattern may be reported as an interpretive benchmark, not a success criterion.

## **Deliverables**

* seed-level statistics script;  
* paired-delta tables;  
* trajectory plots;  
* exact small-sample summaries.

## **Acceptance gate**

No result treats circuits within one model as independent experimental replications.

---

# **Stage 21 — Produce the principal figures**

## **Figure 1**

Training and test curves with all analysed checkpoint markers.

## **Figure 2**

Circuit-family dynamics across checkpoints and fidelity thresholds.

## **Figure 3**

Structural-overlap matrices and distinctness sensitivity.

## **Figure 4**

Functional-transfer matrices and transfer-distinct groups.

## **Figure 5**

Main grokking models versus random-label and matched no-generalisation controls.

Where space allows, include:

* full landmark dynamics;  
* paired seed trajectories;  
* empty-family outcomes;  
* search-failure information.

## **Deliverables**

* reproducible plotting scripts;  
* figure-source tables;  
* publication-ready figures;  
* complete captions;  
* explicit aggregation units.

## **Acceptance gate**

Every figure regenerates from saved result tables without retraining.

---

# **Stage 22 — Freeze the primary analysis**

## **Freeze**

* included seeds;  
* analysed checkpoints;  
* fidelity threshold;  
* threshold grid;  
* distinctness cutoff;  
* distinctness grid;  
* transfer-grouping rule;  
* controls;  
* matching rules;  
* statistical summaries;  
* figures.

## **Predictions table**

Do not rewrite it.

Instead:

* verify that the Stage 1 table is unchanged;  
* resolve each prediction against the observed result;  
* record any deviations or amendments.

## **Deliverables**

* final analysis manifest;  
* unchanged predictions table;  
* results-resolution table;  
* analysis-freeze commit;  
* exploratory-analysis register.

## **Acceptance gate**

The final interpretation is anchored to the predictions that existed before the results.

---

# **Stage 23 — Write the paper**

## **Order**

1. Methods.  
2. Results.  
3. Introduction and related work.  
4. Discussion.  
5. Limitations.  
6. Conclusion.  
7. Abstract.

## **Permitted conclusions**

* circuit-family collapse;  
* persistent non-identifiability;  
* mixed results separating compression, structural multiplicity, and functional interchangeability.

## **Prohibited overclaims**

Do not claim:

* complete enumeration of circuit space;  
* proof of one true mechanism;  
* proof that transfer-equivalent circuits are mechanistically identical;  
* strong condition-level inference from one control seed;  
* independent replication from every recovered circuit.

## **Deliverables**

* Methods draft;  
* Results draft;  
* complete first draft;  
* revised manuscript;  
* final figures and tables.

## **Acceptance gate**

Every claim remains within the evidence provided by the fixed-budget search, controls, sensitivity analyses, and seed count.

---

# **Stage 24 — Minimum reproducibility audit**

## **Required**

* one command regenerates tables and figures from saved results;  
* datasets and splits regenerate from config;  
* checkpoints trace to training configs;  
* saved circuits reload and reevaluate;  
* figure values trace to result tables;  
* manifests connect seeds, checkpoints, masks, and figures.

## **Deferred where necessary**

* complete retraining from a clean environment;  
* full OSF package;  
* comprehensive automated tests;  
* full dependency-lock audit.

## **Deliverables**

* analysis runner;  
* final README;  
* exact commands;  
* dataset manifest;  
* checkpoint manifest;  
* circuit manifest;  
* figure-generation instructions.

## **Acceptance gate**

The paper does not depend on undocumented notebook state or manual data editing.

---

# **Optional extension — Edge-level robustness**

Begin only after the component-level paper is complete.

Use selected checkpoints and a reduced analysis grid to test whether the main conclusion depends on defining circuits as heads and neurons rather than edges.

This extension must not delay the principal paper.

---

# **Final execution order**

Freeze predictions, definitions, statistical plan and sensitivity grids  
→ build minimal repository and data  
→ implement training and dense checkpointing  
→ train one grokking seed  
→ select full dynamics checkpoints  
→ implement masking and exact fidelity  
→ recover first sparse circuits  
→ run early Fourier sanity check  
→ calibrate and freeze primary fidelity threshold  
→ implement diversity-forced search  
→ validate search and project total compute  
→ freeze matched no-generalisation control  
→ run random-label control  
→ run no-generalisation control  
→ run transfer analysis  
→ run fidelity and distinctness sensitivity  
→ choose full or reduced dynamics grid prospectively  
→ scale across main seeds and controls  
→ run matched comparisons  
→ compute paired within-seed changes  
→ produce figures  
→ resolve the original predictions table  
→ freeze analysis  
→ write paper  
→ complete minimum reproducibility audit  
→ optional edge-level extension

## **Final integrity rules**

1. No reported diversity family is generated before the primary threshold is frozen.  
2. Pre-grokking circuit failure is allowed to remain a result.  
3. The predictions table is frozen before results exist.  
4. Family size is tested against both fidelity and distinctness thresholds.  
5. The dynamics claim uses multiple transition checkpoints.  
6. Random-label checkpoints are matched by training step.  
7. Empty families are reported as outcomes, not hidden as missing data.  
8. Primary inference uses paired within-seed changes.  
9. The full checkpoint grid may be reduced only prospectively and uniformly.  
10. Planning stops here; further methodological changes require a documented empirical reason.

---

# **Appendix: Eight-Week Triage Map**

| Week | Required stages | Minimum outcome by week-end |
| ----- | ----- | ----- |
| Week 1 | Stages 1–5 | Predictions and core definitions frozen; minimal repository, data generation, training and dense checkpointing operational |
| Week 2 | Stages 6–8 | First credible grokking run; phase checkpoints selected; component masking and fidelity evaluation validated |
| Week 3 | Stages 9–12 | First sparse circuits; Fourier sanity check; primary fidelity threshold frozen; diversity-forced search validated; total compute projected |
| Week 4 | Stages 13–17 | No-generalisation regime frozen; both controls run through the pipeline; transfer, fidelity and distinctness sensitivity piloted |
| Week 5 | Stage 18 | Main condition scaled across seeds using the prospectively chosen checkpoint grid; additional controls run where feasible |
| Week 6 | Stages 19–21 | Matched comparisons, paired seed-level summaries and principal figures completed |
| Weeks 7–8 | Stages 22–24 | Analysis frozen; paper written and revised; minimum reproducibility audit completed |

## **Schedule rule**

If a week-end minimum outcome is not reached, reduce only items classified as important-but-reducible or stretch work. Do not remove the diversity-forced search, controls, transfer analysis, sensitivity analysis or paired seed-level reporting to preserve the original schedule.

