"""Verify the integrity and completeness of the deposited research artifact."""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE12_MANIFEST = ROOT / "manifests/stage12_diversity_stage12-diversity-s1-020ebf1b5814.json"
STAGE17_MANIFEST = ROOT / "manifests/stage17_sensitivity_stage17-sensitivity-s1-7801e7938531.json"
STAGE18_ARCHIVE_INDEX = ROOT / "results/archives/stage18-scaling-24a9adb84176/index.json"
STAGE18_REPRODUCTION = (
    ROOT / "manifests/stage18_reproduction_comparison_stage18-scaling-24a9adb84176.json"
)
STAGE22_MANIFEST = ROOT / "manifests/stage22_freeze_stage22-freeze-34241335dcf7.json"
DATASET_MANIFEST = ROOT / "manifests/dataset_modular-addition-dataset-s0-7ef9c73ff18f.json"


class VerificationError(RuntimeError):
    """Raised when an artifact check fails."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise VerificationError(f"missing file: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise VerificationError(f"expected a JSON object: {path.relative_to(ROOT)}")
    return value


def _rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise VerificationError(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _verify_hash(relative: str, expected: str) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise VerificationError(f"missing file: {relative}")
    actual = _sha256(path)
    if actual != expected:
        raise VerificationError(f"SHA-256 mismatch: {relative}")


def required_files() -> str:
    required = (
        "README.md",
        "CITATION.cff",
        "LICENSE",
        "LICENSE-DATA",
        "reproduction/REPRODUCE.md",
        "reproduction/PAPER_AVAILABILITY.md",
        "reproduction/verify_artifact.py",
        "reproduction/reproduce_reported_results.py",
        "reproduction/reproduce_figures.py",
        "reproduction/provenance.json",
        "reproduction/validation_log.txt",
        "pyproject.toml",
        "uv.lock",
        "results/tables/stage18_circuits.csv",
        "results/tables/stage21_figure_source_registry.csv",
    )
    missing = [relative for relative in required if not (ROOT / relative).is_file()]
    if missing:
        raise VerificationError("missing required files: " + ", ".join(missing))
    return "PASS"


def frozen_source_hashes() -> str:
    manifest = _json(STAGE22_MANIFEST)
    provenance = _json(ROOT / "reproduction/provenance.json")
    if provenance.get("frozen_analysis_snapshot_commit") != (
        "a55509537a70a225fedc5ce3a1c8236110974a6e"
    ):
        raise VerificationError("unexpected frozen analysis snapshot provenance")
    if provenance.get("analysis_freeze_manifest_sha256") != _sha256(STAGE22_MANIFEST):
        raise VerificationError("analysis-freeze manifest provenance hash mismatch")
    if manifest.get("analysis_frozen") is not True:
        raise VerificationError("analysis freeze flag is not true")
    for mapping_name in ("source_artifacts", "outputs"):
        mapping = manifest.get(mapping_name)
        if not isinstance(mapping, dict):
            raise VerificationError(f"missing Stage 22 {mapping_name}")
        for relative, expected in mapping.items():
            _verify_hash(str(relative), str(expected))
    implementation_commit = manifest.get("implementation_commit")
    if implementation_commit != provenance.get("recorded_analysis_implementation_commit"):
        raise VerificationError("unexpected source commit recorded by the analysis freeze")
    return "PASS"


def dataset() -> str:
    manifest = _json(DATASET_MANIFEST)
    outputs = manifest.get("output_paths")
    hashes = manifest.get("hashes")
    if not isinstance(outputs, dict) or not isinstance(hashes, dict):
        raise VerificationError("dataset manifest is incomplete")
    _verify_hash(str(outputs["dataset_archive"]), str(hashes["archive_sha256"]))
    _verify_hash(str(outputs["dataset_metadata"]), str(hashes["metadata_sha256"]))
    return "PASS"


def selected_checkpoints() -> str:
    rows = _rows(ROOT / "results/tables/stage18_checkpoint_registry.csv")
    rows.extend(_rows(ROOT / "results/tables/seed_0_stage14_random_label_checkpoints.csv"))
    paths = [row["checkpoint_path"] for row in rows]
    if len(paths) != 42 or len(set(paths)) != 42:
        raise VerificationError(
            "expected 42 unique selected checkpoints, "
            f"found {len(paths)} rows/{len(set(paths))} unique"
        )
    for row in rows:
        _verify_hash(row["checkpoint_path"], row["checkpoint_sha256"])
    return "PASS"


def _manifest_archive(manifest_path: Path) -> str:
    manifest = _json(manifest_path)
    outputs = manifest.get("outputs")
    if not isinstance(outputs, dict) or not isinstance(outputs.get("archive"), dict):
        raise VerificationError(f"archive record missing from {manifest_path.name}")
    archive = outputs["archive"]
    _verify_hash(str(archive["path"]), str(archive["sha256"]))
    return "PASS"


def stage12_archive() -> str:
    return _manifest_archive(STAGE12_MANIFEST)


def stage17_archive() -> str:
    return _manifest_archive(STAGE17_MANIFEST)


def stage18_archives() -> str:
    index = _json(STAGE18_ARCHIVE_INDEX)
    shards = index.get("shards")
    if not isinstance(shards, list) or len(shards) != 35:
        raise VerificationError(f"expected 35 archive records, found {len(shards or [])}")
    seen: set[tuple[int, int]] = set()
    for shard in shards:
        if not isinstance(shard, dict):
            raise VerificationError("invalid Stage 18 archive record")
        key = (int(shard["model_seed"]), int(shard["checkpoint_step"]))
        if key in seen:
            raise VerificationError(f"duplicate Stage 18 archive record: {key}")
        seen.add(key)
        _verify_hash(str(shard["path"]), str(shard["sha256"]))
        inventory = Path(str(shard["path"])).with_suffix("").with_suffix("")
        inventory_path = ROOT / f"{inventory}_inventory.json"
        record = _json(inventory_path)
        identity = (
            int(record.get("model_seed", -1)),
            int(record.get("checkpoint_step", -1)),
        )
        if identity != key:
            raise VerificationError(f"archive inventory identity mismatch: {inventory_path.name}")
        if len(record.get("members", [])) != int(shard["raw_file_count"]):
            raise VerificationError(f"archive member-count mismatch: {inventory_path.name}")
    return "PASS (35/35)"


def stage18_reproduction_record() -> str:
    record = _json(STAGE18_REPRODUCTION)
    if record.get("passed") is not True or record.get("stage18_reproduction_status") != "passed":
        raise VerificationError("independent reproduction record does not report PASS")
    if int(record.get("deterministic_mismatch_count", -1)) != 0:
        raise VerificationError("independent reproduction record contains deterministic mismatches")
    if int(record.get("archive_inventory_count", -1)) != 35:
        raise VerificationError("independent reproduction record does not cover 35 archives")
    log = record.get("comparison_log")
    if not isinstance(log, dict):
        raise VerificationError("independent reproduction comparison log record is missing")
    deposited_log = "reproduction/records/stage18_reproduction_comparison.log"
    _verify_hash(deposited_log, str(log["sha256"]))
    return "PASS"


def stage21_figure_sources() -> str:
    manifest = _json(STAGE22_MANIFEST)
    source_artifacts = manifest.get("source_artifacts")
    if not isinstance(source_artifacts, dict):
        raise VerificationError("Stage 22 source-artifact hashes are missing")
    figure_sources = {
        relative: expected
        for relative, expected in source_artifacts.items()
        if str(relative).startswith("results/tables/stage21_figure")
        and str(relative).endswith(".csv")
    }
    if len(figure_sources) != 6:
        raise VerificationError(
            f"expected five figure sources plus registry, found {len(figure_sources)}"
        )
    for relative, expected in figure_sources.items():
        _verify_hash(str(relative), str(expected))
    return "PASS"


def stage22_analysis_freeze() -> str:
    manifest = _json(STAGE22_MANIFEST)
    if not all(
        (
            manifest.get("analysis_frozen") is True,
            manifest.get("analysis_freeze_finalized") is True,
            manifest.get("stage18_reproduction_passed") is True,
            manifest.get("status") == "analysis_frozen",
        )
    ):
        raise VerificationError("Stage 22 freeze status is incomplete")
    return "PASS"


def main() -> None:
    checks: tuple[tuple[str, Callable[[], str]], ...] = (
        ("Required files", required_files),
        ("Frozen source hashes", frozen_source_hashes),
        ("Dataset", dataset),
        ("42 selected checkpoints", selected_checkpoints),
        ("Stage 12 archive", stage12_archive),
        ("Stage 17 archive", stage17_archive),
        ("Stage 18 archives", stage18_archives),
        ("Stage 18 reproduction record", stage18_reproduction_record),
        ("Stage 21 figure sources", stage21_figure_sources),
        ("Stage 22 analysis freeze", stage22_analysis_freeze),
    )
    print("Circuit Families artifact verification")
    print("=======================================")
    failed = False
    for label, check in checks:
        try:
            status = check()
        except Exception as error:  # report all independent failures in one audit pass
            status = f"FAIL ({error})"
            failed = True
        print(f"{label:<31} {status}")
    print()
    print(f"ARTIFACT VERIFICATION: {'FAIL' if failed else 'PASS'}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
