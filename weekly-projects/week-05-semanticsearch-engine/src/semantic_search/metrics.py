from __future__ import annotations

import math


def recall_at_k(ranked_ids: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 1.0
    return len(set(ranked_ids[:k]) & relevant) / len(relevant)


def reciprocal_rank(ranked_ids: list[str], relevant: set[str]) -> float:
    for rank, doc_id in enumerate(ranked_ids, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_ids: list[str], relevant: set[str], k: int) -> float:
    def dcg(ids):
        score = 0.0
        for i, doc_id in enumerate(ids[:k], start=1):
            rel = 1.0 if doc_id in relevant else 0.0
            score += rel / math.log2(i + 1)
        return score
    ideal = min(len(relevant), k)
    if ideal == 0:
        return 1.0
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal + 1))
    return dcg(ranked_ids) / idcg
