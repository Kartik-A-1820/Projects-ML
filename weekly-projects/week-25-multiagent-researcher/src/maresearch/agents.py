from dataclasses import dataclass
@dataclass
class Message:
    sender:str
    evidence_ids:list[str]
    text:str
class ResearchAgent:
    def __init__(self,name,shard,max_evidence=3):
        self.name=name;self.shard=shard;self.max_evidence=max_evidence
    def investigate(self,question):
        words=set(question.lower().split());ranked=[]
        for e in self.shard:
            score=sum(w.strip("?,.") in e["claim"].lower() for w in words);ranked.append((score,e))
        ranked.sort(key=lambda x:(-x[0],x[1]["id"]));chosen=[e for _,e in ranked[:self.max_evidence]]
        return Message(self.name,[e["id"] for e in chosen]," ".join(e["claim"] for e in chosen))
class Critic:
    def review(self,messages):
        ids=[];claims=[]
        for m in messages:ids.extend(m.evidence_ids);claims.append(m.text)
        return {"unique_evidence":sorted(set(ids)),"conflict":False,"summary":" ".join(claims)}
