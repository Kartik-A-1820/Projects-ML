import numpy as np
from sklearn.metrics import roc_auc_score,brier_score_loss,log_loss

def expected_calibration_error(y,p,n_bins=10):
    y=np.asarray(y); p=np.asarray(p); bins=np.linspace(0,1,n_bins+1); ece=0.0
    for i in range(n_bins):
        m=(p>bins[i])&(p<=bins[i+1])
        if m.any(): ece += m.mean()*abs(y[m].mean()-p[m].mean())
    return float(ece)

def evaluate(y,p):
    return {'roc_auc':float(roc_auc_score(y,p)),'brier':float(brier_score_loss(y,p)),'log_loss':float(log_loss(y,p)),'ece':expected_calibration_error(y,p)}
