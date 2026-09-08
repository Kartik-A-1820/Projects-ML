from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset
from .tokenizer import HashTokenizer

LABELS = ["payment", "refund", "account", "shipping"]
LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}

class TextDataset(Dataset):
    def __init__(self, rows: list[dict], tokenizer: HashTokenizer):
        self.rows = rows
        self.tokenizer = tokenizer
    def __len__(self): return len(self.rows)
    def __getitem__(self, idx):
        row = self.rows[idx]
        return self.tokenizer.encode(row["text"]), torch.tensor(LABEL_TO_ID[row["label"]], dtype=torch.long)

def load_rows(path: str) -> list[dict]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    for row in rows:
        if row["label"] not in LABEL_TO_ID: raise ValueError(f"unknown label {row['label']}")
    return rows

def stratified_holdout(rows: list[dict], validation_fraction: float = 0.25, seed: int = 42):
    rng = np.random.default_rng(seed); train, val = [], []
    for label in LABELS:
        group = [r for r in rows if r["label"] == label]
        rng.shuffle(group)
        n_val = max(1, int(round(len(group) * validation_fraction)))
        val.extend(group[:n_val]); train.extend(group[n_val:])
    rng.shuffle(train); rng.shuffle(val)
    return train, val

def non_iid_partition(rows: list[dict], num_clients: int, alpha: float = 0.35, seed: int = 42):
    if num_clients < 2: raise ValueError("num_clients must be >= 2")
    rng = np.random.default_rng(seed); clients = [[] for _ in range(num_clients)]
    for label in LABELS:
        group = [r for r in rows if r["label"] == label]; rng.shuffle(group)
        proportions = rng.dirichlet(np.full(num_clients, alpha))
        counts = rng.multinomial(len(group), proportions); start = 0
        for i, count in enumerate(counts):
            clients[i].extend(group[start:start + count]); start += count
    for i, client in enumerate(clients):
        if client: continue
        donor = max(range(num_clients), key=lambda j: len(clients[j]))
        clients[i].append(clients[donor].pop())
    for client in clients: rng.shuffle(client)
    return clients
