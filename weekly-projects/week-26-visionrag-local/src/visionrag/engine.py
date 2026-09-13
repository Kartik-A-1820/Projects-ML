from collections import defaultdict
from .index import ExemplarIndex

def adaptive_k(rows,base_k=3,max_k=7):
    if len(rows)<=base_k:return len(rows)
    top=[x.label for _,x in rows[:base_k]]
    agreement=max(top.count(y) for y in set(top))/len(top)
    return base_k if agreement>=.67 else min(max_k,len(rows))

class VisionRAG:
    def __init__(self,index:ExemplarIndex,base_k=3,max_k=7,abstain_confidence=.58,min_similarity=.72):
        self.index=index;self.base_k=base_k;self.max_k=max_k
        self.abstain_confidence=abstain_confidence;self.min_similarity=min_similarity
    def predict(self,image,machine=None):
        rows=self.index.search(image,self.max_k,machine=machine)
        k=adaptive_k(rows,self.base_k,self.max_k)
        chosen=rows[:k]
        votes=defaultdict(float)
        for s,x in chosen:votes[x.label]+=max(0.0,s)
        total=sum(votes.values()) or 1.0
        ranked=sorted(votes.items(),key=lambda x:(-x[1],x[0]))
        label,score=ranked[0]
        confidence=score/total
        top_similarity=chosen[0][0] if chosen else 0.0
        status="grounded" if confidence>=self.abstain_confidence and top_similarity>=self.min_similarity else "abstain"
        evidence=[
            {"id":x.item_id,"label":x.label,"similarity":float(s),"path":x.path}
            for s,x in chosen
        ]
        return {
            "status":status,
            "label":label if status=="grounded" else "unknown",
            "confidence":float(confidence),
            "top_similarity":float(top_similarity),
            "adaptive_k":k,
            "evidence":evidence,
        }
