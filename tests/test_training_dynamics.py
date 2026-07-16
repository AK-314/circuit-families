"""Tests for checkpoint-based training-dynamics diagnostics."""

from __future__ import annotations

import math

import pytest
import torch

from circuit_families.analysis.training_dynamics import (
    model_parameter_group_norms,
    optimizer_moment_norms,
    parameter_group,
)


def test_parameter_groups_are_disjoint_and_complete() -> None:
    assert parameter_group("embed.W_E") == "embedding"
    assert parameter_group("pos_embed.W_pos") == "positional_embedding"
    assert parameter_group("blocks.0.attn.W_Q") == "attention"
    assert parameter_group("blocks.0.mlp.W_in") == "mlp"
    assert parameter_group("unembed.W_U") == "unembedding"

    with pytest.raises(
        ValueError,
        match="Unclassified trainable parameter",
    ):
        parameter_group("unknown.weight")


def test_parameter_group_norms_are_calculated_without_double_counting() -> None:
    state = {
        "embed.W_E": torch.tensor([3.0, 4.0]),
        "pos_embed.W_pos": torch.tensor([12.0]),
        "blocks.0.attn.W_Q": torch.tensor([5.0]),
        "blocks.0.mlp.W_in": torch.tensor([8.0, 15.0]),
        "unembed.W_U": torch.tensor([7.0, 24.0]),
        "blocks.0.attn.mask": torch.empty((0, 0)),
        "blocks.0.attn.IGNORE": torch.tensor(0.0),
    }

    norms = model_parameter_group_norms(state)

    assert norms["embedding_parameter_norm"] == 5.0
    assert norms["positional_embedding_norm"] == 12.0
    assert norms["attention_parameter_norm"] == 5.0
    assert norms["mlp_parameter_norm"] == 17.0
    assert norms["unembedding_parameter_norm"] == 25.0

    expected_total = math.sqrt(
        5.0**2
        + 12.0**2
        + 5.0**2
        + 17.0**2
        + 25.0**2
    )

    assert norms["total_parameter_norm"] == expected_total


def test_optimizer_moment_norms_are_extracted_correctly() -> None:
    optimizer_state = {
        "state": {
            0: {
                "exp_avg": torch.tensor([3.0, 4.0]),
                "exp_avg_sq": torch.tensor([5.0, 12.0]),
                "step": torch.tensor(1.0),
            },
            1: {
                "exp_avg": torch.tensor([12.0]),
                "exp_avg_sq": torch.tensor([84.0]),
                "step": torch.tensor(1.0),
            },
        },
        "param_groups": [],
    }

    first, second = optimizer_moment_norms(optimizer_state)

    assert first == 13.0
    assert second == 85.0


def test_empty_optimizer_state_has_zero_moment_norms() -> None:
    first, second = optimizer_moment_norms(
        {
            "state": {},
            "param_groups": [],
        }
    )

    assert first == 0.0
    assert second == 0.0
