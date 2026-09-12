from .agents import ResearchAgent,Critic
class Blackboard:
    def __init__(self,max_messages=12):self.max_messages=max_messages;self.messages=[]
    def post(self,m):
        if len(self.messages)>=self.max_messages:raise RuntimeError("message budget exhausted")
        self.messages.append(m)
class MultiAgentResearcher:
    def __init__(self,evidence,max_messages=12,max_evidence=3):
        self.agents=[ResearchAgent(name,shard,max_evidence) for name,shard in evidence.items()];self.critic=Critic();self.max_messages=max_messages
    def run(self,question):
        board=Blackboard(self.max_messages)
        for a in self.agents:board.post(a.investigate(question))
        review=self.critic.review(board.messages)
        return {"answer":review["summary"],"evidence_ids":review["unique_evidence"],"messages":len(board.messages),"communication_density":len(board.messages)/max(1,len(self.agents)),"trace":[m.__dict__ for m in board.messages]}
