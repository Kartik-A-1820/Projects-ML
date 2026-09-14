from __future__ import annotations
import numpy as np
from scipy.stats import ks_2samp

def ks_test(reference,current):
    stat,p=ks_2samp(reference,current,method='auto')
    return float(stat),float(p)

def psi(reference,current,bins=10):
    reference=np.asarray(reference,float); current=np.asarray(current,float)
    edges=np.unique(np.quantile(reference,np.linspace(0,1,bins+1)))
    if len(edges)<3:return 0.0
    edges[0],edges[-1]=-np.inf,np.inf
    r=np.histogram(reference,bins=edges)[0]/len(reference); c=np.histogram(current,bins=edges)[0]/len(current)
    eps=1e-6; r=np.clip(r,eps,None); c=np.clip(c,eps,None)
    return float(np.sum((c-r)*np.log(c/r)))

def mean_shift_effect(reference,current):
    r=np.asarray(reference,float); c=np.asarray(current,float)
    pooled=max(float(np.std(reference,ddof=1)),1e-9)
    return float(abs(c.mean()-r.mean())/pooled)

def linear_mmd(reference,current):
    r=np.asarray(reference,float); c=np.asarray(current,float)
    return float((r.mean()-c.mean())**2)
