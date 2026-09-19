import numpy as np
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

def _p(model,X): return model.predict_proba(X)[:,1]

class SLearner:
    def __init__(self,model=None): self.model=model or HistGradientBoostingClassifier(max_iter=120,max_depth=4,learning_rate=.06,random_state=42)
    def fit(self,X,w,y): self.model.fit(np.c_[X,w],y); return self
    def effect(self,X): return _p(self.model,np.c_[X,np.ones(len(X))])-_p(self.model,np.c_[X,np.zeros(len(X))])

class TLearner:
    def __init__(self,model=None):
        base=model or HistGradientBoostingClassifier(max_iter=120,max_depth=4,learning_rate=.06,random_state=42); self.m1=clone(base);self.m0=clone(base)
    def fit(self,X,w,y): self.m1.fit(X[w==1],y[w==1]);self.m0.fit(X[w==0],y[w==0]);return self
    def effect(self,X): return _p(self.m1,X)-_p(self.m0,X)

class XLearner:
    def __init__(self):
        self.mu1=HistGradientBoostingClassifier(max_iter=100,max_depth=4,random_state=42);self.mu0=HistGradientBoostingClassifier(max_iter=100,max_depth=4,random_state=42)
        self.tau1=HistGradientBoostingRegressor(max_iter=100,max_depth=4,random_state=42);self.tau0=HistGradientBoostingRegressor(max_iter=100,max_depth=4,random_state=42)
    def fit(self,X,w,y):
        self.mu1.fit(X[w==1],y[w==1]);self.mu0.fit(X[w==0],y[w==0])
        self.tau1.fit(X[w==1],y[w==1]-_p(self.mu0,X[w==1]));self.tau0.fit(X[w==0],_p(self.mu1,X[w==0])-y[w==0]);return self
    def effect(self,X): return .5*self.tau0.predict(X)+.5*self.tau1.predict(X)
