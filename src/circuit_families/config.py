"""Load, validate, and identify experiment configurations."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when a configuration is missing or invalid."""


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ConfigError(f"{field} must be a mapping.")
    return value


def _require(
    mapping: Mapping[str, Any],
    key: str,
    expected: Any,
    section: str,
) -> None:
    if key not in mapping:
        raise ConfigError(f"Missing required field: {section}.{key}")

    actual = mapping[key]
    if actual != expected:
        raise ConfigError(
            f"{section}.{key} must be {expected!r}; received {actual!r}."
        )


def load_config(path: str | Path) -> dict[str, Any]:
    """Load and validate a YAML configuration file."""

    config_path = Path(path)

    if not config_path.is_file():
        raise ConfigError(f"Configuration file does not exist: {config_path}")

    try:
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {config_path}: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"Could not read {config_path}: {exc}") from exc

    config = dict(_mapping(loaded, "configuration"))
    validate_task_config(config)
    return config


def validate_task_config(config: Mapping[str, Any]) -> None:
    """Validate the frozen modular-addition dataset configuration."""

    root = _mapping(config, "configuration")

    _require(root, "schema_version", 1, "configuration")
    _require(
        root,
        "experiment_type",
        "modular_addition_dataset",
        "configuration",
    )

    task = _mapping(root.get("task"), "task")
    _require(task, "name", "modular_addition", "task")
    _require(task, "modulus", 113, "task")
    _require(task, "pair_order", "lexicographic", "task")
    _require(task, "equals_token_id", 113, "task")
    _require(task, "expected_pair_count", 12_769, "task")

    split = _mapping(root.get("split"), "split")
    _require(split, "generator", "PCG64", "split")
    _require(split, "seed", 0, "split")
    _require(split, "primary_train_fraction", 0.30, "split")
    _require(split, "primary_train_count", 3_830, "split")
    _require(split, "primary_test_count", 8_939, "split")
    _require(
        split,
        "control_train_fractions",
        [0.05, 0.10, 0.15, 0.20, 0.25],
        "split",
    )

    random_labels = _mapping(root.get("random_labels"), "random_labels")
    _require(random_labels, "generator", "PCG64", "random_labels")
    _require(random_labels, "seed", 1, "random_labels")
    _require(
        random_labels,
        "method",
        "permute_complete_true_label_vector",
        "random_labels",
    )

    outputs = _mapping(root.get("outputs"), "outputs")
    for key in (
        "data_directory",
        "manifest_directory",
        "dataset_filename",
        "metadata_filename",
    ):
        value = outputs.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"outputs.{key} must be a non-empty string.")

    modulus = task["modulus"]
    pair_count = task["expected_pair_count"]
    train_count = split["primary_train_count"]
    test_count = split["primary_test_count"]

    if pair_count != modulus**2:
        raise ConfigError(
            "task.expected_pair_count must equal task.modulus squared."
        )

    if train_count + test_count != pair_count:
        raise ConfigError(
            "split.primary_train_count plus split.primary_test_count "
            "must equal task.expected_pair_count."
        )


def canonical_config_json(config: Mapping[str, Any]) -> str:
    """Return the configuration in stable canonical JSON form."""

    validate_task_config(config)

    return json.dumps(
        config,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def config_hash(config: Mapping[str, Any]) -> str:
    """Return the SHA-256 hash of the canonical configuration."""

    canonical = canonical_config_json(config).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def stable_run_id(
    experiment_type: str,
    seed: int,
    config: Mapping[str, Any],
) -> str:
    """Derive a stable run ID from experiment type, seed, and config."""

    if not isinstance(experiment_type, str) or not experiment_type.strip():
        raise ConfigError("experiment_type must be a non-empty string.")

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ConfigError("seed must be an integer.")

    if seed < 0:
        raise ConfigError("seed must be non-negative.")

    slug = re.sub(r"[^a-z0-9]+", "-", experiment_type.lower()).strip("-")
    if not slug:
        raise ConfigError(
            "experiment_type must contain an alphanumeric character."
        )

    return f"{slug}-s{seed}-{config_hash(config)[:12]}"
