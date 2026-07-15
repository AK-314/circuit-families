"""End-to-end execution of frozen modular-addition training runs."""

from __future__ import annotations

import copy
import json
import shutil
import sys
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import torch

from circuit_families.config import (
    combined_config_hash,
    config_hash,
    load_config,
    load_model_config,
    load_training_config,
    mapping_hash,
    stable_run_id_from_hash,
    validate_training_config,
)
from circuit_families.manifests import (
    git_commit,
    package_versions,
    utc_timestamp,
    write_manifest,
)
from circuit_families.models.transformer import build_transformer
from circuit_families.training.checkpoints import (
    CHECKPOINT_PACKAGES,
    SavedCheckpoint,
    file_sha256,
    reload_and_reevaluate,
    save_checkpoint,
)
from circuit_families.training.data import (
    TrainingData,
    load_training_data,
)
from circuit_families.training.device import (
    device_record,
    resolve_device,
)
from circuit_families.training.logging import append_jsonl
from circuit_families.training.metrics import (
    evaluate_model,
    parameter_norm,
)
from circuit_families.training.trainer import (
    build_optimizer,
    train_full_batch_step,
)


@dataclass(frozen=True)
class ExecutionPlan:
    """Effective immutable schedule for one training invocation."""

    mode: str
    max_steps: int
    evaluation_interval: int
    checkpoint_interval: int
    evaluate_step_zero: bool
    checkpoint_step_zero: bool
    checkpoint_final_step: bool


@dataclass(frozen=True)
class TrainingRunResult:
    """Paths and identifiers produced by a completed training run."""

    run_id: str
    mode: str
    device: str
    metrics_path: Path
    manifest_path: Path
    checkpoint_directory: Path
    checkpoint_count: int
    final_step: int
    combined_config_sha256: str


def build_execution_plan(
    training_config: Mapping[str, Any],
    *,
    smoke: bool,
) -> ExecutionPlan:
    """Build the frozen full-run or smoke-run schedule."""

    validate_training_config(training_config)
    training = training_config["training"]

    if smoke:
        smoke_config = training_config["smoke"]
        return ExecutionPlan(
            mode="smoke",
            max_steps=smoke_config["steps"],
            evaluation_interval=smoke_config["evaluation_interval"],
            checkpoint_interval=smoke_config["checkpoint_interval"],
            evaluate_step_zero=training["evaluate_step_zero"],
            checkpoint_step_zero=training["checkpoint_step_zero"],
            checkpoint_final_step=training["checkpoint_final_step"],
        )

    return ExecutionPlan(
        mode="full",
        max_steps=training["max_steps"],
        evaluation_interval=training["evaluation_interval"],
        checkpoint_interval=training["checkpoint_interval"],
        evaluate_step_zero=training["evaluate_step_zero"],
        checkpoint_step_zero=training["checkpoint_step_zero"],
        checkpoint_final_step=training["checkpoint_final_step"],
    )


def _resolve_path(root: Path, path: str | Path) -> Path:
    candidate = Path(path)

    if candidate.is_absolute():
        return candidate

    return root / candidate


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _event_due(
    step: int,
    *,
    interval: int,
    include_step_zero: bool,
    final_step: int,
    include_final: bool,
) -> bool:
    if step == 0:
        return include_step_zero

    if step % interval == 0:
        return True

    return include_final and step == final_step


def _evaluation_metrics(
    model: torch.nn.Module,
    data: TrainingData,
) -> dict[str, dict[str, float]]:
    return {
        "train": evaluate_model(
            model,
            data.train_inputs,
            data.train_targets,
        ),
        "test": evaluate_model(
            model,
            data.test_inputs,
            data.test_targets,
        ),
    }


