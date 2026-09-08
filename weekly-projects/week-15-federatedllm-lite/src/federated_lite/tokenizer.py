from __future__ import annotations
import hashlib
import re
import torch

TOKEN_RE = re.compile(r"[a-z0-9_]+")

class HashTokenizer:
    def __init__(self, vocab_size: int = 512, max_length: int = 24):
        if vocab_size < 32:
            raise ValueError("vocab_size must be >= 32")
        self.vocab_size = vocab_size
        self.max_length = max_length

    def _token_id(self, token: str) -> int:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        return 2 + int.from_bytes(digest[:4], "little") % (self.vocab_size - 2)

    def encode(self, text: str) -> torch.Tensor:
        ids = [self._token_id(t) for t in TOKEN_RE.findall(text.lower())][: self.max_length]
        ids = ids or [1]
        ids += [0] * (self.max_length - len(ids))
        return torch.tensor(ids, dtype=torch.long)
