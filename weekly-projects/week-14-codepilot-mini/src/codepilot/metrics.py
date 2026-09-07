def recall_at_k(ranked,relevant,k):
    relevant=set(relevant)
    return 1.0 if not relevant else len(set(ranked[:k])&relevant)/len(relevant)

def reciprocal_rank(ranked,relevant):
    relevant=set(relevant)
    for i,p in enumerate(ranked,1):
        if p in relevant:return 1.0/i
    return 0.0
