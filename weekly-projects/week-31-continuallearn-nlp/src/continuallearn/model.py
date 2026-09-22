import numpy as np
class ContinualSoftmax:
    def __init__(self,dim,lr=.08,reg=.002,seed=42):
        self.dim=dim;self.lr=lr;self.reg=reg;self.rng=np.random.default_rng(seed)
        self.labels=[];self.W=np.zeros((dim,0),np.float32);self.anchor=self.W.copy()
    def _expand(self,labels):
        for lab in labels:
            if lab not in self.labels:
                self.labels.append(lab);self.W=np.c_[self.W,self.rng.normal(0,.01,self.dim).astype(np.float32)]
        if self.anchor.shape[1]<self.W.shape[1]:self.anchor=np.c_[self.anchor,np.zeros((self.dim,self.W.shape[1]-self.anchor.shape[1]),np.float32)]
    def fit(self,X,y,epochs=8):
        self._expand(y);yi=np.array([self.labels.index(v) for v in y])
        for _ in range(epochs):
            z=X@self.W;z-=z.max(1,keepdims=True);p=np.exp(z);p/=p.sum(1,keepdims=True)
            Y=np.zeros_like(p);Y[np.arange(len(y)),yi]=1
            grad=X.T@(p-Y)/len(y)+self.reg*(self.W-self.anchor);self.W-=self.lr*grad.astype(np.float32)
        self.anchor=self.W.copy();return self
    def predict(self,X):return np.array([self.labels[i] for i in np.argmax(X@self.W,axis=1)]) if self.labels else np.array([])
