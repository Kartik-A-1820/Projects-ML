import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
def km_curve(duration,event):
    duration=np.asarray(duration,float);event=np.asarray(event,int);times=np.sort(np.unique(duration[event==1]));s=1.;out=[]
    for t in times:
        at=(duration>=t).sum();d=((duration==t)&(event==1)).sum()
        if at:s*=1-d/at
        out.append((float(t),float(s)))
    return out
class DiscreteTimeHazard:
    def __init__(self,max_month=72):
        self.max_month=max_month;self.model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=400,class_weight="balanced",C=.5))
    def _expand(self,X,duration,event):
        rows=[];targets=[]
        for i in range(len(X)):
            stop=min(int(max(1,np.ceil(duration[i]))),self.max_month)
            for m in range(1,stop+1):
                rows.append(np.r_[X[i],m/self.max_month,(m/self.max_month)**2]);targets.append(int(event[i] and m==stop))
        return np.asarray(rows,np.float32),np.asarray(targets)
    def fit(self,X,duration,event):
        Xe,ye=self._expand(X,duration,event);self.model.fit(Xe,ye);return self
    def survival(self,X,horizons):
        horizons=np.asarray(horizons,int);maxh=min(self.max_month,int(horizons.max()));surv=np.ones((len(X),maxh),np.float32);running=np.ones(len(X),np.float32)
        for m in range(1,maxh+1):
            Xm=np.c_[X,np.full(len(X),m/self.max_month),np.full(len(X),(m/self.max_month)**2)].astype(np.float32)
            running*=1-self.model.predict_proba(Xm)[:,1];surv[:,m-1]=running
        return np.stack([surv[:,min(h,maxh)-1] for h in horizons],axis=1)
