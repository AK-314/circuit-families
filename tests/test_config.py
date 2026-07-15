"""Tests for configuration loading, validation, hashing, and run IDs."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from circuit_families.config import (
    ConfigError,
    canonical_config_json,
    config_hash,
    load_config,
    stable_run_id,
    validate_task_config,
)


def test_loads_frozen_task_config() -> None:
    config = load_config("configs/task.yaml")

    assert config["experiment_type"] == "modular_addition_dataset"
    assert config["task"]["modulus"] == 113
    assert config["split"]["seed"] == 0
    assert config["random_labels"]["seed"] == 1


def test_canonical_hash_is_independent_of_mapping_order() -> None:
    config = load_config("configs/task.yaml")

    reordered = {
        "outputs": config["outputs"],
        "random_labels": config["random_labels"],
        "split": config["split"],
        "task": config["task"],
        "experiment_type": config["experiment_type"],
        "schema_version": config["schema_version"],
    }

    assert canonical_config_json(config) == canonical_config_json(reordered)
    assert config_hash(config) == config_hash(reordered)


def test_relevant_config_change_changes_hash_and_run_id() -> None:
    config = load_config("configs/task.yaml")
    changed = deepcopy(config)
    changed["outputs"]["dataset_filename"] = "different-name.npz"

    assert config_hash(config) != config_hash(changed)

    original_run_id = stable_run_id(
        config["experiment_type"],
        config["split"]["seed"],
        config,
    )
    changed_run_id = stable_run_id(
        changed["experiment_type"],
        changed["split"]["seed"],
        changed,
    )

    assert original_run_id != changed_run_id


def test_stable_run_id_is_reproducible() -> None:
    config = load_config("configs/task.yaml")

    first = stable_run_id(
        config["experiment_type"],
        config["split"]["seed"],
        config,
    )
    second = stable_run_id(
        config["experiment_type"],
        config["split"]["seed"],
        config,
    )

    assert first == second
    assert first.startswith("modular-addition-dataset-s0-")


def test_missing_config_file_fails_clearly(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yaml"

    with pytest.raises(
        ConfigError,
        match="Configuration file does not exist",
    ):
        load_config(missing)


def test_malformed_yaml_fails_clearly(tmp_path: Path) -> None:
    malformed = tmp_path / "malformed.yaml"
    malformed.write_text("task: [\n", encoding="utf-8")

    with pytest.raises(ConfigError, match="Invalid YAML"):
        load_config(malformed)


def test_wrong_frozen_value_fails_clearly(tmp_path: Path) -> None:
    config = load_config("configs/task.yaml")
    config["task"]["modulus"] = 97

    malformed = tmp_path / "wrong-modulus.yaml"
    malformed.write_text(
        yaml.safe_dump(config, sort_keys=False),
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigError,
        match=r"task\.modulus must be 113",
    ):
        load_config(malformed)


def test_inconsistent_counts_fail_clearly() -> None:
    config = load_config("configs/task.yaml")
    config["split"]["primary_test_count"] = 8_938

    with pytest.raises(
        ConfigError,
        match="must be 8939",
    ):
        validate_task_config(config)
