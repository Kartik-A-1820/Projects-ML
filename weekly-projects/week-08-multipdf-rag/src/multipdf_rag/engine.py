from .ingest import ingest_text
from .retrieval import BM25,Dense,rrf
from .answer import evidence_answer
class Engine:
    def __init__(self,paths,dense=False):
        self.chunks=[]
        for p in paths:self.chunks.extend(ingest_text(p))
        self.bm=BM25(self.chunks); self.dense=Dense(self.chunks) if dense else None
    def retrieve(self,q,k=5):
        a=self.bm.search(q,8)
        return a[:k] if self.dense is None else rrf([a,self.dense.search(q,8)],k)
    def query(self,q,k=5):
        hits=self.retrieve(q,k); return {'retrieval':[{'chunk_id':h.chunk.chunk_id,'score':round(h.score,6),'source':h.source} for h in hits],**evidence_answer(q,hits)}
