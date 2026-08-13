# Post-Stage-17 checkpoint-grid and concurrency freeze

## Decision

The scaled genuine-task analysis will use the full seven-checkpoint grid:

```text
200, 3400, 7450, 8150, 8500, 8650, 9050
```

The production CPU layout is frozen as 12 isolated workers with one PyTorch
intra-op thread and one inter-op thread per worker:

```text
OMP_NUM_THREADS=1
VECLIB_MAXIMUM_THREADS=1
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
```

Fourteen one-thread workers is the measured compute-only ceiling, not the
production default. Twelve workers leave six of the 18 physical cores nominally
unallocated and guarantee at least four cores of operational headroom.

## Prospective basis

This administrative decision used only compute and operational evidence:

- the committed Stage 12 compute projection;
- Stage 17 runtime and exact-evaluation totals;
- Stage 17 storage and file-count calibration;
- available hardware and storage;
- compute-only concurrency throughput, memory and integrity measurements; and
- the need for filesystem, hashing, monitoring and thermal headroom.

No family size, transfer result, checkpoint-specific scientific outcome,
publication preference or anticipated result direction was used. The full grid
was selected before Stage 18 training or circuit analysis began and applies
uniformly to all scaled main seeds.

## Workload projection

The frozen protocol requires 18 sensitivity cells at every analysed checkpoint.
For five main seeds and seven checkpoints this is 630 cells. The existing pilot
seed at step 9050 supplies 18 completed cells, leaving 612 main-condition cells.

Stage 17 calibrated 15 fresh cells at 659,524 exact evaluations and
56,929.182229 search seconds. Linear projection gives 645.20
single-worker-equivalent hours per pass. The conservative planning upper bound
is 734 hours per pass. At the production layout, definitive execution plus
independent reproduction is estimated at 11.12--12.65 compute-only days and
12--16 continuous operational days. Additional model training is excluded.

Stage 17 storage scales to approximately 208.39 GB of raw data and 21.50 GB of
archive data per pass. Definitive execution plus reproduction is projected at
459.78 GB, before incidental filesystem overhead. The available storage at the
freeze was 1,511,969,955,840 bytes.

## Concurrency evidence

The sustained benchmark established a single-worker baseline of
0.7162422632 cycles per second. The extended benchmark measured:

| Layout | Cycles per second | Status |
| --- | ---: | --- |
| 8 workers x 2 threads | 2.8744713952 | two-thread reference |
| 12 workers x 1 thread | 3.4644848208 | production |
| 14 workers x 1 thread | 3.6219178877 | compute-only ceiling |
| 16 workers x 1 thread | 3.6006413612 | below ceiling |
| 18 workers x 1 thread | 3.4670984670 | below ceiling |

The 14-worker ceiling was only 4.54% faster than production, while 16 and 18
workers did not improve throughput. The repeated 8-by-2 layout declined by
15.58% at the end of the extended run, supporting sustained-load headroom.
Every benchmark configuration preserved model state, absent parameter gradients
and the fixed mask hash.

The complete compute-only measurements are in
`results/tables/post_stage17_concurrency_benchmark_summary.csv`. Their source
report SHA-256 values and the benchmark-harness SHA-256 are pinned in the freeze
manifest.

## Isolation and deterministic reporting

Each worker must receive independent cells and an isolated output root. No two
workers may write to the same raw directory, table or manifest. Cell budgets,
restart budgets, masks, trajectories and logs remain independent.

After every worker has completed, deterministic merging, validation, archive
creation, manifest creation and final reporting must run serially in frozen cell
order. Concurrency may change scheduling and runtime telemetry only; it may not
change seeds, budgets, cell membership, scientific acceptance or deterministic
output bytes.

## Lifecycle boundary

The checkpoint-grid decision is now made. Stage 18 has not begun. This record
does not train a model, execute a Stage 18 circuit search, select control-seed
counts or alter any Stage 17 scientific result.
