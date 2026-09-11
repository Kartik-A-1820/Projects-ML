import hashlib,re,numpy as np
TOK=re.compile(r"[a-z0-9]+")
ALIASES={"reimbursement":"refund","parcel":"shipment","forgotten":"forgot","timeout":"failed","change":"reset"}
def embed(text,dim=128):
    v=np.zeros(dim,dtype=np.float32)
    for t in TOK.findall(text.lower()):
        t=ALIASES.get(t,t); h=int(hashlib.sha256(t.encode()).hexdigest()[:8],16); v[h%dim]+=1
    n=np.linalg.norm(v); return v if n==0 else v/n
def similarity(a,b): return float(np.dot(embed(a),embed(b)))
