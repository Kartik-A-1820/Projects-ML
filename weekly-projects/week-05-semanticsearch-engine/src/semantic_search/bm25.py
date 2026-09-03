from __future__ import annotations

from collections import Counter
import math
import re

from .models import Document, SearchHit


TOKEN_RE = re.compile(r"[a-z0-9_./:+-]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class BM25Index:
    def __init__(self, documents: list[Document], k1: float = 1.5, b: float = 0.75):
        if not documents:
            raise ValueError("documents must not be empty")
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.tokens = [tokenize(f"{d.title} {d.text}") for d in documents]
        self.lengths = [len(x) for x in self.tokens]
        self.avgdl = sum(self.lengths) / len(self.lengths)
        self.freqs = [Counter(x) for x in self.tokens]
        self.df = Counter()
        for terms in self.tokens:
            self.df.update(set(terms))

    def idf(self, term: str) -> float:
        n = len(self.documents)
        df = self.df.get(term, 0)
        return math.log(1.0 + (n - df + 0.5) / (df + 0.5))

    def score(self, query: str, doc_index: int) -> float:
        terms = tokenize(query)
        dl = self.lengths[doc_index]
        freq = self.freqs[doc_index]
        total = 0.0
        for term in terms:
            tf = freq.get(term, 0)
            if not tf:
                continue
            denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            total += self.idf(term) * (tf * (self.k1 + 1)) / denominator
        return total

    def search(self, query: str, top_k: int = 10, filters: dict | None = None) -> list[SearchHit]:
        rows = []
        for idx, doc in enumerate(self.documents):
            if filters and any(doc.metadata.get(k) != v for k, v in filters.items()):
                continue
            score = self.score(query, idx)
            if score > 0:
                rows.append((score, doc))
        rows.sort(key=lambda x: (-x[0], x[1].doc_id))
        return [
            SearchHit(d.doc_id, d.title, d.text, float(score), "bm25", d.metadata)
            for score, d in rows[:top_k]
        ]
