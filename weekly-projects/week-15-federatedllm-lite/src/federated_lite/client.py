from __future__ import annotations
from dataclasses import dataclass
import copy
import torch
from torch import nn
from torch.utils.data import DataLoader
from .model import adapter_state, load_adapter_state
from .privacy import subtract_states, clip_update, add_gaussian_noise

@dataclass
class ClientResult:
    client_id: int
    num_examples: int
    delta: dict[str, torch.Tensor]
    train_loss: float
    pre_clip_norm: float
    clip_scale: float

def train_client(client_id, model_template, global_adapter, dataset, local_epochs, batch_size, learning_rate, weight_decay, device, privacy_enabled, max_update_norm, noise_multiplier, seed):
    model = copy.deepcopy(model_template).to(device); load_adapter_state(model, global_adapter); model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=learning_rate, weight_decay=weight_decay)
    criterion = nn.CrossEntropyLoss(); loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    losses = []; torch.manual_seed(seed + client_id)
    for _ in range(local_epochs):
        for x, y in loader:
            x, y = x.to(device), y.to(device); optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(x), y); loss.backward(); torch.nn.utils.clip_grad_norm_(params, max_norm=5.0); optimizer.step()
            losses.append(float(loss.detach().cpu()))
    delta = subtract_states(adapter_state(model), global_adapter)
    clipped, pre_norm, clip_scale = clip_update(delta, max_update_norm)
    if not privacy_enabled: clipped, clip_scale = delta, 1.0
    if privacy_enabled and noise_multiplier > 0:
        g = torch.Generator().manual_seed(seed * 1000 + client_id)
        clipped = add_gaussian_noise(clipped, noise_multiplier * max_update_norm, g)
    return ClientResult(client_id, len(dataset), clipped, sum(losses)/max(1,len(losses)), pre_norm, clip_scale)
