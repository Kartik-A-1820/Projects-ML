from pathlib import Path
import json
from collections import defaultdict
from .bm25 import BM25
from .graph import KnowledgeGraph
from .router import route

def rrf(rankings,k=60,top_k=5):
    scores=defaultdict(float); obj={}
    for ranking in rankings:
        for i,item in enumerate(ranking,1):
            scores[item["id"]]+=1/(k+i); obj[item["id"]]=item
    ids=sorted(scores,key=lambda x:(-scores[x],x))[:top_k]
    return [dict(obj[i],score=scores[i],source="rrf") for i in ids]

class GraphRAG:
    def __init__(self,path="data/knowledge.json"):
        data=json.loads(Path(path).read_text())
        self.docs=data["documents"]; self.triples=data["triples"]
        self.lex=BM25(self.docs); self.graph=KnowledgeGraph(self.triples)
    def entity_seeds(self,q):
        ql=q.lower()
        hits=[n for n in self.graph.nodes() if any(tok in ql for tok in n.lower().split())]
        return sorted(hits,key=len,reverse=True)[:4]
    def graph_docs(self,q,hops=2):
        seeds=self.entity_seeds(q); paths=self.graph.traverse(seeds,hops)
        terms=set()
        for p in paths:
            for x in p:
                if not str(x).startswith("inverse:"): terms.add(str(x).lower())
        rows=[]
        for d in self.docs:
            overlap=sum(1 for t in terms if t in d["text"].lower())
            if overlap: rows.append({"id":d["id"],"text":d["text"],"score":float(overlap),"source":"graph","paths":paths})
        rows.sort(key=lambda x:(-x["score"],x["id"]))
        return rows
    def search(self,q,top_k=5):
        rt,score=route(q)
        lexical=[{"id":d["id"],"text":d["text"],"score":float(s),"source":"lexical"} for s,d in self.lex.search(q,6)]
        graph=self.graph_docs(q,2)
        if rt=="lexical": hits=lexical[:top_k]
        elif rt=="graph": hits=graph[:top_k] or lexical[:top_k]
        else: hits=rrf([lexical,graph],top_k=top_k)
        return {"route":rt,"complexity":score,"hits":hits}
