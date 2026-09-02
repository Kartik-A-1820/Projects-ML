from __future__ import annotations
import numpy as np

def softmax(logits, temperature=1.0):
    if temperature <= 0: raise ValueError('temperature must be > 0')
    x=np.asarray(logits,dtype=np.float64)/temperature
    x=x-x.max(axis=1,keepdims=True); e=np.exp(x)
    return e/e.sum(axis=1,keepdims=True)

def expected_calibration_error(probs, labels, n_bins=10):
    probs=np.asarray(probs); labels=np.asarray(labels)
    conf=probs.max(axis=1); pred=probs.argmax(axis=1); correct=(pred==labels).astype(float)
    bins=np.linspace(0,1,n_bins+1); ece=0.0
    for i in range(n_bins):
        mask=(conf>bins[i])&(conf<=bins[i+1])
        if mask.any(): ece += mask.mean()*abs(correct[mask].mean()-conf[mask].mean())
    return float(ece)

def negative_log_likelihood(logits, labels, temperature=1.0):
    p=softmax(logits,temperature); labels=np.asarray(labels,dtype=int)
    chosen=p[np.arange(len(labels)),labels]
    return float(-np.log(np.clip(chosen,1e-12,1.0)).mean())

def find_temperature(logits, labels, candidates=None):
    if candidates is None: candidates=np.linspace(.5,3.0,101)
    return min((negative_log_likelihood(logits,labels,float(t)),float(t)) for t in candidates)[1]
