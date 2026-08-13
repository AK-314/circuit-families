"""Regenerate Figures 1--5 directly from the deposited figure-source CSVs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path

_CACHE_ROOT = Path(tempfile.gettempdir()) / "circuit-families-artifact-cache"
_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_CACHE_ROOT / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_CACHE_ROOT))

import matplotlib  # noqa: E402
import numpy as np  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_STEPS = (200, 3400, 7450, 8150, 8500, 8650, 9050)
SOURCE_TABLES = (
    "results/tables/stage21_figure1_training_curves_source.csv",
    "results/tables/stage21_figure2_family_dynamics_source.csv",
    "results/tables/stage21_figure3_structural_source.csv",
    "results/tables/stage21_figure4_transfer_source.csv",
    "results/tables/stage21_figure5_controls_source.csv",
)
FREEZE_MANIFEST = ROOT / "manifests/stage22_freeze_stage22-freeze-34241335dcf7.json"


def _rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_sources() -> None:
    freeze = json.loads(FREEZE_MANIFEST.read_text(encoding="utf-8"))
    expected = freeze["source_artifacts"]
    for relative in SOURCE_TABLES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"Missing figure-source table: {relative}")
        if _sha256(path) != expected.get(relative):
            raise ValueError(f"Figure-source hash mismatch: {relative}")


def _save(figure: object, output_dir: Path, stem: str) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    png = output_dir / f"{stem}.png"
    pdf = output_dir / f"{stem}.pdf"
    figure.savefig(png, dpi=220, metadata={"Software": "circuit-families artifact"})
    figure.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    return png, pdf


def _mean(values: Iterable[float]) -> float:
    values = tuple(values)
    if not values:
        raise ValueError("Cannot calculate a mean over an empty source selection.")
    return float(np.mean(values))


def figure1(output_dir: Path) -> tuple[Path, Path]:
    rows = _rows(SOURCE_TABLES[0])
    figure, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True, sharex=True)
    for seed in range(5):
        seed_rows = sorted(
            (row for row in rows if int(row["model_seed"]) == seed),
            key=lambda row: int(row["training_step"]),
        )
        steps = [int(row["training_step"]) for row in seed_rows]
        axes[0].plot(
            steps,
            [float(row["train_accuracy"]) for row in seed_rows],
            label=f"seed {seed}",
        )
        axes[1].plot(
            steps,
            [float(row["test_accuracy"]) for row in seed_rows],
            label=f"seed {seed}",
        )
    for axis in axes:
        for step in CHECKPOINT_STEPS:
            axis.axvline(step, color="0.75", linewidth=0.6, zorder=0)
        axis.set(xlabel="Training step", ylim=(-0.02, 1.02))
    axes[0].set(title="Training accuracy", ylabel="Accuracy")
    axes[1].set(title="Test accuracy")
    axes[1].legend(frameon=False, loc="lower right")
    figure.suptitle("Figure 1. Training trajectories and analysed checkpoints")
    outputs = _save(figure, output_dir, "figure1_training_trajectories")
    plt.close(figure)
    return outputs


def figure2(output_dir: Path) -> tuple[Path, Path]:
    rows = _rows(SOURCE_TABLES[1])
    primary = [
        row
        for row in rows
        if row["displayed_fidelity"] == "0.990" and row["displayed_jaccard_cutoff"] == "0.50"
    ]
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    for seed in range(5):
        seed_rows = sorted(
            (row for row in primary if int(row["model_seed"]) == seed),
            key=lambda row: CHECKPOINT_STEPS.index(int(row["checkpoint_step"])),
        )
        axes[0].plot(
            [CHECKPOINT_STEPS.index(int(row["checkpoint_step"])) for row in seed_rows],
            [int(row["family_size"]) for row in seed_rows],
            marker="o",
            label=f"seed {seed}",
        )
    axes[0].set(
        title="Primary family trajectories",
        xlabel="Checkpoint step",
        ylabel="Recovered family size",
        xticks=range(len(CHECKPOINT_STEPS)),
        xticklabels=[str(step) for step in CHECKPOINT_STEPS],
    )
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].legend(frameon=False)

    fidelity_levels = ("0.800", "0.850", "0.900", "0.950", "0.975", "0.990")
    matrix = np.array(
        [
            [
                _mean(
                    int(row["family_size"])
                    for row in rows
                    if row["displayed_fidelity"] == fidelity
                    and row["displayed_jaccard_cutoff"] == "0.50"
                    and int(row["checkpoint_step"]) == step
                )
                for step in CHECKPOINT_STEPS
            ]
            for fidelity in fidelity_levels
        ]
    )
    image = axes[1].imshow(matrix, aspect="auto", cmap="magma", interpolation="nearest")
    axes[1].set(
        title="Mean family size across fidelity thresholds",
        xlabel="Checkpoint step",
        ylabel="Required fidelity",
        xticks=range(len(CHECKPOINT_STEPS)),
        xticklabels=[str(step) for step in CHECKPOINT_STEPS],
        yticks=range(len(fidelity_levels)),
        yticklabels=fidelity_levels,
    )
    axes[1].tick_params(axis="x", rotation=45)
    figure.colorbar(image, ax=axes[1], label="Mean family size", shrink=0.85)
    figure.suptitle("Figure 2. Circuit-family dynamics and fidelity sensitivity")
    outputs = _save(figure, output_dir, "figure2_family_dynamics")
    plt.close(figure)
    return outputs


def figure3(output_dir: Path) -> tuple[Path, Path]:
    rows = _rows(SOURCE_TABLES[2])
    final_step = CHECKPOINT_STEPS[-1]
    figure, axes = plt.subplots(2, 3, figsize=(12, 7.5), constrained_layout=True)
    flat_axes = axes.ravel()
    overlap_image = None
    for seed, axis in enumerate(flat_axes[:5]):
        primary_row = next(
            row
            for row in rows
            if row["record_type"] == "distinctness_sensitivity"
            and int(row["model_seed"]) == seed
            and int(row["checkpoint_step"]) == final_step
            and row["displayed_jaccard_cutoff"] == "0.50"
        )
        family_size = int(primary_row["family_size"])
        axis.set_title(f"Seed {seed}, step {final_step} (n={family_size} circuits)")
        if family_size == 0:
            axis.text(0.5, 0.5, "Empty family", transform=axis.transAxes, ha="center", va="center")
            axis.axis("off")
            continue
        matrix = np.eye(family_size)
        overlap_rows = [
            row
            for row in rows
            if row["record_type"] == "overlap_matrix" and int(row["model_seed"]) == seed
        ]
        for row in overlap_rows:
            left = int(row["circuit_i"][1:]) - 1
            right = int(row["circuit_j"][1:]) - 1
            value = float(row["jaccard_overlap"])
            matrix[left, right] = value
            matrix[right, left] = value
        overlap_image = axis.imshow(matrix, vmin=0, vmax=1, cmap="viridis")
        labels = [f"C{index}" for index in range(1, family_size + 1)]
        axis.set(
            xlabel="Circuit",
            ylabel="Circuit",
            xticks=range(family_size),
            xticklabels=labels,
            yticks=range(family_size),
            yticklabels=labels,
        )
    if overlap_image is not None:
        figure.colorbar(
            overlap_image,
            ax=flat_axes[:5].tolist(),
            label="Pairwise Jaccard overlap",
            shrink=0.65,
        )
    sensitivity_axis = flat_axes[5]
    for cutoff in ("0.25", "0.50", "0.75"):
        values = [
            _mean(
                int(row["family_size"])
                for row in rows
                if row["record_type"] == "distinctness_sensitivity"
                and row["displayed_jaccard_cutoff"] == cutoff
                and int(row["checkpoint_step"]) == step
            )
            for step in CHECKPOINT_STEPS
        ]
        sensitivity_axis.plot(
            range(len(CHECKPOINT_STEPS)),
            values,
            marker="o",
            label=f"cutoff {cutoff}",
        )
    sensitivity_axis.set(
        title="Distinctness sensitivity",
        xlabel="Checkpoint step",
        ylabel="Mean recovered family size",
        xticks=range(len(CHECKPOINT_STEPS)),
        xticklabels=[str(step) for step in CHECKPOINT_STEPS],
    )
    sensitivity_axis.tick_params(axis="x", rotation=45)
    sensitivity_axis.legend(frameon=False)
    figure.suptitle("Figure 3. Structural overlap and distinctness sensitivity")
    outputs = _save(figure, output_dir, "figure3_structural_sensitivity")
    plt.close(figure)
    return outputs


def figure4(output_dir: Path) -> tuple[Path, Path]:
    rows = _rows(SOURCE_TABLES[3])
    final_step = CHECKPOINT_STEPS[-1]
    matrix_rows = [row for row in rows if row["record_type"] == "functional_transfer_matrix"]
    transfer_values = [float(row["transfer_fidelity"]) for row in matrix_rows]
    figure, axes = plt.subplots(2, 3, figsize=(12, 7.5), constrained_layout=True)
    flat_axes = axes.ravel()
    transfer_image = None
    for seed, axis in enumerate(flat_axes[:5]):
        seed_rows = [row for row in matrix_rows if int(row["model_seed"]) == seed]
        group_row = next(
            row
            for row in rows
            if row["record_type"] == "transfer_group_trajectory"
            and int(row["model_seed"]) == seed
            and int(row["checkpoint_step"]) == final_step
        )
        groups = group_row["transfer_distinct_group_count"] or "undefined"
        axis.set_title(f"Seed {seed}, step {final_step} (groups={groups})")
        if not seed_rows:
            axis.text(0.5, 0.5, "Empty family", transform=axis.transAxes, ha="center", va="center")
            axis.axis("off")
            continue
        circuits = sorted(
            {row["circuit_id"] for row in seed_rows},
            key=lambda value: int(value[1:]),
        )
        matrix = np.array(
            [
                [
                    float(
                        next(
                            row["transfer_fidelity"]
                            for row in seed_rows
                            if row["circuit_id"] == circuit and row["test_subset"] == subset
                        )
                    )
                    for subset in ("q1", "q2", "q3", "q4")
                ]
                for circuit in circuits
            ]
        )
        transfer_image = axis.imshow(
            matrix,
            vmin=min(transfer_values),
            vmax=max(transfer_values),
            cmap="magma",
            aspect="auto",
        )
        axis.set(
            xlabel="Held-out test subset",
            ylabel="Circuit",
            xticks=range(4),
            xticklabels=("Q1", "Q2", "Q3", "Q4"),
            yticks=range(len(circuits)),
            yticklabels=circuits,
        )
    if transfer_image is not None:
        figure.colorbar(
            transfer_image,
            ax=flat_axes[:5].tolist(),
            label="Transfer fidelity",
            shrink=0.65,
        )
    group_axis = flat_axes[5]
    for seed in range(5):
        seed_rows = sorted(
            (
                row
                for row in rows
                if row["record_type"] == "transfer_group_trajectory"
                and int(row["model_seed"]) == seed
            ),
            key=lambda row: CHECKPOINT_STEPS.index(int(row["checkpoint_step"])),
        )
        values = [
            (
                np.nan
                if row["transfer_distinct_group_count"] == ""
                else float(row["transfer_distinct_group_count"])
            )
            for row in seed_rows
        ]
        group_axis.plot(range(len(CHECKPOINT_STEPS)), values, marker="o", label=f"seed {seed}")
    group_axis.set(
        title="Transfer-distinct group trajectories",
        xlabel="Checkpoint step",
        ylabel="Group count",
        xticks=range(len(CHECKPOINT_STEPS)),
        xticklabels=[str(step) for step in CHECKPOINT_STEPS],
    )
    group_axis.tick_params(axis="x", rotation=45)
    group_axis.legend(frameon=False, ncol=2)
    figure.suptitle("Figure 4. Functional transfer under the Q1–Q4 probe")
    outputs = _save(figure, output_dir, "figure4_transfer_dynamics")
    plt.close(figure)
    return outputs


def figure5(output_dir: Path) -> tuple[Path, Path]:
    rows = _rows(SOURCE_TABLES[4])
    figure, axis = plt.subplots(figsize=(10, 4.5), constrained_layout=True)
    for seed in range(5):
        seed_rows = sorted(
            (
                row
                for row in rows
                if row["condition"] == "genuine_task" and int(row["model_seed"]) == seed
            ),
            key=lambda row: CHECKPOINT_STEPS.index(int(row["checkpoint_step"])),
        )
        axis.plot(
            [CHECKPOINT_STEPS.index(int(row["checkpoint_step"])) for row in seed_rows],
            [int(row["family_size"]) for row in seed_rows],
            color="tab:blue",
            alpha=0.25,
            linewidth=1,
        )
    genuine_means = [
        _mean(
            int(row["family_size"])
            for row in rows
            if row["condition"] == "genuine_task" and int(row["checkpoint_step"]) == step
        )
        for step in CHECKPOINT_STEPS
    ]
    random_rows = sorted(
        (row for row in rows if row["condition"] == "random_label"),
        key=lambda row: CHECKPOINT_STEPS.index(int(row["checkpoint_step"])),
    )
    axis.plot(
        range(len(CHECKPOINT_STEPS)),
        genuine_means,
        marker="o",
        linewidth=2.5,
        label="Genuine task mean",
    )
    axis.plot(
        [CHECKPOINT_STEPS.index(int(row["checkpoint_step"])) for row in random_rows],
        [int(row["family_size"]) for row in random_rows],
        marker="s",
        linestyle="--",
        label="Random-label seed 0 (descriptive)",
    )
    axis.text(
        0.02,
        0.96,
        "Matched no-generalisation control: unavailable under the frozen protocol",
        transform=axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "0.7", "alpha": 0.9},
    )
    axis.set(
        title="Figure 5. Genuine-task models and available controls",
        xlabel="Checkpoint step",
        ylabel="Primary recovered family size",
        xticks=range(len(CHECKPOINT_STEPS)),
        xticklabels=[str(step) for step in CHECKPOINT_STEPS],
    )
    axis.tick_params(axis="x", rotation=45)
    axis.legend(frameon=False, loc="center left", bbox_to_anchor=(1.01, 0.5))
    outputs = _save(figure, output_dir, "figure5_controls")
    plt.close(figure)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "reproduction/generated/figures",
        help="Destination for regenerated PNG and PDF files.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    _verify_sources()
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    outputs = []
    for generator in (figure1, figure2, figure3, figure4, figure5):
        outputs.extend(generator(output_dir))
    print("Figure-source hashes: PASS")
    print(f"Regenerated {len(outputs)} files in {output_dir}")
    print("FIGURE REPRODUCTION: PASS")


if __name__ == "__main__":
    main()
