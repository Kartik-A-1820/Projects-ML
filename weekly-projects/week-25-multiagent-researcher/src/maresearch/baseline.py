class SingleAgentResearcher:
    def __init__(self,evidence,max_items=3):self.flat=[x for shard in evidence.values() for x in shard];self.max_items=max_items
    def run(self,question):
        chosen=self.flat[:self.max_items]
        return {"answer":" ".join(x["claim"] for x in chosen),"evidence_ids":[x["id"] for x in chosen],"messages":1,"communication_density":1.0}
