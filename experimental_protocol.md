# **Experimental Protocol**

## **Circuit-Family Dynamics Across Grokking**

**Protocol version:** 1.0  
**Protocol initiated:** 13 July 2026  
**Protocol status:** Pre-results  
**Circuit-family results visible at initial freeze:** No  
**Primary implementation plan:** `implementation_order.md`
**Protocol-freeze Git commit:** 6ca148b7916e16d121edb4827948a7af73197db2

---

# **Protocol governance**

This document records the scientific and technical decisions governing the primary experiment.

Any decision described as frozen must not be changed after the result capable of influencing that decision becomes visible. Any later change must be:

1. dated;  
2. justified;  
3. entered in the amendment log;  
4. labelled as occurring before or after the relevant result became visible; and  
5. accompanied by regeneration of every affected reported result.

Any analysis or rule introduced after inspection of the relevant results will be labelled exploratory.

This protocol governs the machine-readable configuration files. Those files must reproduce the values recorded here. Once created, their file paths, hashes and Git commit will be entered in the protocol. A run whose configuration conflicts with this protocol is not eligible for the primary analysis.

The project is intended to establish what circuit families are recoverable under a fixed component definition, fidelity requirement, structural-distinctness rule, search procedure and computational budget. It does not claim to enumerate every possible circuit or identify a uniquely correct mechanism.

---

# **Part I — Scientific specification**

## **1\. Primary research question**

Under a fixed component-level circuit-recovery procedure, fidelity requirement, structural-distinctness criterion and search budget, how does the recoverable family of sparse circuits change as a transformer progresses from memorisation, through the grokking transition, to stable generalisation?

The study distinguishes between two forms of multiplicity:

1. **Structural multiplicity:** how many valid circuits can be recovered while satisfying a prespecified structural-distinctness rule.  
2. **Functional multiplicity:** how many recovered circuits display meaningfully different transfer profiles across prespecified subsets of the modular-addition task.

The study does not attempt to enumerate every possible circuit. All claims are restricted to circuits recoverable under the frozen search procedure, component definition and computational budget.

---

## **2\. Secondary research questions**

1. Does any change in circuit-family structure occur gradually during training, become concentrated around the rise in test performance, or appear only between pre- and post-grokking endpoints?  
2. Are post-grokking circuits smaller, more mutually overlapping or more functionally interchangeable than pre-grokking circuits?  
3. Is any apparent circuit-family contraction specific to successful generalisation, or can it also be produced by continued optimisation, weight decay, memorisation or generic compression?  
4. Does the conclusion survive reasonable variation in both the fidelity threshold and structural-distinctness cutoff?  
5. Does the conclusion remain after circuits are compared at approximately matched fidelity and approximately matched sparsity?  
6. Do structurally distinct circuits necessarily have different functional-transfer profiles?

---

## **3\. Competing hypotheses**

### **3.1 H1: Generalisation-associated circuit-family collapse**

As the model groks, the family of recoverable circuits becomes more constrained.

Expected evidence includes:

* lower recovered structural family size after grokking;  
* fewer transfer-distinct groups after grokking;  
* greater pairwise component overlap among recovered post-grokking circuits;  
* greater similarity among post-grokking transfer profiles;  
* concentration of successful circuits around a smaller shared component set; and  
* a substantial part of the change occurring around the rise in test performance rather than as undifferentiated training-time drift.

The strongest support for H1 would be a repeated decline in both primary endpoints around or after the generalisation transition, with the direction surviving reasonable sensitivity settings and not being reproduced by the matched controls.

### **3.2 H2: Persistent circuit non-identifiability**

Grokking does not collapse the recoverable circuit family to a narrow mechanistic solution.

Expected evidence includes:

* multiple structurally distinct circuits remaining recoverable after grokking;  
* no consistent decline in recovered structural family size across model seeds;  
* multiple transfer-distinct groups remaining after grokking;  
* low or heterogeneous overlap among post-grokking circuits;  
* persistent circuit-specific transfer profiles; and  
* matched-fidelity and matched-sparsity analyses continuing to show substantial multiplicity.

The strongest support for H2 would be persistent structural and functional multiplicity after stable generalisation across model seeds and reasonable sensitivity settings.

### **3.3 Mixed prediction**

Structural compression and mechanistic uniqueness need not coincide.

A mixed outcome may include:

* post-grokking circuits becoming smaller while multiple alternatives remain;  
* a larger common structural core accompanied by distinct peripheral components;  
* structural family size declining while remaining clearly greater than one;  
* functional multiplicity declining more strongly than structural multiplicity;  
* structural multiplicity declining without corresponding functional convergence; or  
* training-time compression occurring without being specifically linked to the generalisation transition.

Such results would support partial convergence, compression or functional interchangeability without supporting a claim of one uniquely identifiable circuit.

---

## **4\. Primary endpoints**

The study has two designated primary endpoints.

### **4.1 Primary endpoint 1: recovered structural family size**

For each model seed and analysed checkpoint, recovered structural family size is the number of valid sparse circuits found under:

* the frozen fidelity threshold;  
* the frozen structural-distinctness cutoff;  
* the frozen search procedure;  
* the frozen family target; and  
* the frozen search budget.

The primary comparison for each seed is:

**Change in structural family size \= post-grokking family size − pre-grokking family size**

A negative value indicates a smaller recovered family after grokking.

### **4.2 Primary endpoint 2: transfer-distinct group count**

For each non-empty recovered family, circuits are grouped using the frozen transfer-profile distance, clustering method and grouping tolerance.

The primary comparison for each seed is:

**Change in transfer-distinct group count \= post-grokking group count − pre-grokking group count**

This comparison is undefined when either the pre- or post-grokking circuit family is empty.

### **4.3 Headline interpretation rule**

The two primary endpoints must be interpreted jointly with:

* their paired direction within each seed;  
* their trajectories across transition checkpoints;  
* fidelity and distinctness sensitivity;  
* the random-label control; and  
* the matched no-generalisation control.

No secondary metric may independently determine the headline conclusion.

H1 may be the headline interpretation only when both primary endpoints show a coherent contraction, the conclusion does not depend on one isolated threshold setting, and the controls do not reproduce the same pattern.

H2 may be the headline interpretation only when meaningful structural and functional multiplicity persists after grokking and there is no coherent contraction across the primary endpoints.

Disagreement between the two primary endpoints produces a mixed result unless the discrepancy is explained by a prespecified rule for empty or otherwise degenerate cells.

Strong reversal across reasonable fidelity or distinctness settings is treated as fragility or an unresolved comparison. It is not evidence for H2.

No fixed significance threshold or fixed “four of five seeds” rule determines the conclusion. Sign consistency and the complete seed-level pattern must nevertheless be reported.

### **4.4 Empty-family transition rule**

An empty recovered family does not represent either maximal identifiability or maximal multiplicity. It indicates that no circuit satisfying the frozen fidelity, sparsity, search and budget requirements was recovered in that condition.

Accordingly, seeds involving an empty pre- or post-grokking family are classified separately from the ordinary H1/H2 directional tally:

* **Pre-grokking empty, post-grokking non-empty:** emergence of sparse recoverability after grokking.  
* **Pre-grokking non-empty, post-grokking empty:** loss of sparse recoverability after grokking.  
* **Both families empty:** persistent incompressibility under the frozen procedure.  
* **Both families non-empty:** eligible for the ordinary H1/H2 directional comparison.

