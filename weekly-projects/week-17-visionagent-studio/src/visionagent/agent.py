from .planner import choose_tools
from .memory import VisualMemory

class VisionAgent:
    def __init__(self,registry,max_steps=4,threshold=.65):
        self.registry=registry;self.max_steps=max_steps;self.threshold=threshold
    def run(self,scene,query):
        mem=VisualMemory();trace=[];tools=choose_tools(query)
        for step,tool in enumerate(tools[:self.max_steps],1):
            obs=self.registry.run(tool,scene,query);mem.add(tool,obs)
            trace.append({"step":step,"tool":tool,"confidence":obs["confidence"]})
        observations=mem.retrieve()
        if not observations:return {"status":"abstain","answer":"","trace":trace}
        avg=sum(e["observation"]["confidence"] for e in observations)/len(observations)
        items=[]
        for e in observations:items.extend(map(str,e["observation"]["items"]))
        status="grounded" if avg>=self.threshold and items else "abstain"
        return {"status":status,"answer":" | ".join(items) if status=="grounded" else "insufficient visual evidence","confidence":avg,"trace":trace,"memory":observations}
