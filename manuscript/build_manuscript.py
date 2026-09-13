"""Build manuscript displays from frozen tables; never load a model or run a search."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

PHASES = ["delayed_pre_generalisation", "transition", "stable_post"]
LABELS = dict(zip(PHASES, ["Delayed", "Transition", "Stable"], strict=True))
COLORS = ["#2473A3", "#C06B27", "#27866C", "#8D6DA7", "#B74D65"]
STEPS = [200, 3400, 7450, 8150, 8500, 8650, 9050]
JS = "mean_jensen_shannon_divergence"
MARGIN = "normalized_mean_absolute_reference_margin_error"
SOURCES = {
    "training": "stage21_figure1_training_curves_source.csv",
    "families": "stage21_figure2_family_dynamics_source.csv",
    "e1": "phase1_tmlr_e1_jaccard_null_v1/pairwise_jaccard_null.csv",
    "e2": "phase1_tmlr_e2_random_mask_fidelity_v1/random_mask_fidelity_evaluations.csv",
    "observed": "phase1_tmlr_e2_random_mask_fidelity_v1/random_mask_fidelity_circuit_summary.csv",
    "e3": "phase1_tmlr_e3_greedy_endpoint_trajectory_v1/greedy_endpoint_trajectories.csv",
    "e4": "phase1_tmlr_e4_independent_search_v1/independent_search_runs.csv",
    "grid": "phase1_tmlr_e5_greedy_grid_v1/nonargmax_fidelity_runs.csv",
    "calibration": "phase1_tmlr_e5_calibration_v1/nonargmax_fidelity_runs.csv",
    "js": "phase1_tmlr_e5_full_js_v1/nonargmax_fidelity_runs.csv",
    "review_masks": "phase1_review_followup_v1/evaluation/mask_evaluations.csv",
    "review_families": "phase1_review_followup_v1/audit/annealing_saved_pool_families.csv",
    "review_confidence": "phase1_review_followup_v1/audit/confidence_positions.csv",
    "review_optimizer": "phase1_review_followup_v1/audit/optimizer_phase_summary.csv",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(repo: Path) -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(repo / "results/tables" / path) for name, path in SOURCES.items()}


def primary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return data["e3"].loc[np.isclose(data["e3"].displayed_fidelity, 0.99)].copy()


def review_displays(data: dict[str, pd.DataFrame], out: Path) -> None:
    """Display the post-review audit and fixed-mask evaluations without reevaluation."""
    d = data["review_masks"]
    assert len(d) == 70 and set(d.model_seed) == {0, 1, 2, 4}
    original = d[d.kind == "original"]
    removed = d[d.kind == "without_core"]
    core = d[d.kind == "core"]
    assert len(original) == len(removed) == 27
    assert original.passes_top1_099.all()
    assert not removed.passes_top1_099.any() and not core.passes_top1_099.any()
    assert core.retained_neurons.tolist() == [3, 8, 4, 1]
    assert not original["passes_js_0.0005"].any()
    assert not original["passes_margin_0.4"].any()
    f = data["review_families"]
    assert len(f) == 60
    assert f[(f.analysis == "e4") & (f.cutoff == 0.5)].maximum_saved_pool_family.eq(10).all()
    rows, detailed = [], []
    for seed, group in d.groupby("model_seed"):
        c = group[group.kind == "core"].iloc[0]
        r = group[group.kind == "without_core"]
        u = group[group.kind == "union"].iloc[0]
        o = group[group.kind == "original"]
        rows.append(
            f"{seed} & {len(o)} & {c.retained_neurons} & {c.top1_fidelity:.4f} & "
            f"{r.top1_fidelity.min():.4f}--{r.top1_fidelity.max():.4f} & "
            f"{u.top1_fidelity:.4f} " + r"\\"
        )
        detailed.append(
            [
                str(seed),
                str(len(o)),
                *[
                    f"{o[col].min():.3f}--{o[col].max():.3f}"
                    for col in ["js_T1_mean", "js_T2_mean", "js_T4_mean", "normalized_margin_error"]
                ],
            ]
        )
    (out / "generated/family_core.tex").write_text(
        "\n".join(
            [
                r"\begin{table}[tb]\centering\small",
                r"\caption{\textbf{Shared neurons matter, but do not suffice.} "
                r"All interventions retain the four attention heads. Core: neurons in every "
                r"original family member. Entries report full-domain prediction agreement. "
                r"Removing the core fails the 0.990 criterion for all 27 members; taking "
                r"the union of members also fails in three models.}",
                r"\label{tab:core}",
                r"\begin{tabular}{crrrrr}\toprule",
                r"Seed & Members & Core neurons & Core only & Core removed & Union \\\midrule",
                *rows,
                r"\bottomrule\end{tabular}\end{table}",
                "",
            ]
        )
    )
    longtable(
        out,
        "original_cross_metric",
        "Cross-metric scores of the same 27 original "
        "family masks at step 9,050. Ranges across members; JS uses natural logs. "
        "Both reference and masked logits use the stated common temperature. "
        "Margin error is normalised by the reference margin.",
        "originalmetrics",
        "rrrrrr",
        ["Seed", "$n$", "JS, $T=1$", "JS, $T=2$", "JS, $T=4$", "Margin error"],
        detailed,
    )
    rows = []
    for (analysis, seed), group in f.groupby(["analysis", "model_seed"]):
        half = group[group.cutoff == 0.5].maximum_saved_pool_family
        quarter = group[group.cutoff == 0.25].maximum_saved_pool_family
        rows.append(
            [
                "Top-one" if analysis == "e4" else "JS",
                str(seed),
                str(len(half)),
                f"{quarter.min()}--{quarter.max()}",
                f"{half.min()}--{half.max()}",
                str(int(half.ge(2).sum())),
            ]
        )
    longtable(
        out,
        "saved_pool_families",
        "Largest qualifying family in each pool of ten saved "
        "annealing masks, computed exactly after the runs. Ranges span stable positions "
        "within a seed. Multiplicity means at least two qualifying masks at Jaccard 0.50; "
        "zero means no mask meets the 258-component bound.",
        "savedfamilies",
        "lrrrrr",
        ["Criterion", "Seed", "Positions", "$J\\leq0.25$", "$J\\leq0.50$", "Multiplicity"],
        rows,
    )


def validate_review(data: dict[str, pd.DataFrame]) -> None:
    d = data["review_masks"]
    assert len(d) == 70 and d.example_count.eq(12769).all()
    assert d.retained_heads.eq(4).all()
    assert d[d.kind == "original"].passes_top1_099.all()
    assert not d[d.kind.isin(["core", "without_core"])].passes_top1_099.any()


def validate(data: dict[str, pd.DataFrame]) -> dict:
    """Fail loudly on changed coverage or the principal numerical claims."""
    p = primary(data)
    expected = {(s, t) for s in range(5) for t in STEPS}
    assert set(zip(p.model_seed, p.checkpoint_step, strict=True)) == expected
    assert len(data["e3"]) == 210 and len(p) == 35
    assert data["e3"].locally_single_deletion_minimal.all()
    assert p.groupby("phase_label").size().to_dict() == dict(zip(PHASES, [9, 11, 15], strict=True))
    ranges = [(510, 515), (297, 515), (65, 146)]
    for phase, bounds in zip(PHASES, ranges, strict=True):
        sizes = p.loc[p.phase_label == phase, "terminal_retained_components"]
        assert (sizes.min(), sizes.max()) == bounds
    for key, bounds, sparse in [
        ("e4", [(508, 515), (264, 515), (58, 136)], [0, 0, 150]),
        ("js", [(509, 515), (432, 515), (209, 368)], [0, 0, 40]),
    ]:
        d = data[key]
        assert len(d) == 350
        assert d.groupby(["model_seed", "checkpoint_step"]).size().eq(10).all()
        assert set(zip(d.model_seed, d.checkpoint_step, strict=True)) == expected
        assert d.locally_single_deletion_minimal.all()
        for phase, limits, count in zip(PHASES, bounds, sparse, strict=True):
            group = d[d.phase_label == phase]
            assert (
                group.final_retained_components.min(),
                group.final_retained_components.max(),
            ) == limits
            assert group.meaningfully_sparse.sum() == count
        joined = d.merge(
            p[["model_seed", "checkpoint_step", "phase_label"]],
            on=["model_seed", "checkpoint_step"],
            validate="many_to_one",
        )
        assert joined.phase_label_x.eq(joined.phase_label_y).all()
    assert data["e4"].final_fidelity.ge(0.99).all()
    assert data["js"].criterion_tolerance.eq(0.0005).all()
    assert data["js"].final_criterion_value.le(0.0005).all()
    assert len(data["grid"]) == 420 and data["grid"].locally_single_deletion_minimal.sum() == 419
    assert len(data["calibration"]) == 60
    assert len(data["e1"]) == 156 and data["e1"].pair_id.nunique() == 78
    assert data["e1"].groupby("null_model").size().eq(78).all()
    for null, group in data["e1"].groupby("null_model"):
        assert group.observed_jaccard.median() > group.exact_null_mean.median(), null
    assert len(data["e2"]) == 4200 and data["e2"].profile_id.nunique() == 21
    assert data["e2"].groupby(["profile_id", "null_model"]).size().eq(100).all()
    assert not data["e2"].passes_0_990_threshold.any()
    assert data["observed"].observed_retained_heads.eq(4).all()
    f = data["families"]
    assert len(f) == 630
    f = f[np.isclose(f.displayed_fidelity, 0.99) & np.isclose(f.displayed_jaccard_cutoff, 0.5)]
    joined = f.merge(
        p[["model_seed", "checkpoint_step", "phase_label"]],
        on=["model_seed", "checkpoint_step"],
        validate="one_to_one",
    )
    assert joined.loc[joined.phase_label != "stable_post", "family_size"].eq(0).all()
    assert joined.loc[joined.phase_label == "stable_post", "family_size"].isin([6, 7]).all()
    return {
        "status": "validated",
        "model_seeds": 5,
        "positions": 35,
        "family_cells": 630,
        "e1_pairs": 78,
        "e2_masks": 4200,
        "e3_endpoints": 210,
        "e4_runs": 350,
        "e5_grid_runs": 420,
        "e5_calibration_runs": 60,
        "e5_full_js_runs": 350,
        "model_evaluations_performed_by_builder": 0,
    }


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "axes.linewidth": 0.6,
            "savefig.dpi": 180,
        }
    )


def save(fig, out: Path, name: str) -> None:
    fig.savefig(
        out / "figures" / f"{name}.pdf",
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    fig.savefig(out / "figures" / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def figures(data: dict[str, pd.DataFrame], out: Path) -> None:
    style()
    p = primary(data)
    phase_colors = dict(zip(PHASES, ["#737980", "#C28A38", "#2473A3"], strict=True))
    phase_handles = [
        Line2D([], [], marker="o", ls="", color=phase_colors[q], label=LABELS[q]) for q in PHASES
    ]

    # The common-grid matrix shows every endpoint without crowded late-time curves.
    fig = plt.figure(figsize=(6.6, 4.6), layout="constrained")
    grids = fig.add_gridspec(2, 1, height_ratios=[1, 1.05])
    ax = fig.add_subplot(grids[0])
    for seed in range(5):
        g = data["training"]
        g = g[(g.model_seed == seed) & (g.training_step <= 11000)]
        ax.plot(
            g.training_step,
            g.test_accuracy,
            color=COLORS[seed],
            lw=1.1,
            label=f"Seed {seed}",
        )
    ax.plot(STEPS, [-0.035] * 7, "|", color="black", markersize=5, clip_on=False)
    ax.set(
        title="(a) Generalisation occurs at different training steps",
        xlabel="Training step",
        ylabel="Test accuracy",
        ylim=(-0.02, 1.04),
        xlim=(0, 11000),
        yticks=[0, 0.5, 1],
    )
    ax.legend(frameon=False, ncol=5, loc="lower center", bbox_to_anchor=(0.5, 1.16))
    ax = fig.add_subplot(grids[1])
    sizes = p.pivot(
        index="model_seed",
        columns="checkpoint_step",
        values="terminal_retained_components",
    ).reindex(columns=STEPS)
    phases = p.pivot(index="model_seed", columns="checkpoint_step", values="phase_label").reindex(
        columns=STEPS
    )
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "retained_size", ["#195E8C", "#78ADC7", "#F1F3F4"]
    )
    im = ax.imshow(sizes, vmin=0, vmax=516, cmap=cmap, aspect="auto")
    for i in range(5):
        for j in range(7):
            v = int(sizes.iloc[i, j])
            phase = LABELS[phases.iloc[i, j]][0]
            ax.text(
                j,
                i,
                f"{v} {phase}",
                ha="center",
                va="center",
                color="white" if v < 180 else "#17232B",
                fontsize=8,
            )
    ax.set(
        title="(b) Components retained at 99% prediction agreement",
        xticks=range(7),
        xticklabels=[f"{s:,}" for s in STEPS],
        yticks=range(5),
        yticklabels=[f"Seed {s}" for s in range(5)],
        xlabel="Analysed checkpoint",
    )
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    bar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, ticks=[0, 258, 516])
    bar.set_label("Retained components")
    save(fig, out, "trajectory")

    # Paired axes give position a numerical meaning and directly test search dependence.
    fig, axes = plt.subplots(
        1, 2, figsize=(6.6, 3.45), sharex=True, sharey=True, layout="constrained"
    )
    greedy_js = data["grid"].loc[
        (data["grid"].criterion_name == JS) & np.isclose(data["grid"].criterion_tolerance, 0.0005)
    ]
    for ax, key, greedy, size_col, title in [
        (
            axes[0],
            "e4",
            p,
            "terminal_retained_components",
            "(a) Top-one agreement ≥ 0.990",
        ),
        (
            axes[1],
            "js",
            greedy_js,
            "final_retained_components",
            "(b) JS divergence ≤ 0.0005",
        ),
    ]:
        ax.plot([0, 516], [0, 516], color="0.55", lw=0.8)
        ax.axhline(258, color="0.6", ls="--", lw=0.7)
        ax.axvline(258, color="0.6", ls="--", lw=0.7)
        for row in greedy.itertuples():
            g = data[key][
                (data[key].model_seed == row.model_seed)
                & (data[key].checkpoint_step == row.checkpoint_step)
            ]
            v = g.final_retained_components
            x = getattr(row, size_col)
            c = phase_colors[row.phase_label]
            ax.vlines(x, v.min(), v.max(), color=c, lw=0.9, alpha=0.8)
            ax.scatter(
                x,
                v.median(),
                color=c,
                s=19,
                alpha=0.85,
                edgecolors="white",
                linewidths=0.3,
                zorder=3,
            )
        ax.set(
            title=title,
            xlabel="Greedy: retained components",
            xlim=(0, 540),
            ylim=(0, 540),
            xticks=[0, 258, 516],
            yticks=[0, 258, 516],
        )
        ax.set_aspect("equal")
    axes[0].set_ylabel("Annealing: retained components")
    fig.legend(handles=phase_handles, frameon=False, ncol=3, loc="outside upper center")
    save(fig, out, "search_robustness")

    # Pool only within a model, with each distinct matching profile weighted equally.
    fig, ax = plt.subplots(figsize=(6.6, 2.85), layout="constrained")
    null_colors = {"size_matched": "#A9AFB5", "basis_stratified": "#2473A3"}
    observed = data["observed"].drop_duplicates(["model_seed", "circuit_id"])
    display_rows = []
    for i, seed in enumerate([0, 1, 2, 4]):
        for null, offset in [("size_matched", -0.18), ("basis_stratified", 0.18)]:
            g = data["e2"][(data["e2"].model_seed == seed) & (data["e2"].null_model == null)]
            values = g.primary_fidelity
            ax.boxplot(
                values,
                positions=[i + offset],
                widths=0.26,
                whis=(0, 100),
                showfliers=False,
                patch_artist=True,
                manage_ticks=False,
                boxprops={"facecolor": null_colors[null], "alpha": 0.65},
                medianprops={"color": "#17232B"},
                whiskerprops={"color": null_colors[null]},
                capprops={"color": null_colors[null]},
            )
            display_rows.append(
                {
                    "model_seed": seed,
                    "group": null,
                    "count": len(values),
                    "minimum": values.min(),
                    "q25": values.quantile(0.25),
                    "median": values.median(),
                    "q75": values.quantile(0.75),
                    "maximum": values.max(),
                }
            )
        obs = observed[observed.model_seed == seed].observed_primary_fidelity
        ax.scatter(np.full(len(obs), i), obs, marker="D", color="#B45532", s=20, zorder=4)
        display_rows.append(
            {
                "model_seed": seed,
                "group": "recovered",
                "count": len(obs),
                "minimum": obs.min(),
                "q25": obs.quantile(0.25),
                "median": obs.median(),
                "q75": obs.quantile(0.75),
                "maximum": obs.max(),
            }
        )
    ax.axhline(0.99, color="#B45532", ls="--", lw=0.8)
    ax.set(
        xticks=range(4),
        xticklabels=["Seed 0", "Seed 1", "Seed 2", "Seed 4"],
        ylabel="Prediction agreement with full model",
        ylim=(0, 1.06),
        yticks=[0, 0.25, 0.5, 0.75, 0.99],
        yticklabels=["0", "0.25", "0.50", "0.75", "0.99"],
    )
    fig.legend(
        handles=[
            Line2D([], [], color="#B45532", marker="D", ls="", label="Recovered circuits"),
            Line2D(
                [],
                [],
                color=null_colors["basis_stratified"],
                lw=6,
                label="Random: same heads + neuron count",
            ),
            Line2D(
                [],
                [],
                color=null_colors["size_matched"],
                lw=6,
                label="Random: same total size",
            ),
        ],
        frameon=False,
        ncol=1,
        loc="outside upper center",
    )
    save(fig, out, "matched_nulls")
    pd.DataFrame(display_rows).to_csv(out / "generated/behavioural_null_display.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(6.6, 3.15), sharey=True, layout="constrained")
    for ax, d, tolerance, size, title in [
        (
            axes[0],
            data["e3"],
            "displayed_fidelity",
            "terminal_retained_components",
            "(a) Top-one agreement",
        ),
        (
            axes[1],
            data["grid"][data["grid"].criterion_name == JS],
            "criterion_tolerance",
            "final_retained_components",
            "(b) JS divergence",
        ),
        (
            axes[2],
            data["grid"][data["grid"].criterion_name == MARGIN],
            "criterion_tolerance",
            "final_retained_components",
            "(c) Margin error",
        ),
    ]:
        levels = sorted(d[tolerance].unique(), reverse=tolerance == "displayed_fidelity")
        for phase in PHASES:
            g = d[d.phase_label == phase].groupby(tolerance)[size]
            lo, mid, hi = [g.agg(op).reindex(levels).to_numpy() for op in ["min", "median", "max"]]
            ax.fill_between(range(6), lo, hi, color=phase_colors[phase], alpha=0.1)
            ax.plot(range(6), mid, color=phase_colors[phase], marker="o", ms=3, lw=1)
        ax.axhline(258, color="0.5", lw=0.7, ls="--")
        ax.set(
            title=title,
            ylim=(0, 535),
            xticks=range(6),
            xticklabels=[f"{x:g}" for x in levels],
            xlabel="Strict → permissive",
            yticks=[0, 258, 516],
        )
        ax.tick_params(axis="x", labelrotation=55)
    axes[0].set_ylabel("Greedy: retained components")
    fig.legend(handles=phase_handles, ncol=3, frameon=False, loc="outside upper center")
    save(fig, out, "fidelity_tradeoff")

    fig, axes = plt.subplots(
        1, 4, figsize=(6.6, 2.65), sharex=True, sharey=True, layout="constrained"
    )
    for ax, seed in zip(axes, [0, 1, 2, 4], strict=True):
        for null, marker, color in [
            ("size_matched", "o", "#A9AFB5"),
            ("basis_stratified", "^", "#2473A3"),
        ]:
            g = data["e1"][(data["e1"].model_seed == seed) & (data["e1"].null_model == null)]
            ax.scatter(
                g.exact_null_mean,
                g.observed_jaccard,
                marker=marker,
                s=12,
                color=color,
                alpha=0.8,
                linewidths=0,
            )
        ax.plot([0, 0.33], [0, 0.33], color="0.5", ls="--", lw=0.7)
        ax.set(
            title=f"Seed {seed}",
            xlim=(0, 0.33),
            ylim=(0, 0.33),
            xticks=[0, 0.15, 0.3],
            yticks=[0, 0.15, 0.3],
        )
        ax.set_aspect("equal")
    axes[0].set_ylabel("Observed Jaccard")
    fig.supxlabel("Expected Jaccard for independent matched subsets", fontsize=8)
    fig.legend(
        handles=[
            Line2D([], [], marker="o", ls="", color="#A9AFB5", label="Same total size"),
            Line2D(
                [],
                [],
                marker="^",
                ls="",
                color="#2473A3",
                label="Same heads + neuron count",
            ),
        ],
        frameon=False,
        ncol=2,
        loc="outside upper center",
    )
    save(fig, out, "overlap_nulls")


def number(x) -> str:
    return f"{x:g}"


def triple(series: pd.Series) -> str:
    return "/".join(number(v) for v in [series.min(), series.median(), series.max()])


def longtable(
    out: Path,
    name: str,
    caption: str,
    label: str,
    columns: str,
    headers: list[str],
    rows: list[list[str]],
) -> None:
    header = " & ".join(headers) + r" \\" + "\n"
    tex = [
        r"\begingroup\small\setlength{\tabcolsep}{4pt}",
        r"\begin{longtable}{" + columns + "}",
        r"\caption{" + caption + r"}\label{tab:" + label + r"}\\",
        r"\toprule",
        header,
        r"\midrule\endfirsthead",
        r"\toprule",
        header,
        r"\midrule\endhead",
        r"\bottomrule\endfoot",
    ]
    tex += [" & ".join(row) + r" \\" for row in rows]
    tex += [r"\end{longtable}", r"\endgroup"]
    (out / "generated" / f"{name}.tex").write_text("\n".join(tex) + "\n")


def tables(data: dict[str, pd.DataFrame], out: Path) -> None:
    rows = []
    for fidelity, group in data["e3"].groupby("displayed_fidelity", sort=True):
        row = [f"{fidelity:.3f}"]
        for phase in PHASES:
            g = group[group.phase_label == phase].terminal_retained_components
            row += [triple(g), f"{(g <= 258).sum()}/{len(g)}"]
        rows.append(row)
    longtable(
        out,
        "e3_grid",
        "First greedy size by fidelity and phase. Size entries are "
        "minimum/median/maximum; sparse columns count positions at or below 258.",
        "e3grid",
        "r rr rr rr",
        [
            "Fidelity",
            "Delayed size",
            "Sparse",
            "Transition size",
            "Sparse",
            "Stable size",
            "Sparse",
        ],
        rows,
    )
    rows = []
    display = []
    for key, title in [("e4", "Top-one"), ("js", "JS")]:
        for phase in PHASES:
            g = data[key][data[key].phase_label == phase]
            rows.append(
                [
                    title,
                    LABELS[phase],
                    str(len(g)),
                    triple(g.final_retained_components),
                    str(g.meaningfully_sparse.sum()),
                    str(g.budget_censored.sum()),
                    str(g.stochastic_plateau_satisfied.sum()),
                ]
            )
            display.append(
                {
                    "analysis": key,
                    "phase": phase,
                    "run_count": len(g),
                    "minimum": int(g.final_retained_components.min()),
                    "median": float(g.final_retained_components.median()),
                    "maximum": int(g.final_retained_components.max()),
                    "sparse": int(g.meaningfully_sparse.sum()),
                    "censored": int(g.budget_censored.sum()),
                    "plateau": int(g.stochastic_plateau_satisfied.sum()),
                }
            )
    pd.DataFrame(display).to_csv(out / "generated/search_summary.csv", index=False)
    longtable(
        out,
        "search_summary",
        "Annealing search outcomes. Size is "
        "minimum/median/maximum over streams. Censored and plateau are separate flags "
        "defined in Section S3.1. Every run completes local cleanup.",
        "searchsummary",
        "llrrrrr",
        ["Criterion", "Phase", "Runs", "Size", "Sparse", "Censored", "Plateau"],
        rows,
    )
    rows = []
    for criterion in [JS, MARGIN]:
        d = data["grid"][data["grid"].criterion_name == criterion]
        for tolerance, group in d.groupby("criterion_tolerance"):
            row = ["JS" if criterion == JS else "Margin", number(tolerance)]
            for phase in PHASES:
                g = group[group.phase_label == phase]
                value = triple(g.final_retained_components)
                if g.budget_censored.any():
                    value += r"$^{*}$"
                row += [value, f"{g.meaningfully_sparse.sum()}/{len(g)}"]
            rows.append(row)
    longtable(
        out,
        "e5_grid",
        "Complete deterministic non-argmax grid. Each phase reports "
        "minimum/median/maximum retained size and sparse positions. The starred group "
        "contains one censored endpoint (seed 0, step 9,050, size 458); all other "
        "endpoints are locally minimal and uncensored.",
        "e5grid",
        "lr rr rr rr",
        [
            "Metric",
            "Tolerance",
            "Delayed",
            "Sparse",
            "Transition",
            "Sparse",
            "Stable",
            "Sparse",
        ],
        rows,
    )
    rows = []
    for criterion in [JS, MARGIN]:
        d = data["calibration"][data["calibration"].criterion_name == criterion]
        for tolerance, g in d.groupby("criterion_tolerance"):
            passed = (
                g.meaningfully_sparse.sum() >= 4
                and g.locally_single_deletion_minimal.all()
                and not g.budget_censored.any()
            )
            gate = "pass" if passed else "fail"
            if criterion == JS and tolerance == 0.0005:
                gate += "; selected"
            rows.append(
                [
                    "JS" if criterion == JS else "Margin",
                    number(tolerance),
                    triple(g.final_retained_components),
                    f"{g.meaningfully_sparse.sum()}/5",
                    gate,
                ]
            )
    longtable(
        out,
        "calibration",
        "All stable-only calibration results at seed 0, step 9,050. "
        "Every run is locally minimal and uncensored.",
        "calibration",
        "lrrrl",
        ["Metric", "Tolerance", "Min/median/max", "Sparse", "Gate"],
        rows,
    )
    rows = []
    position_display = []
    for row in primary(data).sort_values(["model_seed", "checkpoint_step"]).itertuples():
        e4 = data["e4"][
            (data["e4"].model_seed == row.model_seed)
            & (data["e4"].checkpoint_step == row.checkpoint_step)
        ]
        js = data["js"][
            (data["js"].model_seed == row.model_seed)
            & (data["js"].checkpoint_step == row.checkpoint_step)
        ]
        assert js.mean_full_model_reference_margin.nunique() == 1
        phase = LABELS[row.phase_label][0]
        rows.append(
            [
                str(row.model_seed),
                str(row.checkpoint_step),
                phase,
                str(row.terminal_retained_components),
                triple(e4.final_retained_components),
                triple(js.final_retained_components),
                f"{js.mean_full_model_reference_margin.iloc[0]:.2f}",
                f"{js.mean_absolute_reference_margin_error.median():.2f}",
            ]
        )
        position_display.append(
            {
                "model_seed": row.model_seed,
                "checkpoint_step": row.checkpoint_step,
                "phase": row.phase_label,
                "greedy_top1": row.terminal_retained_components,
                "annealing_top1_min": int(e4.final_retained_components.min()),
                "annealing_top1_median": float(e4.final_retained_components.median()),
                "annealing_top1_max": int(e4.final_retained_components.max()),
                "annealing_top1_censored": int(e4.budget_censored.sum()),
                "annealing_js_min": int(js.final_retained_components.min()),
                "annealing_js_median": float(js.final_retained_components.median()),
                "annealing_js_max": int(js.final_retained_components.max()),
                "annealing_js_censored": int(js.budget_censored.sum()),
                "full_margin": float(js.mean_full_model_reference_margin.iloc[0]),
                "js_raw_margin_error_median": float(
                    js.mean_absolute_reference_margin_error.median()
                ),
            }
        )
    pd.DataFrame(position_display).to_csv(out / "generated/positions.csv", index=False)
    longtable(
        out,
        "positions",
        "All checkpoint positions. G: greedy top-one size. A: annealing "
        "top-one size; JS: annealing Jensen--Shannon size at 0.0005 (both min/median/max). "
        r"$m$: mean full-model reference margin; $e$: median raw mean absolute margin error "
        "among the ten JS endpoints. D/T/S indicate phase.",
        "positions",
        "rrrrrrrr",
        ["Seed", "Step", "Phase", "G", "A", "JS", "$m$", "$e$"],
        rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    data = load(args.repo)
    report = validate(data)
    validate_review(data)
    if not args.validate_only:
        for directory in ["figures", "generated"]:
            (args.out / directory).mkdir(parents=True, exist_ok=True)
        figures(data, args.out)
        tables(data, args.out)
        review_displays(data, args.out)
        registry = {
            "analysis": "manuscript_aggregation_only",
            "source_files": {
                f"results/tables/{p}": digest(args.repo / "results/tables" / p)
                for p in SOURCES.values()
            },
            "validation": report,
            "builder_sha256": digest(Path(__file__)),
            "generated_files": {
                str(p.relative_to(args.out)): digest(p)
                for directory in ["generated", "figures"]
                for p in sorted((args.out / directory).iterdir())
                if p.is_file()
            },
        }
        (args.out / "source_registry.json").write_text(json.dumps(registry, indent=2) + "\n")
    else:
        registry_path = args.out / "source_registry.json"
        if registry_path.exists():
            registry = json.loads(registry_path.read_text())
            for path, expected in registry["source_files"].items():
                assert digest(args.repo / path) == expected, path
            for path, expected in registry["generated_files"].items():
                assert digest(args.out / path) == expected, path
            assert digest(Path(__file__)) == registry["builder_sha256"]
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
