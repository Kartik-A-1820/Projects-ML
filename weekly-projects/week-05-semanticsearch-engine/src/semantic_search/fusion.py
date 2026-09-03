from __future__ import annotations

from collections import defaultdict

from .models import SearchHit


def reciprocal_rank_fusion(
    rankings: list[list[SearchHit]],
    top_k: int = 10,
    rrf_k: int = 60,
) -> list[SearchHit]:
    if rrf_k < 0:
        raise ValueError("rrf_k must be >= 0")

    scores = defaultdict(float)
    representative: dict[str, SearchHit] = {}

    for ranking in rankings:
        for rank, hit in enumerate(ranking, start=1):
            scores[hit.doc_id] += 1.0 / (rrf_k + rank)
            representative.setdefault(hit.doc_id, hit)

    ordered = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:top_k]
    return [
        SearchHit(
            doc_id=doc_id,
            title=representative[doc_id].title,
            text=representative[doc_id].text,
            score=float(score),
            source="rrf",
            metadata=representative[doc_id].metadata,
        )
        for doc_id, score in ordered
    ]
