def recall_at_k(ranked, relevant, k):
    relevant=set(relevant)
    if not relevant: return 1.0
    return len(set(ranked[:k]) & relevant)/len(relevant)

def reciprocal_rank(ranked, relevant):
    relevant=set(relevant)
    for i, x in enumerate(ranked, 1):
        if x in relevant: return 1.0/i
    return 0.0