Structural-family-size changes are still calculated and reported numerically, including changes from or to zero. However, a seed involving an empty endpoint is excluded from the sign tally used to assess circuit-family contraction or persistence, because the numerical direction does not have the same interpretation as a change between two non-empty families.

Transfer-distinct group count and other metrics requiring recovered circuits remain undefined wherever the relevant family is empty.

Empty-family transitions are interpreted using:

* the corresponding sensitivity curves;  
* search-failure classifications;  
* the size and transfer structure of any non-empty family;  
* and the matched control outcomes.

They are not automatically counted as support for either H1 or H2.

---

## **5\. Role of the controls**

### **5.1 Random-label control**

The random-label control tests whether changes in recovered circuit families can arise from:

* prolonged optimisation;  
* memorisation;  
* weight decay;  
* generic parameter compression; or  
* artefacts of the circuit-search procedure,

without a learnable modular-addition mapping.

Random-label checkpoints are matched to main-model checkpoints by training step rather than by test-accuracy landmark.

### **5.2 Matched no-generalisation control**

The matched no-generalisation control uses:

* the same modular-addition task;  
* the same architecture;  
* the same optimiser;  
* the same optimiser settings;  
* the same weight decay;  
* the same checkpoint procedure; and  
* the same circuit-search pipeline,

but a prespecified lower training-data fraction under which the model memorises the training data without undergoing the corresponding generalisation transition within the matched training budget.

The regime is selected using training and test curves only. No circuit-family metric may be inspected during control selection.

### **5.3 Control-attribution logic**

Control outcomes determine attribution rather than directly supporting H2.

If a control reproduces the main model’s apparent circuit-family contraction, the contraction cannot be attributed specifically to successful generalisation without further evidence.

If the controls do not reproduce the contraction, attribution to the grokking transition is strengthened.

A control reproducing the main effect weakens H1 but does not by itself establish persistent multiplicity in the main model.

One control seed permits only descriptive comparison. Seed-level inferential language about controls requires multiple control seeds.

---

## **6\. Frozen prediction table**

| Quantity | H1 prediction | H2 prediction | Mixed or unresolved interpretation |
| ----- | ----- | ----- | ----- |
| Recovered structural family size | Declines around or after grokking | Remains substantial and shows no coherent decline | Declines but remains greater than one, or varies inconsistently |
| Transfer-distinct group count | Declines around or after grokking | Multiple functional groups persist without coherent decline | Structural and functional multiplicity change differently |
| Circuit size | Generally decreases after grokking | No consistent change required | Compression occurs without removal of alternatives |
| Pairwise structural overlap | Increases after grokking | Remains low or heterogeneous | A larger common core coexists with distinct peripheral components |
| Cross-subset transfer | Becomes more similar across circuits | Remains strongly circuit-dependent | Mean transfer improves while circuit-specific differences remain |
| Timing of change | The largest contraction is concentrated near the transition landmarks | No transition-linked contraction; multiplicity persists | Gradual training-time drift or endpoint-only change |
| Matched-fidelity result | Post-grokking multiplicity remains lower | Substantial multiplicity persists after matching | Unequal fidelity explained part of the apparent effect |
| Matched-sparsity result | Post-grokking circuits remain more constrained or interchangeable | Substantial multiplicity persists after matching | Unequal circuit size explained part of the apparent effect |
| Empty-family transition   | Classified separately as emergence or loss of sparse recoverability | Classified separately as emergence or loss of sparse recoverability  | Not scored directionally as H1 or H2; interpreted using sensitivity, diagnostics and controls |

### **Control interpretation table**

| Control result | Interpretation |
| ----- | ----- |
| Random-label control reproduces the main contraction | The effect may reflect optimisation, memorisation, regularisation or search behaviour rather than generalisation |
| Random-label control does not reproduce the main contraction | Generic optimisation and memorisation explanations are weakened |
| No-generalisation control reproduces the main contraction | The effect may reflect training-time or compression dynamics rather than the generalisation transition |
| No-generalisation control does not reproduce the main contraction | Attribution to successful generalisation is strengthened |
| Controls are unstable or only one seed is available | Control comparison remains descriptive and attribution remains limited |

---

## **7\. Prediction-resolution categories**

At the final analysis stage, each prediction will be classified as:

* **Supported**  
* **Partly supported**  
* **Unsupported**  
* **Contradicted**  
* **Unresolved**

A prediction is unresolved when:

* the direction reverses across reasonable sensitivity settings;  
* the necessary circuit family is empty;  
* the required matched comparison cannot validly be made;  
* search failure prevents the relevant comparison;  
* control behaviour is indeterminate; or  
* the available seed count is insufficient for the intended claim.

The predictions table will not be rewritten after results become visible.

---

# **Part II — Frozen technical specification**

## **8\. Task**

### **8.1 Primary task**

The task is modular addition:

**c \= (a \+ b) mod 113**

where both operands are integers from 0 to 112\.

The complete input universe contains 12,769 ordered operand pairs.

### **8.2 Input representation**

Each example is represented by the token sequence:

`[a, b, =]`

where:

* `a` is one of 113 operand tokens;  
* `b` is one of 113 operand tokens;  
* `=` is a separate special token; and  
* the model predicts the answer at the final token position.

The input vocabulary contains 114 tokens.

The output vocabulary contains the 113 possible residue classes.

The target for each example is:

`(a + b) % 113`

### **8.3 Loss and accuracy**

Training loss is categorical cross-entropy on the output logits at the final sequence position.

Training and test accuracy are top-one classification accuracy.

No loss is applied to the first two sequence positions.

---

## **9\. Dataset generation and split**

### **9.1 Ordered input generation**

All operand pairs are generated in lexicographic order:

(0, 0), (0, 1), ..., (0, 112),  
(1, 0), ..., (112, 112\)

The correct label table is generated deterministically.

### **9.2 Primary train/test split**

A deterministic random permutation of the 12,769 pair indices is generated using:

* NumPy generator: PCG64  
* Split seed: 0

The primary training set contains the first 3,830 permuted pairs, corresponding to 30% of the full dataset rounded down.

The remaining 8,939 pairs form the test set.

The split is held fixed across all main model seeds.

No validation set is used for hyperparameter tuning after results become visible.

### **9.3 Nested training fractions**

Candidate lower training fractions for the matched no-generalisation control are derived from the same fixed permutation.

The candidate grid is:

* 5%  
* 10%  
* 15%  
* 20%  
* 25%

Each candidate training set is the corresponding prefix of the same permuted ordering.

This creates nested training sets and prevents the control-selection process from changing both the data fraction and the random split.

### **9.4 Dataset records**

The following must be saved:

* modulus;  
* complete ordered-pair table;  
* true-label table;  
* split seed;  
* permutation;  
* training indices;  
* test indices;  
* dataset hash;  
* split hash; and  
* software version used for generation.

Regenerating the dataset from the same configuration must reproduce the same hashes.

---

## **10\. Random-label dataset**

The random-label control uses the same 12,769 input pairs and the same 30% train/test split as the primary task.

