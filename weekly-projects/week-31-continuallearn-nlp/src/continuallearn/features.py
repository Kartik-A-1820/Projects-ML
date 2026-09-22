import hashlib, re, numpy as np
class HashingTextEncoder:
    def __init__(self,dim=2048): self.dim=dim
    def encode(self,texts):
        X=np.zeros((len(texts),self.dim),dtype=np.float32)
        for i,text in enumerate(texts):
            toks=re.findall(r"[a-z0-9]+",text.lower())
            feats=toks+[f"{a}_{b}" for a,b in zip(toks,toks[1:])]
            for f in feats:
                h=int(hashlib.blake2b(f.encode(),digest_size=8).hexdigest(),16)
                X[i,h%self.dim]+=1.0 if (h>>8)%2 else -1.0
            n=np.linalg.norm(X[i])
            if n:X[i]/=n
        return X
