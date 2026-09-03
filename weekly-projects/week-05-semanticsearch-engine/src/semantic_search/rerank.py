from __future__ import annotations

from .models import SearchHit


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", device=None):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name, device=device)

    def rerank(self, query: str, hits: list[SearchHit], top_k: int = 5) -> list[SearchHit]:
        if not hits:
            return []
        pairs = [(query, f"{h.title}. {h.text}") for h in hits]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(scores, hits), key=lambda x: float(x[0]), reverse=True)
        return [SearchHit(h.doc_id, h.title, h.text, float(score), "cross_encoder", h.metadata) for score, h in ranked[:top_k]]
