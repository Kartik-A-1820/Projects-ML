import re
MULTIHOP={"which","that","operates","consuming","governed","depends","after","before","through","constraint"}
def complexity_score(query):
    q=query.lower(); toks=re.findall(r"[a-z0-9]+",q)
    score=0.12
    score += min(0.30,max(0,len(toks)-7)*0.03)
    score += 0.15*sum(1 for w in MULTIHOP if w in toks)
    score += 0.18 if "that" in toks or "which" in toks else 0
    return min(1.0,score)
def route(query,graph_threshold=.62,hybrid_lower=.40):
    s=complexity_score(query)
    if s>=graph_threshold:return "graph",s
    if s>=hybrid_lower:return "hybrid",s
    return "lexical",s
