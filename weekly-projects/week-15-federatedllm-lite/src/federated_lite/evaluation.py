from __future__ import annotations
import copy
import torch
from torch.utils.data import DataLoader
from .model import load_adapter_state

@torch.inference_mode()
def evaluate(model_template, adapter, dataset, device, batch_size: int = 16):
    model = copy.deepcopy(model_template).to(device); load_adapter_state(model, adapter); model.eval()
    correct = total = 0
    for x, y in DataLoader(dataset, batch_size=batch_size, shuffle=False):
        x, y = x.to(device), y.to(device); pred = model(x).argmax(dim=-1)
        correct += int((pred == y).sum()); total += int(y.numel())
    return correct / max(1, total)