Random labels are generated by applying a deterministic random permutation to the complete vector of true modular-addition labels.

This preserves exact global class balance: each of the 113 output classes occurs exactly 113 times.

The random-label permutation uses:

* NumPy generator: PCG64  
* Random-label seed: 1

The resulting label assigned to each input pair is frozen before training.

Labels are not regenerated between model seeds.

The random-label table and its hash must be saved.

---

## **11\. Primary model architecture**

The primary model is a one-layer decoder-only transformer.

### **11.1 Frozen architecture**

| Setting | Value |
| ----- | ----- |
| Transformer layers | 1 |
| Context length | 3 |
| Model width | 128 |
| Attention heads | 4 |
| Head dimension | 32 |
| MLP hidden width | 512 |
| Activation function | ReLU |
| Positional embeddings | Learned |
| Attention mask | Causal |
| Layer normalisation | None |
| Dropout | None |
| Embedding/unembedding tying | None |
| Input vocabulary size | 114 |
| Output vocabulary size | 113 |

The model reads the answer logits at the final token position.

### **11.2 Fixed non-searchable structures**

The following remain part of every masked model and are not independently searched in the primary component analysis:

* operand embeddings;  
* the `=` embedding;  
* positional embeddings;  
* attention projection matrices within retained heads;  
* MLP input and output weights within retained neurons;  
* residual connections;  
* unembedding weights; and  
* output biases, where present.

### **11.3 Implementation authority**

The intended implementation uses TransformerLens unless it proves technically incompatible with the required neuron-level masking.

Before the first training run, record:

* Python version;  
* PyTorch version;  
* TransformerLens version or commit;  
* complete model configuration;  
* parameter count;  
* bias configuration;  
* initialisation configuration;  
* device; and  
* numerical precision.

Low-level library defaults are frozen through the pinned package version and saved configuration. They may not silently change between seeds.

---

## **12\. Optimisation**

### **12.1 Primary optimiser**

| Setting | Value |
| ----- | ----- |
| Optimiser | AdamW |
| Learning rate | 0.001 |
| Beta 1 | 0.9 |
| Beta 2 | 0.98 |
| Epsilon | 0.00000001 |
| Weight decay | 1.0 |
| Learning-rate schedule | Constant |
| Warm-up | None |
| Gradient clipping | None |
| Batch size | Full training set |
| Numerical precision | Float32 |

Weight decay is applied using the implementation’s decoupled AdamW rule.

All main and control conditions use the same optimiser settings and weight decay.

### **12.2 Training step**

Because training is full batch, one epoch equals one optimiser update and one training step.

### **12.3 Training horizon**

The standard training horizon is 40,000 steps.

No early stopping is used.

If a main seed has not reached the stable post-grokking criterion by 40,000 steps, training continues without changing any hyperparameter in increments of 10,000 steps, up to an absolute maximum of 80,000 steps.

A seed that has not reached stable post-grokking by 80,000 steps is recorded as a failed-to-grok main run and is not silently discarded.

Replacement seeds, where required to obtain five complete grokking seeds, are taken in ascending order from the prespecified reserve-seed list.

### **12.4 Numerical failures**

A run is stopped only for:

* non-finite loss;  
* non-finite parameters;  
* corrupted checkpoint output; or  
* confirmed implementation failure.

Numerical failure does not permit informal hyperparameter retuning. Any corrective change requires a dated pre-results amendment and rerunning all affected conditions.

---

## **13\. Seed definitions**

### **13.1 Main model seeds**

The primary main-model seeds are:

`0, 1, 2, 3, 4`

The reserve seeds are:

`5, 6, 7, 8, 9`

A model seed controls:

* parameter initialisation;  
* model-internal stochasticity; and  
* any other training randomness.

The train/test split remains fixed across model seeds.

The independently trained model seed is the independent unit for the primary analysis.

### **13.2 Control seeds**

The minimum control implementation uses model seed 0\.

Additional control seeds, if resources permit, use seeds 1, 2, 3 and 4 in ascending order.

### **13.3 Search seeds**

Search outputs are not independent experimental units.

Where a search procedure requires random tie-breaking or restarts, its seed is deterministically derived from:

* model seed;  
* checkpoint index;  
* family-member index; and  
* restart index.

The complete derived search seed is stored in the circuit manifest.

---

## **14\. Logging and dense checkpointing**

### **14.1 Evaluation interval**

Training and test metrics are evaluated every 50 training steps, including step 0\.

### **14.2 Checkpoint interval**

A complete model checkpoint is saved every 50 training steps, including step 0 and the final step.

### **14.3 Recorded metrics**

At every evaluation point, record:

* training step;  
* train cross-entropy;  
* test cross-entropy;  
* train accuracy;  
* test accuracy;  
* learning rate;  
* total parameter norm;  
* gradient norm where practical;  
* checkpoint path;  
* elapsed wall time; and  
* device information.

### **14.4 Checkpoint integrity**

Each checkpoint must store or link to:

* model state;  
* optimiser state;  
* model configuration;  
* training configuration;  
* model seed;  
* dataset and split hashes;  
* code commit;  
* metric record; and  
* checkpoint hash.

Reloading a checkpoint must reproduce its saved train and test metrics within numerical tolerance.

---

## **15\. Grokking eligibility and phase definitions**

### **15.1 Credible grokking run**

A main run is eligible as a complete grokking seed only if it shows:

1. training accuracy reaching at least 99.9%;  
2. a period after memorisation during which test accuracy remains below 10%;  
3. a later rise in test accuracy; and  
4. stable test accuracy of at least 99%.

A run in which training and test accuracy rise together without a discernible delayed-generalisation interval is not classified as a grokking run for the primary analysis.

### **15.2 Pre-grokking checkpoint**

The pre-grokking checkpoint is the latest saved checkpoint satisfying:

* training accuracy of at least 99.9%; and  
* test accuracy of at most 5%,

before the first saved checkpoint at which test accuracy reaches or exceeds 10%.

If no checkpoint satisfies this rule, the run does not contain a valid primary pre-grokking landmark.

### **15.3 Transition landmarks**

The preferred transition landmarks are:

* 10% test accuracy;  
* 25% test accuracy;  
* 50% test accuracy;  
* 75% test accuracy; and  
* 90% test accuracy.

For each target, select the saved checkpoint between the pre-grokking and stable post-grokking checkpoints whose test accuracy is nearest to the target.

Ties are resolved in favour of the earlier training step.

For each landmark, record:

* target accuracy;  
* achieved accuracy;  
* absolute difference from the target;  
* training step; and  
* checkpoint path.

### **15.4 Stable post-grokking checkpoint**

Stable post-grokking is reached at the fifth checkpoint in the earliest sequence of five consecutive saved checkpoints with test accuracy of at least 99%.

The selected stable post-grokking checkpoint is the fifth checkpoint in that sequence.

### **15.5 Dynamic grid**

The preferred full grid is:

* pre-grokking;  
* 10%;  
* 25%;  
* 50%;  
* 75%;  
* 90%; and  
* stable post-grokking.

The pilot main seed is analysed using the full grid.

After the Stage 12 compute projection, scaled seeds use either:

* the full grid; or  
* the uniformly reduced grid consisting of pre-grokking, 50% and stable post-grokking.

