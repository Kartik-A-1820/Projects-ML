from __future__ import annotations
import hashlib, re
import numpy as np

TOK = re.compile(r"[a-z0-9]+")

def normalize(v):
    v = np.asarray(v, dtype=np.float32)
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

class DeterministicTextImageEncoder:
    """Dependency-light shared-space encoder used only for tests/smoke paths."""
    def __init__(self, dim=128):
        self.dim = dim

    def _encode_tokens(self, text):
        v = np.zeros(self.dim, dtype=np.float32)
        for token in TOK.findall(text.lower()):
            h = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16)
            v[h % self.dim] += 1.0
        return normalize(v)

    def encode_text(self, text):
        return self._encode_tokens(text)

    def encode_image_descriptor(self, caption):
        return self._encode_tokens(caption)

class VectorIndex:
    def __init__(self):
        self.ids, self.vectors, self.metadata = [], [], []

    def add(self, item_id, vector, metadata):
        self.ids.append(item_id)
        self.vectors.append(normalize(vector))
        self.metadata.append(dict(metadata))

    def search(self, query_vector, top_k=5, filters=None):
        q = normalize(query_vector)
        rows = []
        for item_id, v, meta in zip(self.ids, self.vectors, self.metadata):
            if filters and any(meta.get(k) != val for k, val in filters.items()):
                continue
            rows.append((float(np.dot(q, v)), item_id, meta))
        rows.sort(key=lambda x: (-x[0], x[1]))
        return rows[:top_k]
