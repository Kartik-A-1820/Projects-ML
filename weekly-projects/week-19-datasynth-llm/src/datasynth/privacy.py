import re
PII={"email":r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b","phone":r"\b(?:\+?\d[\d -]{8,}\d)\b","card":r"\b(?:\d[ -]*?){13,16}\b"}
def pii_hits(text): return [k for k,p in PII.items() if re.search(p,text)]
def token_set(text): return set(re.findall(r"[a-z0-9]+",text.lower()))
def jaccard(a,b):
    a,b=token_set(a),token_set(b); return len(a&b)/max(1,len(a|b))
def nearest_overlap(text,references): return max((jaccard(text,r["text"]) for r in references),default=0.0)
