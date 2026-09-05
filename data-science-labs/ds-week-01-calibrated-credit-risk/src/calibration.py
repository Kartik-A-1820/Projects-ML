import numpy as np
from sklearn.linear_model import LogisticRegression

class PlattCalibratedModel:
    def __init__(self,base_model): self.base_model=base_model; self.calibrator=LogisticRegression(solver="lbfgs")
    @staticmethod
    def _logit(p):
        p=np.clip(np.asarray(p,dtype=float),1e-6,1-1e-6); return np.log(p/(1-p)).reshape(-1,1)
    def fit(self,X_cal,y_cal):
        self.calibrator.fit(self._logit(self.base_model.predict_proba(X_cal)[:,1]),y_cal); return self
    def predict_proba(self,X):
        p=self.base_model.predict_proba(X)[:,1]; pc=self.calibrator.predict_proba(self._logit(p))[:,1]; return np.c_[1-pc,pc]
