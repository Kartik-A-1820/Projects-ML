from collections import Counter
from .privacy import pii_hits,nearest_overlap

def deduplicate(rows):
    seen=set();out=[]
    for r in rows:
        key=" ".join(r["text"].lower().split())
        if key not in seen: seen.add(key);out.append(r)
    return out

def diversity(rows):
    toks=[w for r in rows for w in r["text"].lower().split()]; return len(set(toks))/max(1,len(toks))
def label_balance(rows):
    c=Counter(r["label"] for r in rows)
    return 0.0 if not c else min(c.values())/max(c.values())
def assess_row(row,references,copy_threshold=.82):
    pii=pii_hits(row["text"]); overlap=nearest_overlap(row["text"],references); reasons=[]
    if pii: reasons.append("pii:"+",".join(pii))
    if overlap>=copy_threshold: reasons.append("near_copy")
    return {"accepted":not reasons,"reasons":reasons,"nearest_reference_overlap":overlap}
def gate_dataset(rows,references,copy_threshold=.82):
    accepted=[];rejected=[]
    for r in deduplicate(rows):
        a=assess_row(r,references,copy_threshold); item={**r,**a}; (accepted if a["accepted"] else rejected).append(item)
    return {"accepted":accepted,"rejected":rejected,"diversity":diversity(accepted),"label_balance":label_balance(accepted)}
