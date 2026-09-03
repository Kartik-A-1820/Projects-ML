from __future__ import annotations

import numpy as np

from .models import Document, SearchHit


class DenseRetriever:
    def __init__(self, documents: list[Document], model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        from sentence_transformers import SentenceTransformer
        self.documents = documents
        self.model = SentenceTransformer(model_name, device=device)
        self.embeddings = np.asarray(self.model.encode([f"{d.title}. {d.text}" for d in documents], normalize_embeddings=True, show_progress_bar=False), dtype=np.float32)

    def search(self, query: str, top_k: int = 10, filters: dict | None = None) -> list[SearchHit]:
        q = np.asarray(self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0], dtype=np.float32)
        scores = self.embeddings @ q
        ids = np.argsort(-scores)
        hits = []
        for idx in ids:
            doc = self.documents[int(idx)]
            if filters and any(doc.metadata.get(k) != v for k, v in filters.items()):
                continue
            hits.append(SearchHit(doc.doc_id, doc.title, doc.text, float(scores[idx]), "dense", doc.metadata))
            if len(hits) >= top_k:
                break
        return hits
