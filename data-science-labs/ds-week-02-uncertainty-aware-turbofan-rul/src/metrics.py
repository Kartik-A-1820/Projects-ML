from __future__ import annotations
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def nasa_like_asymmetric_cost(y_true, y_pred):
    d=np.asarray(y_pred)-np.asarray(y_true)
    return float(np.mean(np.where(d<0,np.exp(-d/13.0)-1.0,np.exp(d/10.0)-1.0)))

def regression_metrics(y_true,y_pred):
    return {'rmse':float(mean_squared_error(y_true,y_pred)**0.5),'mae':float(mean_absolute_error(y_true,y_pred)),'asymmetric_cost':nasa_like_asymmetric_cost(y_true,y_pred)}

def interval_metrics(y_true,lower,upper):
    y=np.asarray(y_true);lo=np.asarray(lower);hi=np.asarray(upper)
    return {'coverage':float(np.mean((y>=lo)&(y<=hi))),'mean_width':float(np.mean(hi-lo)),'median_width':float(np.median(hi-lo))}
