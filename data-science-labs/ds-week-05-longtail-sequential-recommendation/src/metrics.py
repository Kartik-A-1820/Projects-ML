"""Single-target ranking metrics; ranking duplicates never count twice."""
import math

def _rank(ranking, target, k):
    if k < 1:
        raise ValueError('k must be positive')
    unique = list(dict.fromkeys(ranking))[:k]
    return unique.index(target) + 1 if target in unique else None

def recall_at_k(ranking, target, k):
    return float(_rank(ranking, target, k) is not None)

def mrr_at_k(ranking, target, k):
    rank = _rank(ranking, target, k)
    return 1. / rank if rank else 0.

def ndcg_at_k(ranking, target, k):
    rank = _rank(ranking, target, k)
    return 1. / math.log2(rank + 1) if rank else 0.

def coverage(rankings, catalog):
    catalog = set(catalog)
    selected = {item for ranking in rankings for item in ranking}
    return len(selected & catalog) / len(catalog) if catalog else 0.

def tail_share(rankings, tail):
    selected = [item for ranking in rankings for item in ranking]
    return sum(item in tail for item in selected) / len(selected) if selected else 0.
