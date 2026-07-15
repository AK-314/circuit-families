"""Training, evaluation, device, and checkpoint utilities."""

from circuit_families.training.device import (
    device_record,
    resolve_device,
)
from circuit_families.training.metrics import (
    OUTPUT_CLASS_COUNT,
    classification_accuracy,
    cross_entropy_loss,
    evaluate_model,
    final_position_logits,
    gradient_norm,
    parameter_norm,
)
from circuit_families.training.trainer import (
    build_optimizer,
    train_full_batch_step,
)

__all__ = [
    "OUTPUT_CLASS_COUNT",
    "build_optimizer",
    "classification_accuracy",
    "cross_entropy_loss",
    "device_record",
    "evaluate_model",
    "final_position_logits",
    "gradient_norm",
    "parameter_norm",
    "resolve_device",
    "train_full_batch_step",
]
