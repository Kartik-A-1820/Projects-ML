def recall_at_k(ranked_ids,relevant,k):
    relevant=set(relevant)
    return 1.0 if not relevant else len(set(ranked_ids[:k])&relevant)/len(relevant)

def reciprocal_rank(ranked_ids,relevant):
    relevant=set(relevant)
    for i,eid in enumerate(ranked_ids,1):
        if eid in relevant: return 1.0/i
    return 0.0

def temporal_coverage(hits,relevant_events):
    rel=set(relevant_events)
    if not rel: return 1.0
    return len({h.event_id for h in hits}&rel)/len(rel)
