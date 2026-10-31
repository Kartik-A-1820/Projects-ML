"""Evaluation: subject-cluster uncertainty, ECE, and cost-aware abstention."""
import numpy as np
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score,log_loss,confusion_matrix

def ece(y,p,bins=10):
    confidence=p.max(axis=1); correct=(p.argmax(axis=1)==y)
    edges=np.linspace(0,1,bins+1);total=0.
    for i in range(bins):
        mask=(confidence>=edges[i]) & (confidence<edges[i+1] if i<bins-1 else confidence<=1)
        if mask.any(): total+=mask.mean()*abs(correct[mask].mean()-confidence[mask].mean())
    return float(total)

def evaluate(y,p):
    pred=p.argmax(axis=1)
    return {'n':int(len(y)),'accuracy':float(accuracy_score(y,pred)),'balanced_accuracy':float(balanced_accuracy_score(y,pred)),'macro_f1':float(f1_score(y,pred,average='macro',zero_division=0)),'nll':float(log_loss(y,p,labels=np.arange(p.shape[1]))),'ece':ece(y,p)}

def cluster_ci(y,p,subjects,seed=42,n_boot=150):
    rng=np.random.default_rng(seed);groups=np.unique(subjects);values=[]
    for _ in range(n_boot):
        sampled=rng.choice(groups,size=len(groups),replace=True)
        idx=np.concatenate([np.where(subjects==g)[0] for g in sampled])
        values.append(f1_score(y[idx],p[idx].argmax(axis=1),average='macro',zero_division=0,labels=np.arange(p.shape[1])))
    return [float(v) for v in np.percentile(values,[2.5,97.5])]

def selective(y,p,threshold=.8,error_cost=10,review_cost=1):
    accepted=p.max(axis=1)>=threshold
    errors=int(np.sum(p[accepted].argmax(axis=1)!=y[accepted]))
    review=int((~accepted).sum())
    return {'coverage':float(accepted.mean()),'accepted_errors':errors,'manual_reviews':review,'cost_per_window':float((errors*error_cost+review*review_cost)/len(y))}

def temperature_calibrate(p_cal,y_cal,p_test):
    """Temperature on multiclass log-probabilities; choose only on calibration split."""
    from scipy.optimize import minimize_scalar
    logp=np.log(np.clip(p_cal,1e-8,1))
    def softmax(z):
        z=z-z.max(axis=1,keepdims=True);ex=np.exp(z);return ex/ex.sum(axis=1,keepdims=True)
    def loss(log_temp):
        q=softmax(logp/np.exp(log_temp));return log_loss(y_cal,q,labels=np.arange(q.shape[1]))
    result=minimize_scalar(loss,bounds=(-2,2),method='bounded')
    temp=float(np.exp(result.x));q=softmax(np.log(np.clip(p_test,1e-8,1))/temp)
    return temp,q
