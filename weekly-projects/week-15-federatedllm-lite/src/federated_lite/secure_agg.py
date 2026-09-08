from __future__ import annotations
import torch

def apply_canceling_masks(deltas, seed: int = 42):
    """Educational algebraic simulation only; not cryptographic secure aggregation."""
    if len(deltas) < 2:
        return [{k: v.clone() for k, v in deltas[0].items()}] if deltas else []
    masked = [{k: v.clone() for k, v in d.items()} for d in deltas]
    keys = list(deltas[0])
    for i in range(len(deltas) - 1):
        g = torch.Generator().manual_seed(seed + i)
        for k in keys:
            mask = torch.randn(deltas[i][k].shape, generator=g, dtype=deltas[i][k].dtype)
            masked[i][k] += mask; masked[i + 1][k] -= mask
    return masked
