import numpy as np

def conformal_quantile(y_cal,prob_cal,alpha=.1):
    y_cal=np.asarray(y_cal,dtype=int); p=np.asarray(prob_cal,dtype=float); p_true=np.where(y_cal==1,p,1-p); scores=1-p_true; n=len(scores)
    q=min(1.0,np.ceil((n+1)*(1-alpha))/n); return float(np.quantile(scores,q,method="higher"))

def prediction_sets(prob,qhat):
    p=np.asarray(prob,dtype=float); return np.c_[p<=qhat,(1-p)<=qhat]

def coverage_and_size(y_true,sets):
    y=np.asarray(y_true,dtype=int); sets=np.asarray(sets,dtype=bool); return float(sets[np.arange(len(y)),y].mean()),float(sets.sum(axis=1).mean())
