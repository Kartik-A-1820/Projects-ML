from __future__ import annotations
from collections import Counter,defaultdict
import json,math,re
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
TOK=re.compile(r"[a-z0-9_.:/+-]+")
def tokens(t):return TOK.findall(t.lower())
class BM25:
 def __init__(self,docs):
  self.docs=docs;self.ts=[tokens(d["text"]) for d in docs];self.freq=[Counter(x) for x in self.ts];self.length=[len(x) for x in self.ts];self.avg=max(1,sum(self.length)/len(self.length));self.df=Counter();[self.df.update(set(x)) for x in self.ts]
 def search(self,q,k=10):
  qt=tokens(q);n=len(self.docs);rows=[]
  for i,d in enumerate(self.docs):
   s=0.;dl=self.length[i]
   for term in qt:
    tf=self.freq[i].get(term,0)
    if tf:
     idf=math.log(1+(n-self.df[term]+.5)/(self.df[term]+.5));s+=idf*(tf*2.5)/(tf+1.5*(.25+.75*dl/self.avg))
   if s>0:rows.append((float(s),d))
  return sorted(rows,key=lambda x:(-x[0],x[1]["id"]))[:k]
class DenseProxy:
 def __init__(self,docs):
  self.docs=docs;self.v=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True);X=self.v.fit_transform([d["text"] for d in docs]);n=min(6,max(2,min(X.shape)-1));self.svd=TruncatedSVD(n_components=n,random_state=42);self.X=normalize(self.svd.fit_transform(X))
 def search(self,q,k=10):
  qv=normalize(self.svd.transform(self.v.transform([q])))[0];scores=self.X@qv;ids=np.argsort(-scores);return [(float(scores[i]),self.docs[int(i)]) for i in ids[:k] if scores[i]>0]
EXACT=re.compile(r"\b(?:[A-Z]{1,5}-?\d{2,}|\w*\d{3,}\w*)\b")
def query_family(q):
 exact=bool(EXACT.search(q));semantic=any(w in q.lower().split() for w in {"why","how","similar","meaning","different","described","concept","paraphrase"})
 if exact and semantic:return "mixed"
 if exact:return "mixed" if len(q.split())>=3 else "exact"
 if semantic:return "semantic"
 return "mixed"
def rrf(rankings,k=60,top_k=10):
 s=defaultdict(float);d={}
 for ranking in rankings:
  for rank,(_,doc) in enumerate(ranking,1):s[doc["id"]]+=1/(k+rank);d[doc["id"]]=doc
 return [(s[i],d[i]) for i in sorted(s,key=lambda x:(-s[x],x))[:top_k]]
def weighted(sparse,dense,alpha=.5,top_k=10):
 def norm(rows):
  if not rows:return {}
  vals=[s for s,_ in rows];lo,hi=min(vals),max(vals);return {d["id"]:((s-lo)/(hi-lo) if hi>lo else 1,d) for s,d in rows}
 a,b=norm(sparse),norm(dense);out=[]
 for i in set(a)|set(b):sa,da=a.get(i,(0,None));sb,db=b.get(i,(0,None));out.append(((1-alpha)*sa+alpha*sb,da or db))
 return sorted(out,key=lambda x:(-x[0],x[1]["id"]))[:top_k]
def expand(q,rows,n=2):
 base=set(re.findall(r"[a-z0-9]+",q.lower()));c=Counter();stop={"the","a","an","and","or","to","of","is","are","with","for","in","on","can","how","why"}
 for _,d in rows[:2]:
  for t in re.findall(r"[a-z0-9]+",d["text"].lower()):
   if t not in stop and t not in base and len(t)>3:c[t]+=1
 extra=[x for x,_ in c.most_common(n)];return q+(" "+" ".join(extra) if extra else "")
class HybridEngine:
 def __init__(self,path="data/documents.json"):
  self.docs=json.loads(Path(path).read_text());self.sparse=BM25(self.docs);self.dense=DenseProxy(self.docs)
 def search(self,q,top_k=5,fusion="rrf",use_prf=True):
  fam=query_family(q);budget={"exact":5,"semantic":8,"mixed":10}[fam];s=self.sparse.search(q,budget);d=self.dense.search(q,budget)
  if use_prf and fam!="exact":d=self.dense.search(expand(q,s),budget)
  rows=s if fam=="exact" else d if fam=="semantic" else (rrf([s,d],top_k=top_k) if fusion=="rrf" else weighted(s,d,.5,top_k))
  return {"family":fam,"candidate_budget":budget,"hits":[{"id":doc["id"],"text":doc["text"],"score":float(score)} for score,doc in rows[:top_k]]}
def recall_at_k(ranked,relevant,k):rel=set(relevant);return 1 if not rel else len(set(ranked[:k])&rel)/len(rel)
def reciprocal_rank(ranked,relevant):
 rel=set(relevant)
 for i,x in enumerate(ranked,1):
  if x in rel:return 1/i
 return 0.
def ndcg_at_k(ranked,relevant,k):
 rel=set(relevant);dcg=sum((1 if x in rel else 0)/math.log2(i+2) for i,x in enumerate(ranked[:k]));ideal=sum(1/math.log2(i+2) for i in range(min(len(rel),k)));return dcg/ideal if ideal else 1.
