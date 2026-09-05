from dataclasses import dataclass, asdict
import re

@dataclass
class Step:
    step:int
    query:str
    evidence_score:float
    retrieved_ids:list[str]
    action:str

def evidence_score(query,hits):
    q=set(re.findall(r"[a-z0-9]+",query.lower()))
    if not q or not hits: return 0.0
    text=" ".join(d["title"]+" "+d["text"] for _,d in hits).lower()
    covered=sum(1 for t in q if t in text)
    lexical=covered/len(q)
    rank_signal=min(1.0, sum(s for s,_ in hits)/(len(hits)*3.0))
    return round(.75*lexical+.25*rank_signal,4)

def reformulate(query):
    q=query.lower().strip()
    aliases={"out of memory":"oomkilled memory limit","error 104":"e104 payment gateway timeout","retrieval metric":"recall mrr ndcg retrieval evaluation"}
    for src,dst in aliases.items():
        if src in q: return q+" "+dst
    words=[w for w in re.findall(r"[a-z0-9]+",q) if len(w)>2]
    return " ".join(dict.fromkeys(words))

class CorrectiveRAG:
    def __init__(self,retriever,max_steps=3,top_k=4,minimum_evidence_score=.42):
        self.r=retriever; self.max_steps=max_steps; self.top_k=top_k; self.minimum=minimum_evidence_score

    def run(self,query):
        trace=[]; current=query; final=[]
        for step in range(1,self.max_steps+1):
            hits=self.r.search(current,self.top_k); score=evidence_score(current,hits); final=hits
            if score>=self.minimum:
                trace.append(Step(step,current,score,[d["id"] for _,d in hits],"accept"))
                return {"status":"grounded","query":current,"hits":[d for _,d in hits],"trace":[asdict(x) for x in trace]}
            if step==self.max_steps:
                trace.append(Step(step,current,score,[d["id"] for _,d in hits],"abstain"))
                break
            trace.append(Step(step,current,score,[d["id"] for _,d in hits],"reformulate"))
            current=reformulate(current)
        return {"status":"abstain","query":current,"hits":[d for _,d in final],"trace":[asdict(x) for x in trace]}
