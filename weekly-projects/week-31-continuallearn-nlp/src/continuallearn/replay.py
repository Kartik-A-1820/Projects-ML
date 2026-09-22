from dataclasses import dataclass
@dataclass
class Item:
    text:str;label:str;task:str;forgetting:float=0.0
class ReplayBuffer:
    def __init__(self,capacity=120):self.capacity=capacity;self.items=[]
    def add(self,task,samples):
        for text,label in samples:self.items.append(Item(text,label,task))
        self.items=sorted(self.items,key=lambda x:x.forgetting,reverse=True)[:self.capacity]
    def update_forgetting(self,task_scores):
        for x in self.items:x.forgetting=max(0.0,task_scores.get(x.task,0.0))
    def sample(self,n):return sorted(self.items,key=lambda x:(-x.forgetting,x.task,x.text))[:n]
