from __future__ import annotations

import json
from pathlib import Path

from .bm25 import BM25Index
from .dense import DenseRetriever
from .fusion import reciprocal_rank_fusion
from .models import Document
from .rerank import CrossEncoderReranker


def load_documents(path: str) -> list[Document]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Document(doc_id=row["id"], title=row["title"], text=row["text"], metadata={k: v for k, v in row.items() if k not in {"id", "title", "text"}}) for row in rows]


class SearchEngine:
    def __init__(self, documents: list[Document], dense_enabled: bool = False, reranker_enabled: bool = False):
        self.bm25 = BM25Index(documents)
        self.dense = DenseRetriever(documents) if dense_enabled else None
        self.reranker = CrossEncoderReranker() if reranker_enabled else None

    def search(self, query: str, top_k: int = 5, filters: dict | None = None):
        lexical = self.bm25.search(query, top_k=max(20, top_k), filters=filters)
        if self.dense is None:
            candidates = lexical[:top_k]
        else:
            dense = self.dense.search(query, top_k=max(20, top_k), filters=filters)
            candidates = reciprocal_rank_fusion([lexical, dense], top_k=max(10, top_k))
        if self.reranker is not None:
            return self.reranker.rerank(query, candidates, top_k=top_k)
        return candidates[:top_k]
