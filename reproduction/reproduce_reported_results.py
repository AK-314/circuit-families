"""Recalculate headline reported results from deposited lower-level records."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY_TABLE = ROOT / "results/tables/stage18_family_summary.csv"
TRAINING_MANIFEST = ROOT / "manifests/stage18_training.json"
EXPECTED_PHASE_COUNTS = {
    "delayed": (0, 162),
    "transition": (30, 198),
    "stable-post": (270, 270),
}
EXPECTED_PRIMARY_CHANGES = (6, 7, 7, 0, 7)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _phase(step: int, *, first_ten_percent_step: int, stable_post_step: int) -> str:
    if step < first_ten_percent_step:
        return "delayed"
    if step < stable_post_step:
        return "transition"
    return "stable-post"


def _two_sided_exact_sign_probability(changes: list[int]) -> float:
    nonzero = [value for value in changes if value != 0]
    positives = sum(value > 0 for value in nonzero)
    negatives = len(nonzero) - positives
    tail = min(positives, negatives)
    probability = 2 * sum(math.comb(len(nonzero), k) for k in range(tail + 1)) / 2 ** len(nonzero)
    return min(1.0, probability)


def recalculate() -> dict[str, object]:
    family_rows = _read_csv(FAMILY_TABLE)
    training = json.loads(TRAINING_MANIFEST.read_text(encoding="utf-8"))
    landmarks = {
        int(run["model_seed"]): (
            int(run["first_ten_percent_test_step"]),
            int(run["stable_post_step"]),
        )
        for run in training["runs"]
    }

    phase_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    primary_by_seed: dict[int, dict[int, int]] = defaultdict(dict)
    for row in family_rows:
        seed = int(row["model_seed"])
        step = int(row["checkpoint_step"])
        first_ten_percent_step, stable_post_step = landmarks[seed]
        phase = _phase(
            step,
            first_ten_percent_step=first_ten_percent_step,
            stable_post_step=stable_post_step,
        )
        phase_counts[phase][1] += 1
        phase_counts[phase][0] += int(row["family_size"]) > 0
        if row["displayed_fidelity"] == "0.990" and row["displayed_jaccard_cutoff"] == "0.50":
            primary_by_seed[seed][step] = int(row["family_size"])

    checkpoint_steps = sorted({step for values in primary_by_seed.values() for step in values})
    first_step, final_step = checkpoint_steps[0], checkpoint_steps[-1]
    primary_changes = [
        primary_by_seed[seed][final_step] - primary_by_seed[seed][first_step]
        for seed in sorted(primary_by_seed)
    ]
    primary_seed_values = [
        {
            "model_seed": seed,
            "delayed_checkpoint_step": first_step,
            "delayed_family_size": primary_by_seed[seed][first_step],
            "stable_post_checkpoint_step": final_step,
            "stable_post_family_size": primary_by_seed[seed][final_step],
            "change": primary_by_seed[seed][final_step] - primary_by_seed[seed][first_step],
        }
        for seed in sorted(primary_by_seed)
    ]
    result = {
        "sensitivity_cell_count": len(family_rows),
        "phase_recovery_counts": {
            phase: {"recovered": values[0], "tested": values[1]}
            for phase, values in phase_counts.items()
        },
        "primary_seed_changes": primary_changes,
        "primary_seed_values": primary_seed_values,
        "median_change": statistics.median(primary_changes),
        "mean_change": statistics.mean(primary_changes),
        "sign_test_p": _two_sided_exact_sign_probability(primary_changes),
        "sign_test_zero_handling": "zeros reported but excluded",
    }
    return result


def _write_tables(result: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    phase_path = output_dir / "phase_recovery_summary.csv"
    phase_counts = result["phase_recovery_counts"]
    with phase_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("phase", "recovered_cell_count", "tested_cell_count"),
        )
        writer.writeheader()
        for phase in ("delayed", "transition", "stable-post"):
            writer.writerow(
                {
                    "phase": phase,
                    "recovered_cell_count": phase_counts[phase]["recovered"],
                    "tested_cell_count": phase_counts[phase]["tested"],
                }
            )

    seed_path = output_dir / "primary_seed_changes.csv"
    seed_values = result["primary_seed_values"]
    with seed_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(seed_values[0]))
        writer.writeheader()
        writer.writerows(seed_values)
    return phase_path, seed_path


def _matches_reported(result: dict[str, object]) -> bool:
    phase_counts = result["phase_recovery_counts"]
    assert isinstance(phase_counts, dict)
    observed = {
        phase: (int(values["recovered"]), int(values["tested"]))
        for phase, values in phase_counts.items()
    }
    return (
        result["sensitivity_cell_count"] == 630
        and observed == EXPECTED_PHASE_COUNTS
        and tuple(result["primary_seed_changes"]) == EXPECTED_PRIMARY_CHANGES
        and result["median_change"] == 7
        and math.isclose(float(result["mean_change"]), 5.4)
        and math.isclose(float(result["sign_test_p"]), 0.125)
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recalculate headline results from deposited lower-level records."
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "reproduction/generated/tables",
        help="Destination for independently recalculated summary tables.",
    )
    args = parser.parse_args()
    result = recalculate()
    output_paths = _write_tables(result, args.output_dir.resolve())
    passed = _matches_reported(result)
    if args.json:
        payload = {**result, "reported_value_check": "PASS" if passed else "FAIL"}
        print(json.dumps(payload, indent=2))
    else:
        counts = result["phase_recovery_counts"]
        changes = result["primary_seed_changes"]
        print("Circuit Families reported-result recalculation")
        print("================================================")
        print(f"Sensitivity cells: {result['sensitivity_cell_count']}")
        print()
        for phase in ("delayed", "transition", "stable-post"):
            values = counts[phase]
            print(f"{phase:<12} {values['recovered']:>3} / {values['tested']}")
        print()
        displayed_changes = ", ".join(
            "0" if value == 0 else f"{value:+d}" for value in changes
        )
        print("Primary seed changes: " + displayed_changes)
        print(f"Median change: {result['median_change']:+g}")
        print(f"Mean change: {result['mean_change']:+g}")
        print(f"Exact two-sided sign test: p = {result['sign_test_p']:.3f}")
        print(f"Recalculated tables: {', '.join(str(path) for path in output_paths)}")
        print()
        print(f"REPORTED-VALUE CHECK: {'PASS' if passed else 'FAIL'}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
