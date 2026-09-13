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
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(repo: Path) -> dict[str, pd.DataFrame]:
    return {name: pd.read_csv(repo / "results/tables" / path) for name, path in SOURCES.items()}


def primary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return data["e3"].loc[np.isclose(data["e3"].displayed_fidelity, 0.99)].copy()


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
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.75), layout="constrained")
    markers = dict(zip(PHASES, ["o", "^", "s"], strict=True))
    for seed in range(5):
        g = data["training"]
        g = g[(g.model_seed == seed) & (g.training_step <= 11000)]
        axes[0].plot(
            g.training_step, g.test_accuracy, color=COLORS[seed], lw=1, label=f"Seed {seed}"
        )
        g = p[p.model_seed == seed].sort_values("checkpoint_step")
        axes[1].plot(
            g.checkpoint_step,
            g.terminal_retained_components,
            color=COLORS[seed],
            lw=0.85,
            alpha=0.75,
        )
        for phase in PHASES:
            h = g[g.phase_label == phase]
            axes[1].scatter(
                h.checkpoint_step,
                h.terminal_retained_components,
                marker=markers[phase],
                color=COLORS[seed],
                s=20,
                zorder=3,
                edgecolors="white",
                linewidths=0.3,
            )
    axes[0].plot(STEPS, [-0.035] * 7, "|", color="black", markersize=4, clip_on=False)
    axes[0].set(
        title="(a) Test accuracy",
        xlabel="Training step",
        ylabel="Accuracy",
        ylim=(-0.02, 1.03),
        xlim=(0, 11000),
    )
    axes[0].legend(frameon=False, ncol=2, loc="upper left", columnspacing=0.7)
    axes[1].set(
        title="(b) First greedy circuit",
        xlabel="Training step",
        ylabel="Retained components",
        ylim=(0, 535),
        xlim=(0, 9500),
    )
    axes[1].axhline(258, color="0.5", ls="--", lw=0.7)
    axes[1].legend(
        handles=[
            Line2D([], [], marker=markers[q], color="0.3", ls="", label=LABELS[q], markersize=4)
            for q in PHASES
        ],
        frameon=False,
        loc="center left",
    )
    save(fig, out, "trajectory")

    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.65), sharey=True, layout="constrained")
    for ax, key, title in zip(
        axes,
        ["e3", "e4", "js"],
        ["(a) Greedy, top-one 0.990", "(b) Annealing, top-one 0.990", "(c) Annealing, JS 0.0005"],
        strict=True,
    ):
        d = (
            p.rename(columns={"terminal_retained_components": "final_retained_components"})
            if key == "e3"
            else data[key]
        )
        for j, phase in enumerate(PHASES):
            groups = list(d[d.phase_label == phase].groupby(["model_seed", "checkpoint_step"]))
            for x, ((seed, _step), g) in zip(
                np.linspace(j - 0.3, j + 0.3, len(groups)), groups, strict=True
            ):
                v = g.final_retained_components
                c = COLORS[seed]
                ax.vlines(x, v.min(), v.max(), color=c, lw=0.75)
                censored = key != "e3" and g.budget_censored.any()
                ax.scatter(
                    x,
                    v.median(),
                    s=15,
                    edgecolor=c,
                    linewidth=0.7,
                    facecolor="white" if censored else c,
                    zorder=3,
                )
        ax.axhline(258, color="0.5", ls="--", lw=0.7)
        ax.set(
            xticks=[0, 1, 2],
            xticklabels=["Delayed", "Transition", "Stable"],
            ylim=(0, 535),
            title=title,
        )
        ax.tick_params(axis="x", length=0)
    axes[0].set_ylabel("Retained components")
    save(fig, out, "search_robustness")

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9), layout="constrained")
    for null, marker in [("size_matched", "o"), ("basis_stratified", "^")]:
        for seed, g in data["e1"][data["e1"].null_model == null].groupby("model_seed"):
            axes[0].scatter(
                g.exact_null_mean,
                g.observed_jaccard,
                marker=marker,
                s=14,
                facecolor="none",
                edgecolor=COLORS[seed],
                alpha=0.75,
                linewidth=0.65,
            )
    axes[0].plot([0, 0.33], [0, 0.33], color="0.5", lw=0.7, ls="--")
    axes[0].set(
        xlim=(0, 0.33),
        ylim=(0, 0.33),
        xlabel="Expected Jaccard under matched null",
        ylabel="Observed Jaccard",
        title="(a) Structural overlap",
    )
    axes[0].legend(
        handles=[
            Line2D(
                [],
                [],
                ls="",
                marker=m,
                color="0.3",
                markerfacecolor="none",
                label=label,
                markersize=4,
            )
            for m, label in [("o", "Size matched"), ("^", "Composition matched")]
        ],
        loc="lower right",
        frameon=False,
    )
    profiles = data["observed"][["profile_id", "model_seed", "observed_retained_components"]]
    profiles = profiles.drop_duplicates().sort_values(
        ["model_seed", "observed_retained_components"]
    )
    for i, row in enumerate(profiles.itertuples(index=False)):
        for null, offset, marker in [("size_matched", -0.14, "o"), ("basis_stratified", 0.14, "^")]:
            g = data["e2"][
                (data["e2"].profile_id == row.profile_id) & (data["e2"].null_model == null)
            ].primary_fidelity
            c = COLORS[row.model_seed]
            axes[1].vlines(i + offset, g.min(), g.max(), color=c, lw=0.65, alpha=0.7)
            axes[1].scatter(i + offset, g.median(), s=12, marker=marker, color=c)
        obs = (
            data["observed"]
            .loc[data["observed"].profile_id == row.profile_id, "observed_primary_fidelity"]
            .min()
        )
        axes[1].scatter(i, obs, color=COLORS[row.model_seed], marker="D", s=12)
    axes[1].axhline(0.99, color="0.5", ls="--", lw=0.6)
    axes[1].set(
        ylim=(0, 1.04),
        xlabel="Seed / composition profile",
        ylabel="Top-one fidelity",
        title="(b) Behavioural fidelity",
    )
    centers = []
    for seed in [0, 1, 2, 4]:
        positions = np.flatnonzero(profiles.model_seed.to_numpy() == seed)
        centers.append(float(np.mean(positions)))
    axes[1].set_xticks(centers, ["Seed 0", "Seed 1", "Seed 2", "Seed 4"])
    axes[1].text(0.03, 0.83, "Observed circuits", transform=axes[1].transAxes, fontsize=7)
    save(fig, out, "matched_nulls")


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
        ["Metric", "Tolerance", "Delayed", "Sparse", "Transition", "Sparse", "Stable", "Sparse"],
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
    if not args.validate_only:
        for directory in ["figures", "generated"]:
            (args.out / directory).mkdir(parents=True, exist_ok=True)
        figures(data, args.out)
        tables(data, args.out)
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