The choice must be made before scaled family results are generated and applied uniformly to all scaled main seeds.

The full grid may not be used selectively only for convenient seeds.

---

## **16\. Primary searchable components**

The primary component universe contains:

* four complete attention heads; and  
* 512 individual MLP neurons.

The total number of searchable components is therefore 516\.

### **16.1 Attention-head masking**

A head mask multiplies the complete output contribution of the relevant attention head by either zero or one before it enters the residual stream.

A retained head has mask value one.

An ablated head has mask value zero.

### **16.2 MLP-neuron masking**

A neuron mask multiplies the post-ReLU activation of the individual neuron by either zero or one before multiplication by the MLP output matrix.

A retained neuron has mask value one.

An ablated neuron has mask value zero.

### **16.3 Primary ablation baseline**

The primary intervention is zero ablation.

Mean ablation may be examined only as a separately labelled robustness analysis and does not replace the primary zero-ablation result.

### **16.4 Circuit representation**

A circuit is stored as:

* a four-element binary attention-head mask;  
* a 512-element binary MLP-neuron mask;  
* a combined ordered list of retained component indices;  
* retained-component count;  
* retained-component proportion;  
* checkpoint identifier;  
* discovery set;  
* fidelity threshold;  
* distinctness cutoff;  
* search seed;  
* search-budget use; and  
* all evaluation metrics.

---

## **17\. Masking acceptance tests**

Before any search result is accepted, the masking implementation must pass the following tests:

1. all components retained;  
2. all components ablated;  
3. one attention head ablated;  
4. one MLP neuron ablated;  
5. arbitrary saved mask reloaded;  
6. repeated evaluation of the same mask; and  
7. component-index mapping.

The all-retained mask must reproduce the full model’s logits within numerical tolerance.

The all-retained top-one predictions must match exactly.

---

## **18\. Fidelity definition**

### **18.1 Primary behavioural fidelity**

Primary fidelity is the proportion of examples on which the masked model and the corresponding full checkpoint produce the same top-one prediction.

In plain terms:

**Fidelity \= number of matching predictions ÷ total number of evaluated examples**

### **18.2 Primary global evaluation set**

For the primary circuit-family analysis, fidelity is evaluated on all 12,769 ordered input pairs.

This includes both training and test inputs.

The aim is to preserve the checkpoint’s complete learned function, including memorised behaviour, rather than to reward only ground-truth generalisation.

### **18.3 Secondary fidelity metrics**

Every circuit evaluation also reports:

* ground-truth accuracy;  
* cross-entropy against the true labels;  
* mean KL divergence from the full-model output distribution;  
* mean Jensen–Shannon divergence where practical;  
* full-model confidence on retained predictions;  
* masked-model confidence;  
* retained-component count; and  
* retained-component proportion.

These secondary metrics do not replace the primary top-one agreement threshold.

### **18.4 Exact evaluation rule**

Approximate attribution or first-order scores may rank candidate removals.

Every accepted removal and every reported circuit must be evaluated through an exact forward pass over the complete relevant evaluation set.

---

## **19\. Sparse-circuit definition**

A reported primary circuit must satisfy:

1. the applicable fidelity threshold;  
2. the fixed component definition;  
3. exact evaluation; and  
4. the primary sparsity requirement.

A circuit is meaningfully sparse when it retains no more than 50% of the 516 searchable components.

The maximum retained-component count is therefore 258\.

The all-retained mask is not counted as a recovered sparse circuit.

A condition in which no circuit satisfying the fidelity and sparsity requirements is recovered has recovered family size zero.

The 50% rule is primary and is frozen before threshold calibration.

Alternative sparsity cutoffs may be reported only as sensitivity analyses.

---

## **20\. Fidelity-threshold grid**

The frozen fidelity-threshold grid is:

* 80%  
* 85%  
* 90%  
* 95%  
* 97.5%  
* 99%

The grid is frozen before calibration.

The actual primary threshold is not selected at protocol initiation. It is selected at Stage 11 using only the permitted calibration information described below.

---

## **21\. Primary fidelity-threshold calibration**

### **21.1 Permitted calibration evidence**

The primary threshold may use only:

* the first stable post-grokking checkpoint of the pilot seed;  
* the first post-grokking sparse-search result at each candidate threshold;  
* exact fidelity;  
* retained-component proportion;  
* matched-size random-mask pass rate;  
* the early Fourier-style sanity check;  
* search evaluation count; and  
* measured computational feasibility.

### **21.2 Prohibited calibration evidence**

The threshold must not use:

* pre-to-post family-size differences;  
* pre-to-post circuit-size differences;  
* transition family results;  
* diversity-forced family counts;  
* random-label family results;  
* no-generalisation family results;  
* across-seed family results; or  
* the threshold that maximises the apparent primary effect.

Pre-grokking or transition sparse-search outputs may exist for implementation checking, but they may not enter the threshold-selection justification.

### **21.3 Random-mask calibration**

For each candidate threshold, generate 100 uniformly sampled random masks matched exactly to the retained-component count of the pilot post-grokking sparse circuit.

Random-mask sampling uses a frozen derived seed and samples without replacement from the 516 searchable components.

Record:

* number passing the fidelity threshold;  
* pass proportion;  
* fidelity distribution; and  
* random-mask seed.

### **21.4 Calibration criteria**

A candidate threshold qualifies only if:

1. the post-grokking search recovers a circuit retaining no more than 258 components;  
2. no more than 5 of the 100 matched-size random masks pass;  
3. the recovered circuit is compatible with the Fourier-style diagnostic, or any mismatch has been satisfactorily explained; and  
4. the search remains within the frozen pilot search budget.

### **21.5 Threshold-selection rule**

Evaluate candidate thresholds from highest to lowest.

Select the highest threshold satisfying every calibration criterion.

If no threshold qualifies, no primary threshold is selected automatically. The failure must be recorded, and any methodological correction must occur through a dated pre-family amendment before any reported diversity-family result is generated.

### **21.6 Freeze rule**

**Frozen Stage 11 result — 18 July 2026:** the primary behavioural-fidelity threshold is **0.990000** (exactly 99/100).

The threshold was selected mechanically as the highest candidate satisfying every prespecified calibration criterion. All six candidate thresholds qualified. At each threshold, zero of the 100 matched-size random masks passed. The selected 0.990000 candidate retained 146 of 516 searchable components, remained within the 10,000 exact-evaluation budget, and was classified as a clear match by the frozen Fourier diagnostic.

The calibration used the pilot seed's stable post-grokking checkpoint at training step 9,050. Its definitive run identifier is `stage11-calibration-s1-c2856467c00f`; its implementation commit is `c2856467c00f47b9baa28ed866b7295b0ac5f3ff`; and its scientific-artifact commit is `e224c5f06909e0d6ad826c54b58c7770bb97a6d3`. An independent detached-worktree reproduction matched all four deterministic scientific artifacts and all 600 raw mask records byte-for-byte.

No diversity-forced family output existed before this freeze. The excluded-development-output register therefore contains its required header and zero data rows.

After selecting the threshold:

* record it in this protocol;  
* record the calibration table;  
* record the Git commit and timestamp;  
* record every excluded method-development output; and  
* regenerate all reported family-search results from scratch.

---

## **22\. Structural distinctness**

