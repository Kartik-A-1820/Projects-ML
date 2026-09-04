def recall_at_k(ids,relevant,k):
    relevant=set(relevant); return len(set(ids[:k])&relevant)/len(relevant) if relevant else 1.0
def reciprocal_rank(ids,relevant):
    relevant=set(relevant)
    for i,x in enumerate(ids,1):
        if x in relevant:return 1/i
    return 0.0
