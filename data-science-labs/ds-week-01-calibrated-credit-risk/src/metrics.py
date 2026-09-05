import numpy as np
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,log_loss,confusion_matrix

def expected_calibration_error(y_true,prob,n_bins=10):
    y_true=np.asarray(y_true,dtype=int); prob=np.asarray(prob,dtype=float); edges=np.linspace(0,1,n_bins+1); ece=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(prob>=lo)&(prob<(hi) if hi<1 else prob<=hi)
        if mask.any(): ece+=mask.mean()*abs(y_true[mask].mean()-prob[mask].mean())
    return float(ece)

def recall_at_fpr(y_true,prob,max_fpr=.05):
    best=(0.0,1.0)
    for t in np.unique(prob)[::-1]:
        tn,fp,fn,tp=confusion_matrix(y_true,(prob>=t).astype(int),labels=[0,1]).ravel(); fpr=fp/max(fp+tn,1); rec=tp/max(tp+fn,1)
        if fpr<=max_fpr and rec>=best[0]: best=(float(rec),float(t))
    return best

def evaluate_probabilities(y_true,prob):
    rec,t=recall_at_fpr(np.asarray(y_true),np.asarray(prob))
    return {"roc_auc":float(roc_auc_score(y_true,prob)),"pr_auc":float(average_precision_score(y_true,prob)),"brier":float(brier_score_loss(y_true,prob)),"log_loss":float(log_loss(y_true,np.c_[1-prob,prob],labels=[0,1])),"ece_10":expected_calibration_error(y_true,prob),"recall_at_5pct_fpr":rec,"threshold_at_5pct_fpr":t}

def cost_optimal_threshold(y_true,prob,false_negative_cost=5.0,false_positive_cost=1.0):
    rows=[]
    for t in np.linspace(.01,.99,99):
        tn,fp,fn,tp=confusion_matrix(y_true,(prob>=t).astype(int),labels=[0,1]).ravel(); rows.append((false_negative_cost*fn+false_positive_cost*fp,t,fp,fn,tp,tn))
    return min(rows,key=lambda x:x[0])