### **22.1 Primary metric**

Structural overlap between two circuits is measured using Jaccard similarity:

**Jaccard overlap \= number of components shared by both circuits ÷ number of components present in either circuit**

Attention heads and MLP neurons are treated as elements of one combined 516-component universe.

### **22.2 Primary cutoff**

The primary maximum pairwise overlap is 0.50.

A newly recovered circuit is structurally distinct only if its Jaccard overlap with every previously accepted circuit is no greater than 0.50.

The requirement applies to the maximum pairwise overlap, not the mean overlap.

### **22.3 Sensitivity cutoffs**

The frozen structural-distinctness sensitivity grid is:

* 0.25  
* 0.50  
* 0.75

Lower values impose stricter distinctness.

### **22.4 Interpretation**

Structural distinctness does not imply mechanistic or functional distinctness.

Recovered structural family size is explicitly conditional on the selected Jaccard cutoff.

---

## **23\. Primary sparse-search procedure**

### **23.1 Search objective**

The search seeks a sparse component mask that preserves the full checkpoint’s predictions.

For attribution ranking, the target for each example is the full model’s top-one prediction.

The ranking loss is cross-entropy between the masked-model logits and those frozen full-model predictions.

### **23.2 Greedy removal**

For each search:

1. begin with every component retained;  
2. calculate a first-order component-removal score using the gradient of the prediction-preservation loss with respect to component gates;  
3. rank retained components from least to most damaging;  
4. break exact score ties using the fixed component index;  
5. exactly evaluate candidate removals in ordered batches of 16;  
6. identify the first candidate batch containing at least one valid removal;  
7. within that batch, remove the candidate producing the highest exact fidelity;  
8. break any remaining tie using the lower component index;  
9. recompute the ranking after every accepted removal; and  
10. continue until no valid single-component removal remains or the search budget is exhausted.

Approximate ranking determines which candidates are tested first.

Exact forward evaluation determines whether a removal is accepted.

### **23.3 Terminal deletion check**

Where the search budget has not been exhausted, the terminal iteration must test every remaining component for single deletion before declaring that no further valid deletion is available.

### **23.4 Output status**

Each search receives one of the following statuses:

* valid sparse circuit;  
* fidelity failure;  
* sparsity failure;  
* optimiser or search failure;  
* budget exhaustion;  
* invalid masking output; or  
* no feasible sparse candidate discovered within budget.

---

## **24\. Diversity-forced family search**

### **24.1 Sequential family construction**

For each checkpoint and parameter setting:

1. recover the first sparse circuit;  
2. recover the second circuit while penalising reuse of components in the first;  
3. recover the third circuit while penalising reuse across the first two;  
4. continue sequentially until the family target, failure rule or budget limit is reached.

Every accepted circuit must independently satisfy:

* exact fidelity;  
* the primary sparsity requirement; and  
* the applicable maximum pairwise Jaccard-overlap cutoff.

### **24.2 Primary reuse cost**

For each component, calculate how frequently it appears in the previously accepted circuits.

Convert the estimated fidelity-damage scores to percentile ranks between 0 and 1\.

The diversity-forced removal score is:

**Removal score \= damage percentile − 0.5 × previous reuse rate**

Components with lower scores are tested for removal first.

This means that frequently reused components are preferentially considered for removal, while exact fidelity remains the acceptance criterion.

### **24.3 Restarts**

For each requested alternative circuit, use up to five deterministic restarts.

Restarts use the frozen derived search-seed rule.

A small seeded tie-breaking perturbation may alter the order of candidates with numerically indistinguishable ranking scores but may not alter the exact acceptance criteria.

When multiple valid distinct candidates are found, choose them in this order:

1. fewer retained components;  
2. higher fidelity; and  
3. lower restart index.

### **24.4 Failure to find another circuit**

If all five restarts fail to produce another valid structurally distinct circuit within the remaining budget, family construction stops.

The stopping reason is recorded as:

* fidelity failure;  
* distinctness failure;  
* sparsity failure;  
* search failure; or  
* budget exhaustion.

Failure to find another circuit is not interpreted as proof that no other circuit exists.

---

## **25\. Search budget**

### **25.1 Budget unit**

One exact mask evaluation is one complete evaluation of a candidate component mask over the applicable discovery set.

Candidate masks may be evaluated in computational batches, but each candidate counts separately.

Approximate gradient-ranking passes are recorded separately.

### **25.2 Per-circuit budget**

The maximum per requested circuit is 10,000 exact mask evaluations.

### **25.3 Per-cell budget**

The maximum for one combination of checkpoint, fidelity threshold and distinctness cutoff is 50,000 exact mask evaluations.

### **25.4 Family target**

The maximum requested family size is ten circuits.

The reported family size is therefore a fixed-budget recovered family size capped at ten.

A family reaching ten is right-censored by the family target and must be labelled accordingly.

### **25.5 Uniformity**

The same budget applies to:

* pre-grokking checkpoints;  
* transition checkpoints;  
* post-grokking checkpoints;  
* random-label controls;  
* no-generalisation controls;  
* all model seeds; and  
* every primary sensitivity setting.

Unused budget is not transferred between conditions.

### **25.6 Pilot revision rule**

The Stage 12 compute projection may reveal that the frozen budget is technically unusable.

A budget change is permitted only:

* before scaled or control family results are inspected;  
* through a dated amendment;  
* using runtime and evaluation-count evidence rather than scientific outcomes; and  
* with regeneration of all reported family results under the revised uniform budget.

---

## **26\. Early Fourier-style sanity check**

At the pilot stable post-grokking checkpoint, examine whether:

* embeddings show concentrated Fourier structure;  
* retained components are associated with frequencies used by the model;  
* the recovered sparse circuit preserves relevant Fourier structure; and  
* ablating retained relevant components damages the expected behaviour.

This check is a pipeline diagnostic.

It is not used as proof of uniqueness.

A mismatch triggers investigation of:

* checkpoint identity;  
* component indexing;  
* masking;  
* logits;  
* fidelity computation;  
* search objective;  
* distributed representations; or  
* a legitimate alternative implementation.

The diagnostic may enter threshold calibration only as a check against a clearly broken recovery pipeline.

---

## **27\. Matched no-generalisation control selection**

### **27.1 Candidate grid**

Train one pilot model at each nested training fraction:

* 5%  
* 10%  
* 15%  
* 20%  
* 25%

Use model seed 0 and leave all other primary training settings unchanged.

### **27.2 Selection criteria**

A candidate regime qualifies if:

1. training accuracy reaches at least 99.9% by step 5,000;  
2. training accuracy remains at least 99.9% at no fewer than 90% of subsequent evaluation checkpoints;  
3. test accuracy never exceeds 10% during the required matched training horizon;  
4. the difference between mean test accuracy over the final 1,000 steps and the preceding 1,000 steps is no greater than two percentage points; and  
5. test cross-entropy falls by no more than 10% over the final 5,000 steps.

These rules use only training and test curves.

### **27.3 Selection rule**

Choose the largest training fraction satisfying all criteria.

This maximises data coverage while retaining a no-generalisation regime.

If no candidate qualifies, record the control-selection failure. No new fraction may be introduced after circuit-family results become visible.

### **27.4 Horizon validation**

