import math
from collections import Counter
from .labelers import LABELS

def aggregate(votes,min_confidence=.68):
    valid=[v for v in votes if v in LABELS]
    if not valid:return {'label':None,'confidence':0.0,'entropy':1.0,'abstain':True}
    c=Counter(valid); label,count=c.most_common(1)[0]; conf=count/len(valid)
    probs=[c[l]/len(valid) for l in LABELS if c[l]]
    ent=-sum(p*math.log(p+1e-12) for p in probs)/math.log(len(LABELS))
    return {'label':label if conf>=min_confidence else None,'confidence':conf,'entropy':ent,'abstain':conf<min_confidence}
