from __future__ import annotations
import numpy as np

class DelayedLabelPerformance:
    def __init__(self):
        self.predictions={}; self.labels={}
    def add_prediction(self,event_id,prediction,confidence):
        self.predictions[event_id]=(int(prediction),float(confidence))
    def add_label(self,event_id,label):
        self.labels[event_id]=int(label)
    def accuracy(self):
        ids=set(self.predictions)&set(self.labels)
        if not ids:return None
        return float(np.mean([self.predictions[i][0]==self.labels[i] for i in ids]))
    def mean_confidence(self):
        if not self.predictions:return None
        return float(np.mean([x[1] for x in self.predictions.values()]))