The selected regime must remain qualifying through the largest main-model landmark step to which it will be matched.

If it begins generalising before that step, move to the next lower fraction according to the same prespecified rule, using curves only and before inspecting circuit results.

### **27.5 Matching**

For each main-model landmark, select the no-generalisation checkpoint at the same training step.

If that exact step was not saved, use the nearest saved checkpoint and record the absolute step difference.

Test-accuracy landmarks are not used for matching.

---

## **28\. Random-label checkpoint matching**

The random-label model is trained for at least as many steps as the largest selected main-model landmark.

For every main-model checkpoint, use the random-label checkpoint at:

* the same saved training step; or  
* the nearest available saved step.

Record any step mismatch.

The random-label control receives the same component definition, search procedure, family target and search budget.

### **28.1 Random-label memorisation criterion**

For the random-label run to serve as a control for prolonged optimisation, memorisation and weight decay, it must reach at least 99% training accuracy by the end of the training horizon required for step matching to the main model.

Its complete training-accuracy trajectory must be recorded regardless of whether this criterion is met.

If the random-label model does not reach 99% training accuracy within the matched horizon:

* the run is retained and reported;  
* it is labelled an **optimisation-only control** rather than a successful memorisation control;  
* it may inform whether training time, weight decay or the search procedure alone reproduce the main pattern;  
* but it may not be used to rule in or rule out an explanation specifically based on memorisation.

The model is not retuned solely to force memorisation after circuit-family results become visible. Any pre-results correction to a demonstrably failed implementation must be documented through the amendment procedure.

---

## **29\. Transfer subsets**

### **29.1 Primary transfer partition**

Define the lower operand range as 0 to 56 and the higher operand range as 57 to 112\.

The four primary transfer subsets are:

* **Q1:** both operands are in the lower range;  
* **Q2:** the first operand is in the lower range and the second is in the higher range;  
* **Q3:** the first operand is in the higher range and the second is in the lower range;  
* **Q4:** both operands are in the higher range.

These subsets are fixed before circuit results are inspected.

### **29.2 Transfer-profile evaluation**

For every circuit in a globally discovered family, evaluate its prediction agreement with the full model separately on Q1, Q2, Q3 and Q4.

The circuit’s transfer profile is the resulting four-value vector.

### **29.3 Subset-discovery analysis**

As a secondary analysis:

1. discover a circuit using Q1 only;  
2. transfer it unchanged to Q2, Q3 and Q4;  
3. repeat with each subset as the discovery subset; and  
4. construct the discovery-to-evaluation transfer matrix.

Subset-discovered circuits must satisfy the fidelity threshold on their own discovery subset.

Their performance elsewhere is not constrained.

### **29.4 Additional descriptive subsets**

The following may be used descriptively but do not replace the primary four-subset partition:

* diagonal inputs, where the operands are equal;  
* off-diagonal inputs, where the operands differ;  
* output-residue groups; and  
* balanced fixed random partitions.

Any result introduced from these subsets after inspection of the primary transfer results is exploratory unless the analysis was implemented before those results became visible.

---

## **30\. Transfer-distinct group count**

### **30.1 Distance**

The distance between two circuits’ transfer profiles is the largest absolute difference between their fidelity values across Q1, Q2, Q3 and Q4.

### **30.2 Clustering**

Use deterministic complete-linkage hierarchical clustering.

The primary grouping tolerance is 0.05.

Every pair of circuits placed in the same cluster must therefore have complete-linkage distance no greater than 0.05.

### **30.3 Sensitivity tolerances**

The transfer-grouping sensitivity grid is:

* 0.025  
* 0.050  
* 0.100

### **30.4 Empty and singleton families**

If structural family size is zero, transfer-distinct group count is undefined.

If structural family size is one, transfer-distinct group count is one.

Transfer-distinct groups are not described as the true number of mechanisms.

---

## **31\. Two-dimensional sensitivity analysis**

For every analysed checkpoint, report recovered structural family size across all combinations of the frozen fidelity and distinctness settings.

The fidelity settings are:

* 80%  
* 85%  
* 90%  
* 95%  
* 97.5%  
* 99%

The structural-distinctness cutoffs are:

* 0.25  
* 0.50  
* 0.75

At minimum, report:

* family size against fidelity at several distinctness cutoffs;  
* family size against distinctness at several fidelity thresholds;  
* a two-dimensional family-size table or heatmap;  
* search-failure rates;  
* family-target censoring;  
* circuit-size summaries;  
* transfer-distinct group counts where defined; and  
* empty-family outcomes.

The primary conclusion must not be justified solely by the one setting that produces the largest pre-to-post difference.

A qualitative reversal across reasonable neighbouring settings is treated as sensitivity fragility and may make the headline comparison unresolved.

---

## **32\. Matched comparisons**

Matched comparisons are secondary.

### **32.1 Matched fidelity**

Within a seed and checkpoint comparison, circuits may be matched only if their exact global fidelity differs by no more than 0.01, or one percentage point.

Use one-to-one matching without replacement, minimising the total absolute fidelity difference.

Report unmatched circuits.

### **32.2 Matched sparsity**

Circuits may be matched only if their retained-component counts differ by no more than five components.

Use one-to-one matching without replacement, minimising the total absolute size difference.

Report unmatched circuits.

### **32.3 Degenerate cells**

Matched comparisons are reported only when both relevant conditions contain valid circuits satisfying the matching tolerance.

No circuit is imputed into an empty family.

Failure to form a match is reported directly.

---

# **Part III — Statistical analysis plan**

## **33\. Independent unit**

The independently trained model seed is the independent unit.

Recovered circuits within one model are not independent experimental replications.

Search restarts are not independent replications.

Checkpoints within one model form a repeated trajectory.

---

## **34\. Primary paired comparisons**

For every model seed, calculate the following changes.

### **34.1 Pre- to post-grokking**

**Change \= post-grokking value − pre-grokking value**

### **34.2 Pre-grokking to each transition checkpoint**

**Change \= transition-checkpoint value − pre-grokking value**

### **34.3 Transition checkpoint to post-grokking**

**Change \= post-grokking value − transition-checkpoint value**

### **34.4 Adjacent landmarks**

**Change \= value at the later landmark − value at the preceding landmark**

These comparisons may be calculated for:

* recovered structural family size;  
* transfer-distinct group count;  
* median pairwise overlap;  
* median circuit size;  
* mean transfer score;  
* matched-fidelity diversity; and  
* matched-sparsity fidelity.

---

## **35\. Primary summaries**

For every primary and secondary metric, report:

* raw values for each seed;  
* raw seed trajectories;  
* paired changes;  
* number of positive, negative and zero changes;  
* sign consistency;  
* median paired change;  
* mean paired change where useful;  
* full seed-level range; and  
* exact sign or permutation reasoning where meaningful.

With five main seeds:

* bootstrap confidence intervals do not carry the main argument;  
* conventional significance thresholds do not determine the conclusion; and  
* circuits are not pooled as though independently sampled.

A “four of five seeds in the same direction” pattern may be described as an interpretive benchmark, but it is not a prespecified binary success criterion.

---

## **36\. Empty-family handling**

Recovered structural family size is zero when no valid sparse circuit family is recovered under the fixed search procedure and budget.

