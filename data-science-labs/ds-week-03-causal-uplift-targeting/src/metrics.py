import numpy as np

def transformed_outcome(y, w, p=0.5):
    y=np.asarray(y,float); w=np.asarray(w,float)
    return y*(w-p)/(p*(1-p))

def qini_curve(y,w,uplift):
    y=np.asarray(y);w=np.asarray(w);uplift=np.asarray(uplift)
    order=np.argsort(-uplift); y=y[order];w=w[order]
    tr=np.cumsum(w);co=np.cumsum(1-w)
    ty=np.cumsum(y*w);cy=np.cumsum(y*(1-w))
    gain=ty-cy*tr/np.maximum(co,1)
    x=np.arange(1,len(y)+1)/len(y)
    return x,gain

def qini_auc(y,w,uplift):
    x,g=qini_curve(y,w,uplift)
    baseline=x*g[-1]
    return float(np.trapezoid(g-baseline,x))

def policy_value_ipw(y,w,policy,p=0.5):
    y=np.asarray(y,float);w=np.asarray(w,int);policy=np.asarray(policy,int)
    prob=np.where(w==1,p,1-p)
    matched=(w==policy)
    return float(np.mean(matched*y/prob))

def ate(y,w):
    y=np.asarray(y,float);w=np.asarray(w,int)
    return float(y[w==1].mean()-y[w==0].mean())
