from __future__ import annotations
from collections import Counter,defaultdict
import math,re
from .schema import Chunk,Hit
TOK=re.compile(r'[a-z0-9_./:+-]+')
def tokens(t): return TOK.findall(t.lower())
class BM25:
    def __init__(self,chunks:list[Chunk],k1=1.5,b=.75):
        self.chunks=chunks; self.k1=k1; self.b=b; self.docs=[tokens(c.text) for c in chunks]; self.lens=list(map(len,self.docs)); self.avg=sum(self.lens)/len(self.lens); self.freq=[Counter(x) for x in self.docs]; self.df=Counter(); [self.df.update(set(x)) for x in self.docs]
    def search(self,q:str,k=8):
        rows=[]; n=len(self.docs)
        for i,c in enumerate(self.chunks):
            s=0.0
            for term in tokens(q):
                tf=self.freq[i].get(term,0)
                if not tf: continue
                idf=math.log(1+(n-self.df.get(term,0)+.5)/(self.df.get(term,0)+.5)); den=tf+self.k1*(1-self.b+self.b*self.lens[i]/self.avg); s+=idf*(tf*(self.k1+1))/den
            if s>0: rows.append(Hit(c,s,'bm25'))
        return sorted(rows,key=lambda h:(-h.score,h.chunk.chunk_id))[:k]
class Dense:
    def __init__(self,chunks,model='sentence-transformers/all-MiniLM-L6-v2'):
        import numpy as np
        from sentence_transformers import SentenceTransformer
        self.np=np; self.chunks=chunks; self.model=SentenceTransformer(model,device='cpu'); self.emb=self.np.asarray(self.model.encode([c.text for c in chunks],normalize_embeddings=True,show_progress_bar=False))
    def search(self,q,k=8):
        v=self.np.asarray(self.model.encode([q],normalize_embeddings=True,show_progress_bar=False)[0]); scores=self.emb@v; ids=self.np.argsort(-scores)[:k]; return [Hit(self.chunks[int(i)],float(scores[i]),'dense') for i in ids]
def rrf(rankings,top_k=5,rrf_k=60):
    scores=defaultdict(float); rep={}
    for ranking in rankings:
        for rank,h in enumerate(ranking,1): scores[h.chunk.chunk_id]+=1/(rrf_k+rank); rep.setdefault(h.chunk.chunk_id,h.chunk)
    return [Hit(rep[cid],score,'rrf') for cid,score in sorted(scores.items(),key=lambda x:(-x[1],x[0]))[:top_k]]
