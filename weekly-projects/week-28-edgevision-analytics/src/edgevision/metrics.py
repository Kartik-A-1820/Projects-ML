import numpy as np

def classification_metrics(y_true,y_pred):
    y_true=np.asarray(y_true,dtype=bool); y_pred=np.asarray(y_pred,dtype=bool)
    tp=int(np.sum(y_true & y_pred)); fp=int(np.sum(~y_true & y_pred)); fn=int(np.sum(y_true & ~y_pred)); tn=int(np.sum(~y_true & ~y_pred))
    precision=tp/(tp+fp) if tp+fp else 0.0; recall=tp/(tp+fn) if tp+fn else 0.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {'tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':precision,'recall':recall,'f1':f1}

def latency_metrics(values):
    a=np.asarray(values,float)
    return {'mean_ms':float(a.mean()),'p95_ms':float(np.percentile(a,95)),'fps_equivalent':float(1000/max(a.mean(),1e-9))}
