from __future__ import annotations
import math
import torch

def subtract_states(new, old): return {k: new[k] - old[k] for k in old}
def add_states(base, delta): return {k: base[k] + delta[k] for k in base}
def l2_norm(delta): return math.sqrt(sum(float((v.float() ** 2).sum()) for v in delta.values()))

def clip_update(delta, max_norm: float):
    norm = l2_norm(delta); scale = min(1.0, max_norm / max(norm, 1e-12))
    return {k: v * scale for k, v in delta.items()}, norm, scale

def add_gaussian_noise(delta, std: float, generator: torch.Generator):
    if std <= 0: return {k: v.clone() for k, v in delta.items()}
    return {k: v + torch.randn(v.shape, generator=generator, dtype=v.dtype) * std for k, v in delta.items()}