Family-size changes are calculated normally using zero.

Metrics requiring one or more circuits are undefined when the relevant family is empty. These include:

* median circuit size;  
* median pairwise overlap;  
* transfer-distinct group count;  
* transfer-profile dispersion;  
* matched-fidelity results; and  
* matched-sparsity results.

Undefined values are not converted to zero.

They are excluded from comparisons requiring that metric.

The empty-family outcome remains included in:

* family-size analysis;  
* threshold curves;  
* search-failure analysis; and  
* the seed-level results table.

---

## **37\. Family-target censoring**

A family reaching the maximum of ten circuits is recorded as:

**Family size at least 10**

The stored recovered count remains ten, but the result is explicitly marked as capped.

A pre-to-post comparison involving a capped family is interpreted cautiously because the true recoverable family may be larger.

Sensitivity analyses may not silently treat ten as an uncensored exact family size.

---

## **38\. Control analysis**

With one control seed, control results are descriptive.

Where multiple control seeds are completed, apply the same paired seed-level summaries used for the main models.

Control circuits are never pooled to create artificial replication.

The controls are used to evaluate whether the main pattern is attributable specifically to successful generalisation.

---

## **39\. Timing analysis**

The dynamics claim is evaluated using:

* the full landmark trajectory in the pilot seed;  
* the uniformly selected grid across scaled seeds;  
* changes between adjacent landmarks; and  
* comparison with step-matched controls.

A transition-linked change should appear as a concentration of changes around the accuracy landmarks.

A smooth monotonic change with training step that is also present in the step-matched controls is interpreted as generic training-time or compression dynamics rather than a grokking-specific transition.

An endpoint difference alone cannot support a strong dynamics claim.

---

# **Part IV — Reporting and integrity**

## **40\. Required result records**

Every reported circuit must trace to:

* dataset hash;  
* split hash;  
* label-table hash;  
* model seed;  
* training configuration;  
* checkpoint hash;  
* checkpoint metrics;  
* component definition;  
* fidelity threshold;  
* distinctness cutoff;  
* transfer tolerance;  
* search seed;  
* search budget;  
* code commit;  
* circuit mask;  
* exact evaluation results; and  
* output-file hash.

Every figure must regenerate from saved result tables without retraining.

---

## **41\. Primary figures**

### **Figure 1**

Training and test curves with every analysed checkpoint marked.

### **Figure 2**

Recovered circuit-family dynamics across checkpoints and fidelity thresholds.

### **Figure 3**

Structural-overlap matrices and structural-distinctness sensitivity.

### **Figure 4**

Functional-transfer matrices and transfer-distinct groups.

### **Figure 5**

Main grokking models compared with random-label and matched no-generalisation controls.

Figures must show, where relevant:

* seed-level trajectories;  
* aggregation unit;  
* empty families;  
* family-target censoring;  
* search failures; and  
* sensitivity settings.

---

## **42\. Permitted conclusions**

Depending on the evidence, the paper may conclude:

* generalisation-associated circuit-family collapse;  
* persistent circuit non-identifiability;  
* partial structural convergence;  
* functional convergence without structural uniqueness;  
* structural compression without functional convergence; or  
* an unresolved threshold-sensitive result.

---

## **43\. Prohibited overclaims**

The paper must not claim:

* complete enumeration of circuit space;  
* discovery of the one true mechanism;  
* proof that no other valid circuits exist;  
* proof that transfer-equivalent circuits are mechanistically identical;  
* condition-level inference from one control seed;  
* independent replication from every recovered circuit; or  
* search failure as proof of circuit absence.

All conclusions must be conditional on:

* the component definition;  
* masking intervention;  
* search algorithm;  
* fidelity threshold;  
* distinctness cutoff;  
* family target; and  
* computational budget.

---

## **44\. Method-development outputs**

Any diversity-search output produced before the primary fidelity threshold is frozen must be labelled:

**METHOD DEVELOPMENT — EXCLUDED FROM SCIENTIFIC COMPARISONS**

Excluded outputs must be entered in an excluded-development-output register containing:

* file path;  
* creation date;  
* checkpoint;  
* settings;  
* purpose; and  
* reason for exclusion.

After the threshold is frozen, every reported diversity-family result must be regenerated from scratch.

---

## **45\. Exploratory analyses**

An analysis is exploratory if:

* it was introduced after the relevant result became visible;  
* it uses an unregistered subset;  
* it changes a primary threshold or budget to improve the result;  
* it adds a new metric after inspecting existing metrics; or  
* it selects checkpoints based on circuit-family outcomes.

Exploratory analyses may be reported, but they must be clearly separated from the primary analysis.

---

## **46\. Configuration files governed by this protocol**

The intended machine-readable files are:

configs/  
├── task.yaml  
├── model.yaml  
├── training.yaml  
├── search.yaml  
├── controls.yaml  
└── analysis.yaml

After creation, enter their hashes below.

| File | Hash | Git commit |
| ----- | ----- | ----- |
| `configs/task.yaml` | Pending | Pending |
| `configs/model.yaml` | Pending | Pending |
| `configs/training.yaml` | Pending | Pending |
| `configs/search.yaml` | Pending | Pending |
| `configs/controls.yaml` | Pending | Pending |
| `configs/analysis.yaml` | Pending | Pending |

Adding a hash or commit reference without altering the values already frozen in this document is administrative completion, not a scientific amendment.

---

## **47\. Analysis freeze**

At the final analysis freeze, record:

* included model seeds;  
* failed or replacement seeds;  
* analysed checkpoints;  
* primary fidelity threshold;  
* fidelity grid;  
* primary distinctness cutoff;  
* distinctness grid;  
* transfer-group tolerance;  
* controls;  
* matching rules;  
* statistical summaries;  
* figures;  
* family-target censoring; and  
* exploratory analyses.

The original predictions table must remain unchanged.

Each prediction must be resolved against the observed result.

---

## **48\. Final integrity rules**

1. No reported diversity family is generated before the primary fidelity threshold is frozen.  
2. Failure to recover a pre-grokking sparse circuit is allowed to remain a result.  
3. The predictions table is frozen before circuit-family results exist.  
4. Recovered family size is tested against both fidelity and structural-distinctness thresholds.  
5. The dynamics claim uses transition checkpoints rather than endpoints alone.  
6. Random-label and no-generalisation checkpoints are matched by training step.  
7. Empty families are reported as outcomes rather than hidden as missing data.  
8. Primary inference uses paired within-seed changes.  
9. The scaled checkpoint grid may be reduced only prospectively and uniformly.  
10. Controls are interpreted as attribution tests, not as automatic evidence for H2.  
11. Threshold-sensitive reversal is treated as fragility or unresolved evidence, not persistent multiplicity.  
12. No secondary endpoint may independently determine the headline conclusion.  
13. Planning stops at this protocol and the final implementation order. Further methodological changes require a documented empirical reason and amendment.

---

## **Stage 13 administrative freeze record**

