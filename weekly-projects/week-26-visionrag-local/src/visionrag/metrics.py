def accuracy(rows):
    kept=[r for r in rows if r["status"]=="grounded"]
    return 0.0 if not kept else sum(r["truth"]==r["label"] for r in kept)/len(kept)
def abstention_rate(rows):
    return sum(r["status"]=="abstain" for r in rows)/max(1,len(rows))
def retrieval_recall_at_k(evidence,truth,k):
    return float(any(x["label"]==truth for x in evidence[:k]))
