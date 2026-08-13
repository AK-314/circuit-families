# Stage 18 reproduction and downstream concurrency amendment

Date: 2026-07-31.

The research advisor directed that independent Stage 18 reproduction use one-half
to two-thirds of available processing capacity while Stages 19-22 proceed, because
the first research draft is due within one week.

The selected policy retains the frozen Stage 18 layout of 12 isolated one-thread
workers. On the 18-physical-core host this is two-thirds of physical-core capacity,
leaving six cores for downstream table analysis, inference and figure generation.
The reproduction process receives reduced scheduling priority. Stages 19-22 are
limited to six combined threads or workers while reproduction is active.

This amendment does not change the Stage 18 scientific configuration, cell registry,
worker-shard mapping, search budgets, transfer rule or deterministic outputs. It is
prospective for reproduction scheduling and downstream analysis; Stage 18 scientific
outcomes were not used to select the concurrency fraction.

Stage 18 definitive execution is complete but independent reproduction remains
pending. Stages 19-22 may begin under the advisor's direction, but their results must
not be finalized and Stage 18 must not be declared complete until reproduction and
byte-level comparison succeed.

The user-owned `stage17_inspection.md` file remains excluded.
