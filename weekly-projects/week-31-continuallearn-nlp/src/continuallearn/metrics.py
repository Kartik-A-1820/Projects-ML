import numpy as np
def accuracy(y,p):return float(np.mean(np.asarray(y)==np.asarray(p))) if len(y) else 0.0
def forgetting(history):
    out={};tasks=set(k for row in history for k in row)
    for t in tasks:
        vals=[r[t] for r in history if t in r];out[t]=float(max(vals)-vals[-1]) if vals else 0.0
    return out
def average_accuracy(row):return float(np.mean(list(row.values()))) if row else 0.0
