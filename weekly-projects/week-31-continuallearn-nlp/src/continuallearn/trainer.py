from .features import HashingTextEncoder
from .model import ContinualSoftmax
from .replay import ReplayBuffer
from .metrics import accuracy,forgetting,average_accuracy
class ContinualTrainer:
    def __init__(self,dim=2048,replay_capacity=120,replay_per_task=24,lr=.08,reg=.002,seed=42):
        self.enc=HashingTextEncoder(dim);self.model=ContinualSoftmax(dim,lr,reg,seed);self.buffer=ReplayBuffer(replay_capacity);self.replay_per_task=replay_per_task;self.seen={};self.history=[]
    def learn(self,task,samples,epochs=8):
        replay=self.buffer.sample(self.replay_per_task);merged=list(samples)+[(x.text,x.label) for x in replay]
        self.model.fit(self.enc.encode([x[0] for x in merged]),[x[1] for x in merged],epochs);self.seen[task]=list(samples);scores=self.evaluate();self.history.append(scores)
        f=forgetting(self.history);self.buffer.update_forgetting(f);self.buffer.add(task,samples)
        return {"task":task,"scores":scores,"avg_accuracy":average_accuracy(scores),"forgetting":f,"replay_size":len(replay)}
    def evaluate(self):return {t:accuracy([y for _,y in s],self.model.predict(self.enc.encode([x for x,_ in s]))) for t,s in self.seen.items()}
