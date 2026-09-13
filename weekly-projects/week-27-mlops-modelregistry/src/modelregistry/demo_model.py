from __future__ import annotations
import json,pickle,hashlib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def train(path,C=1.0,seed=42):
    X,y=load_iris(return_X_y=True)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,stratify=y,random_state=seed)
    m=LogisticRegression(C=C,max_iter=400,random_state=seed).fit(Xtr,ytr)
    acc=float(accuracy_score(yte,m.predict(Xte)))
    with open(path,"wb") as f:pickle.dump(m,f)
    data_hash=hashlib.sha256(np.ascontiguousarray(Xtr).tobytes()+np.ascontiguousarray(ytr).tobytes()).hexdigest()
    signature={"inputs":[{"name":f"feature_{i}","dtype":"float64"} for i in range(X.shape[1])],"outputs":[{"name":"class","dtype":"int64"}]}
    return {"accuracy":acc},data_hash,signature
