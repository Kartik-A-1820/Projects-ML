from __future__ import annotations
import math
import torch
from torch import nn

class LoRALinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 8.0):
        super().__init__()
        self.base = nn.Linear(in_features, out_features)
        for p in self.base.parameters():
            p.requires_grad = False
        self.rank = rank
        self.scaling = alpha / rank
        self.lora_a = nn.Parameter(torch.empty(rank, in_features))
        self.lora_b = nn.Parameter(torch.zeros(out_features, rank))
        nn.init.kaiming_uniform_(self.lora_a, a=math.sqrt(5))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base = self.base(x)
        adapter = (x @ self.lora_a.t()) @ self.lora_b.t()
        return base + adapter * self.scaling

class TinyTextModel(nn.Module):
    def __init__(self, vocab_size: int = 512, embedding_dim: int = 48, hidden_dim: int = 32, num_classes: int = 4, lora_rank: int = 4, lora_alpha: float = 8.0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        for p in self.embedding.parameters():
            p.requires_grad = False
        self.proj = LoRALinear(embedding_dim, hidden_dim, lora_rank, lora_alpha)
        self.activation = nn.Tanh()
        self.head = LoRALinear(hidden_dim, num_classes, lora_rank, lora_alpha)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        mask = (token_ids != 0).float().unsqueeze(-1)
        embedded = self.embedding(token_ids)
        pooled = (embedded * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1.0)
        return self.head(self.activation(self.proj(pooled)))

def adapter_state(model: nn.Module) -> dict[str, torch.Tensor]:
    return {name: p.detach().cpu().clone() for name, p in model.named_parameters() if "lora_" in name}

def load_adapter_state(model: nn.Module, state: dict[str, torch.Tensor]) -> None:
    named = dict(model.named_parameters())
    for name, value in state.items():
        if name not in named:
            raise KeyError(f"missing adapter parameter: {name}")
        named[name].data.copy_(value.to(named[name].device))

def trainable_parameter_count(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