* selected no-generalisation fraction: `no_qualifying_fraction`;
* exact training-example count: `not applicable`;
* Stage 13 run ID: `stage13-no-generalisation-s0-154f43de1214`;
* selection table: `results/tables/stage13_no_generalisation_selection.csv`;
* selection-table SHA-256: `26d21e456d5605e5cacebe317b94a47901526cae0085279bea171deb590923f6`;
* Stage 13 manifest: `manifests/stage13_no_generalisation_stage13-no-generalisation-s0-154f43de1214.json`;
* Stage 13 manifest SHA-256: `25bffe9604896e1d7480fbf03bfa9dab1c7840d546cd7ec149e78bc74820b854`;
* freeze timestamp UTC: `2026-07-21T07:10:09.167771+00:00`;
* selection decision commit: `2eabcc378596865365d3f2a8e9c481280bc03abd`;
* permitted evidence used: training and test curves only;
* no control circuit-family result existed or was inspected.

> The matched no-generalisation control changes the fraction of the original training partition available to the model. It therefore controls for training time, architecture, optimiser and regularisation while deliberately changing data coverage. Any later difference between the main condition and this control cannot be attributed solely to generalisation without acknowledging the reduced-data intervention.

## **Stage 15 administrative resolution record**

* Stage 15: resolved as `unavailable under the frozen protocol`;
* prerequisite: a qualifying Stage 13 no-generalisation fraction;
* prerequisite outcome: not satisfied;
* scientific computation: not performed;
* replacement control: none;
* criteria amended: no;
* Stage 16: permitted to proceed;
* Stage 15-dependent comparisons: `unavailable`.

This is an administrative resolution of a failed prerequisite, not a methodological amendment. Stage 15 is neither provisional nor deferred. No rejected candidate may be substituted, and no missing Stage 15 result may be imputed. An unavailable control is distinct from an executed control with an empty family: Stage 15 family size and transfer-group count are undefined, not zero.

## **Post-Stage-17 checkpoint-grid and concurrency freeze record**

* selected scaled checkpoint grid: `full_seven_checkpoint_grid`;
* checkpoint steps: `200, 3400, 7450, 8150, 8500, 8650, 9050`;
* sensitivity cells per analysed checkpoint: `18`;
* production concurrency: `12 isolated workers x 1 intra-op thread x 1 inter-op thread`;
* environment: `OMP_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`;
* compute-only ceiling: `14 isolated workers x 1 thread`;
* minimum reserved operational headroom: `4 CPU cores`;
* worker outputs: isolated by cell and output root;
* deterministic merging, archive creation and final reporting: serial;
* permitted evidence: compute projection, runtime, evaluation counts, storage,
  hardware, compute-only throughput and practical parallelism;
* scientific outcomes used: no;
* Stage 18 started: no;
* freeze manifest: `manifests/post_stage17_checkpoint_grid_and_concurrency_freeze.json`;
* benchmark summary: `results/tables/post_stage17_concurrency_benchmark_summary.csv`.

The full grid is selected prospectively and applies uniformly to the scaled main
seeds. The 14-worker result is a compute-only ceiling, not the production
default. No two workers may share a writable raw directory, table or manifest.

## **Post-Stage-17 additional-control seed-count freeze record**

* second no-generalisation seed: `not executable`;
* additional random-label seeds: `0`;
* required primary genuine-task seeds retained: `0, 1, 2, 3, 4`;
* main-seed workload priority preserved: yes;
* decision basis: committed compute projection, available storage, frozen
  production concurrency, expected Stage 18 main-seed workload and project
  schedule;
* scientific outcomes used: no;
* Stage 18 scientific outputs visible: no;
* decision manifest:
  `manifests/post_stage17_additional_control_seed_count_freeze.json`.

The required five-main-seed definitive and independent-reproduction workload
already projects to 459,775,077,926 bytes, approximately 1.67 million raw files
per pass and 12--16 continuous operational days before additional training.
Optional controls are therefore frozen at zero so they cannot delay or reduce
the mandatory main-seed analysis. Stage 15 remains unavailable rather than an
empty control result.

# **Amendment log**

| Date | Section changed | Change | Reason | Relevant results already visible? |
| ----- | ----- | ----- | :---: | :---: |
| 13 July 2026 | Initial protocol | Initial scientific questions, hypotheses, predictions and interpretation rules recorded | Project initiation | No |
| 14 July 2026 | Full protocol | Added the technical specification, primary endpoints, control-attribution logic, timing prediction, threshold-sensitivity interpretation, statistical plan and amendment discipline | Pre-results protocol completion | No |
| 14 July 2026  | §§4.4, 6 and 28.1 | Added prespecified handling of empty-family transitions and a random-label memorisation criterion | Closed remaining pre-results interpretive gaps | No |
| 18 July 2026 | §§21 and 44; pending-entry register | Recorded the mechanically selected primary fidelity threshold of 0.990000 and a zero-row excluded-development-output register | Required Stage 11 resolution under the already frozen selection rule | Yes — permitted Stage 11 calibration evidence only |
| 21 July 2026 | §27; Stage 13 administrative freeze record; pending-entry register | Recorded that no candidate fraction qualified; no control configuration was frozen and its provenance | Required Stage 13 resolution under the frozen curve-only rule | Yes — permitted Stage 13 training and test curves only |
| 22 July 2026 | Pending-entry register | Removed the resolved Stage 13 no-generalisation selection entry; the administrative freeze record already states `no_qualifying_fraction` and that no control configuration was frozen | Administrative consistency correction only; no scientific rule, result or interpretation changed | Yes — Stage 13 and Stage 14 results were already visible; no new scientific evidence was used |
| 25 July 2026 | Stage 15 administrative resolution record | Recorded Stage 15 as unavailable because its frozen Stage 13 prerequisite was not satisfied; permitted Stage 16 to proceed while marking Stage 15-dependent comparisons unavailable | Administrative resolution only; no scientific computation or methodological change | Yes — the final Stage 13 failure and Stage 14 results were already visible; no new scientific evidence was used |
| 28 July 2026 | Post-Stage-17 checkpoint-grid and concurrency freeze record; pending-entry register | Selected the full seven-checkpoint scaled grid and froze 12 isolated one-thread production workers after compute-only benchmarking; removed the resolved checkpoint-grid entry from the pending register | Required prospective compute and operational decision before Stage 18; scientific outcomes were excluded | Yes — Stages 12–17 were complete, but only permitted runtime, evaluation-count, storage, hardware and compute-only evidence was used |
| 28 July 2026 | Post-Stage-17 additional-control seed-count freeze record; pending-entry register | Froze zero additional random-label seeds and recorded the second no-generalisation seed as not executable; removed the resolved additional-control entry from the pending register | Preserve resources and schedule for the five required main seeds under the frozen priority rule | Yes — Stages 12–17 were complete, but no Stage 18 scientific outputs existed and only resource evidence was used |

---

# **Pending protocol entries**

The following entries are intentionally pending because their selection occurs later under an already frozen rule.

| Entry | Stage selected | Permitted basis |
| ----- | ----- | ----- |
| Configuration-file hashes | After configuration creation | Administrative record only |
| Final analysis commit | Stage 22 | Analysis freeze |

---

# **References informing the experimental setup**

Nanda, N., Chan, L., Lieberum, T., Smith, J. and Steinhardt, J. (2023). *Progress Measures for Grokking via Mechanistic Interpretability*. International Conference on Learning Representations.

Power, A., Burda, Y., Edwards, H., Babuschkin, I. and Misra, V. (2022). *Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets*.