def _clear_device_cache(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.empty_cache()
    elif device.type == "mps" and hasattr(torch, "mps"):
        torch.mps.empty_cache()


def _prepare_output_paths(
    *,
    output_root: Path,
    training_config: Mapping[str, Any],
    run_id: str,
    overwrite: bool,
) -> tuple[Path, Path, Path]:
    outputs = training_config["outputs"]

    checkpoint_directory = (
        output_root
        / outputs["checkpoint_directory"]
        / run_id
    )
    results_directory = (
        output_root
        / outputs["results_directory"]
        / run_id
    )
    manifest_path = (
        output_root
        / outputs["manifest_directory"]
        / f"training_{run_id}.json"
    )

    existing = [
        path
        for path in (
            checkpoint_directory,
            results_directory,
            manifest_path,
        )
        if path.exists()
    ]

    if existing and not overwrite:
        formatted = ", ".join(str(path) for path in existing)
        raise FileExistsError(
            "Training outputs already exist: "
            f"{formatted}. Use overwrite=True to replace them."
        )

    if overwrite:
        shutil.rmtree(checkpoint_directory, ignore_errors=True)
        shutil.rmtree(results_directory, ignore_errors=True)
        manifest_path.unlink(missing_ok=True)

    checkpoint_directory.mkdir(parents=True, exist_ok=True)
    results_directory.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    return checkpoint_directory, results_directory, manifest_path


def _verify_checkpoints(
    *,
    checkpoints: list[tuple[int, SavedCheckpoint]],
    model_config: Mapping[str, Any],
    training_config: Mapping[str, Any],
    model_seed: int,
    device: torch.device,
    data: TrainingData,
) -> None:
    validation = training_config["validation"]

    for _, saved in checkpoints:
        verification_model = build_transformer(
            model_config,
            seed=model_seed,
            device=device,
        )
        verification_optimizer = build_optimizer(
            verification_model,
            training_config,
        )

        reload_and_reevaluate(
            saved.path,
            model=verification_model,
            optimizer=verification_optimizer,
            device=device,
            train_inputs=data.train_inputs,
            train_targets=data.train_targets,
            test_inputs=data.test_inputs,
            test_targets=data.test_targets,
            absolute_tolerance=validation[
                "reload_metric_absolute_tolerance"
            ],
            relative_tolerance=validation[
                "reload_metric_relative_tolerance"
            ],
        )

        del verification_optimizer
        del verification_model
        _clear_device_cache(device)


def _write_training_manifest(
    *,
    path: Path,
    repository_root: Path,
    output_root: Path,
    run_id: str,
    experiment_type: str,
    model_seed: int,
    device: torch.device,
    plan: ExecutionPlan,
    task_config_path: Path,
    model_config_path: Path,
    training_config_path: Path,
    task_config_sha256: str,
    model_config_sha256: str,
    training_config_sha256: str,
    combined_config_sha256: str,
    data: TrainingData,
    metrics_path: Path,
    checkpoint_directory: Path,
    checkpoints: list[tuple[int, SavedCheckpoint]],
    final_record: Mapping[str, Any],
) -> Path:
    checkpoint_records = [
        {
            "training_step": step,
            "path": _display_path(saved.path, output_root),
            "file_sha256": saved.file_sha256,
            "model_state_sha256": saved.model_state_sha256,
            "optimizer_state_sha256": (
                saved.optimizer_state_sha256
            ),
            "reload_verified": True,
        }
        for step, saved in checkpoints
    ]

    manifest = {
        "schema_version": 1,
        "timestamp_utc": utc_timestamp(),
        "run_id": run_id,
        "experiment_type": experiment_type,
        "mode": plan.mode,
        "git_commit": git_commit(repository_root),
        "configs": {
            "task": {
                "path": _display_path(
                    task_config_path,
                    repository_root,
                ),
                "sha256": task_config_sha256,
            },
            "model": {
                "path": _display_path(
                    model_config_path,
                    repository_root,
                ),
                "sha256": model_config_sha256,
            },
            "training": {
                "path": _display_path(
                    training_config_path,
                    repository_root,
                ),
                "sha256": training_config_sha256,
            },
            "combined_sha256": combined_config_sha256,
        },
        "software": {
            "python": sys.version,
            "packages": package_versions(CHECKPOINT_PACKAGES),
        },
        "device": device_record(device),
        "seed": {
            "name": "model_seed",
            "value": model_seed,
        },
        "execution": asdict(plan),
        "dataset": {
            "archive_path": _display_path(
                data.archive_path,
                repository_root,
            ),
            "metadata_path": _display_path(
                data.metadata_path,
                repository_root,
            ),
            "manifest_path": _display_path(
                data.manifest_path,
                repository_root,
            ),
            "archive_sha256": data.archive_sha256,
            "metadata_sha256": data.metadata_sha256,
            "canonical_hashes": copy.deepcopy(
                data.dataset_hashes
            ),
            "total_count": data.total_count,
            "train_count": data.train_count,
            "test_count": data.test_count,
        },
        "output_paths": {
            "metrics_jsonl": _display_path(
                metrics_path,
                output_root,
            ),
            "checkpoint_directory": _display_path(
                checkpoint_directory,
                output_root,
            ),
            "training_manifest": _display_path(
                path,
                output_root,
            ),
        },
        "hashes": {
            "combined_config_sha256": combined_config_sha256,
            "metrics_jsonl_sha256": file_sha256(metrics_path),
        },
        "checkpoints": checkpoint_records,
        "final_metrics": dict(final_record),
        "acceptance": {
            "checkpoint_reload_verification": "passed",
            "verified_checkpoint_count": len(checkpoints),
        },
    }

    json.dumps(manifest, allow_nan=False)
    return write_manifest(path, manifest)


def run_training(
    *,
    repository_root: str | Path,
    task_config_path: str | Path,
    model_config_path: str | Path,
    training_config_path: str | Path,
    dataset_archive_path: str | Path,
    dataset_metadata_path: str | Path,
    dataset_manifest_path: str | Path,
    model_seed: int,
    smoke: bool,
    device_override: str | None = None,
    output_root: str | Path | None = None,
    overwrite: bool = False,
) -> TrainingRunResult:
    """Execute a complete frozen training or smoke run."""

    repository = Path(repository_root).resolve()
    output = (
        repository
        if output_root is None
        else Path(output_root).resolve()
    )

    resolved_task_config = _resolve_path(
        repository,
        task_config_path,
    )
    resolved_model_config = _resolve_path(
        repository,
        model_config_path,
    )
    resolved_training_config = _resolve_path(
        repository,
        training_config_path,
    )
    resolved_archive = _resolve_path(
        repository,
        dataset_archive_path,
    )
    resolved_metadata = _resolve_path(
        repository,
        dataset_metadata_path,
    )
    resolved_dataset_manifest = _resolve_path(
        repository,
        dataset_manifest_path,
    )

    task_config = load_config(resolved_task_config)
    model_config = load_model_config(resolved_model_config)
    training_config = load_training_config(
        resolved_training_config
    )
    plan = build_execution_plan(
        training_config,
        smoke=smoke,
    )

    configured_override = training_config["device"]["override"]
    requested_device = (
        device_override
        if device_override is not None
        else configured_override
    )
    device = resolve_device(requested_device)

    data = load_training_data(
        archive_path=resolved_archive,
        metadata_path=resolved_metadata,
        manifest_path=resolved_dataset_manifest,
        task_config=task_config,
        device=device,
    )

    task_config_sha256 = config_hash(task_config)
    model_config_sha256 = mapping_hash(model_config)
    training_config_sha256 = mapping_hash(training_config)

    execution_mapping = asdict(plan)
    combined_sha256 = combined_config_hash(
        {
            "task": task_config,
            "model": model_config,
            "training": training_config,
            "execution": execution_mapping,
        }
    )

    experiment_type = training_config["experiment_type"]
    if smoke:
        experiment_type = f"{experiment_type}_smoke"

    run_id = stable_run_id_from_hash(
        experiment_type,
        model_seed,
        combined_sha256,
    )

    (
        checkpoint_directory,
        results_directory,
        manifest_path,
    ) = _prepare_output_paths(
        output_root=output,
        training_config=training_config,
        run_id=run_id,
        overwrite=overwrite,
    )

    metrics_path = results_directory / "metrics.jsonl"

    model = build_transformer(
        model_config,
        seed=model_seed,
        device=device,
    )
    optimizer = build_optimizer(model, training_config)

    saved_checkpoints: list[tuple[int, SavedCheckpoint]] = []
    last_gradient_norm: float | None = None
    final_record: dict[str, Any] | None = None

    for step in range(plan.max_steps + 1):
        if step > 0:
            step_metrics = train_full_batch_step(
                model,
                optimizer,
                data.train_inputs,
                data.train_targets,
            )
            last_gradient_norm = step_metrics["gradient_norm"]

        evaluation_due = _event_due(
            step,
            interval=plan.evaluation_interval,
            include_step_zero=plan.evaluate_step_zero,
            final_step=plan.max_steps,
            include_final=True,
        )
        checkpoint_due = _event_due(
            step,
            interval=plan.checkpoint_interval,
            include_step_zero=plan.checkpoint_step_zero,
            final_step=plan.max_steps,
            include_final=plan.checkpoint_final_step,
        )

        if not evaluation_due and not checkpoint_due:
            continue

        metrics = _evaluation_metrics(model, data)
        weight_norm = parameter_norm(model)
        learning_rate = float(
            optimizer.param_groups[0]["lr"]
        )

        checkpoint_metrics = {
            **metrics,
            "training_step": step,
            "learning_rate": learning_rate,
            "weight_norm": weight_norm,
            "gradient_norm": last_gradient_norm,
        }

        saved: SavedCheckpoint | None = None

        if checkpoint_due:
            saved = save_checkpoint(
                checkpoint_directory,
                model=model,
                optimizer=optimizer,
                step=step,
                model_config=model_config,
                training_config=training_config,
                model_seed=model_seed,
                dataset_hashes=data.dataset_hashes,
                metrics=checkpoint_metrics,
                repository_root=repository,
                device=device,
            )
            saved_checkpoints.append((step, saved))

        record = {
            "schema_version": 1,
            "run_id": run_id,
            "mode": plan.mode,
            "training_step": step,
            "learning_rate": learning_rate,
            "weight_norm": weight_norm,
            "gradient_norm": last_gradient_norm,
            "train_loss": metrics["train"]["cross_entropy"],
            "test_loss": metrics["test"]["cross_entropy"],
            "train_accuracy": metrics["train"]["accuracy"],
            "test_accuracy": metrics["test"]["accuracy"],
            "checkpoint_path": (
                None
                if saved is None
                else _display_path(saved.path, output)
            ),
            "checkpoint_sha256": (
                None
                if saved is None
                else saved.file_sha256
            ),
            "model_state_sha256": (
                None
                if saved is None
                else saved.model_state_sha256
            ),
            "optimizer_state_sha256": (
                None
                if saved is None
                else saved.optimizer_state_sha256
            ),
        }

        append_jsonl(metrics_path, record)
        final_record = record

    if final_record is None:
        raise RuntimeError("Training produced no evaluation records.")

    _verify_checkpoints(
        checkpoints=saved_checkpoints,
        model_config=model_config,
        training_config=training_config,
        model_seed=model_seed,
        device=device,
        data=data,
    )

    _write_training_manifest(
        path=manifest_path,
        repository_root=repository,
        output_root=output,
        run_id=run_id,
        experiment_type=experiment_type,
        model_seed=model_seed,
        device=device,
        plan=plan,
        task_config_path=resolved_task_config,
        model_config_path=resolved_model_config,
        training_config_path=resolved_training_config,
        task_config_sha256=task_config_sha256,
        model_config_sha256=model_config_sha256,
        training_config_sha256=training_config_sha256,
        combined_config_sha256=combined_sha256,
        data=data,
        metrics_path=metrics_path,
        checkpoint_directory=checkpoint_directory,
        checkpoints=saved_checkpoints,
        final_record=final_record,
    )

    return TrainingRunResult(
        run_id=run_id,
        mode=plan.mode,
        device=str(device),
        metrics_path=metrics_path,
        manifest_path=manifest_path,
        checkpoint_directory=checkpoint_directory,
        checkpoint_count=len(saved_checkpoints),
        final_step=plan.max_steps,
        combined_config_sha256=combined_sha256,
    )
