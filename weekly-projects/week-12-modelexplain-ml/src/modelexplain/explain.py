from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.linear_model import Ridge

IMMUTABLE={'age'}

def global_permutation_importance(model,X,y,seed=42):
    r=permutation_importance(model,X,y,n_repeats=8,random_state=seed,scoring='roc_auc')
    return sorted(zip(X.columns,r.importances_mean),key=lambda x:-abs(x[1]))

def partial_dependence_curve(model,X,feature,grid_resolution=15):
    out=partial_dependence(model,X,[feature],grid_resolution=grid_resolution)
    grid=out['grid_values'][0] if 'grid_values' in out else out['values'][0]
    avg=out['average'][0]
    return list(zip(map(float,grid),map(float,avg)))

def local_surrogate(model,X,row_index=0,seed=42,n=350):
    rng=np.random.default_rng(seed); x=X.iloc[row_index].astype(float); scales=X.std().replace(0,1.0)
    samples=np.tile(x.values,(n,1))+rng.normal(0,.18,(n,len(x)))*scales.values
    P=pd.DataFrame(samples,columns=X.columns); probs=model.predict_proba(P)[:,1]
    distances=np.linalg.norm((P-x)/scales,axis=1); weights=np.exp(-(distances**2))
    surrogate=Ridge(alpha=1.0).fit(P,probs,sample_weight=weights)
    return dict(sorted(zip(X.columns,map(float,surrogate.coef_)),key=lambda x:-abs(x[1])))

def explanation_stability(model,X,row_index=0):
    a=local_surrogate(model,X,row_index,seed=41); b=local_surrogate(model,X,row_index,seed=43)
    va=np.array([a[k] for k in X.columns]); vb=np.array([b[k] for k in X.columns]); denom=np.linalg.norm(va)*np.linalg.norm(vb)
    return 0.0 if denom==0 else float(np.dot(va,vb)/denom)

def counterfactual_search(model,X,row_index,target_probability=.35,max_candidates=400,seed=42):
    rng=np.random.default_rng(seed); original=X.iloc[row_index].astype(float).copy(); base=float(model.predict_proba(pd.DataFrame([original]))[0,1]); candidates=[]
    for _ in range(max_candidates):
        c=original.copy(); c['income']*=rng.uniform(1.0,1.35); c['utilization']*=rng.uniform(.45,1.0)
        c['late_payments']=max(0,round(c['late_payments']-rng.integers(0,3))); c['credit_age']+=rng.uniform(0,2); c['debt_ratio']*=rng.uniform(.55,1.0); c['age']=original['age']
        p=float(model.predict_proba(pd.DataFrame([c]))[0,1])
        if p<=target_probability:
            distance=float(np.mean(np.abs((c-original)/(X.std().replace(0,1.0)))))
            candidates.append((distance,p,c))
    if not candidates: return {'found':False,'base_probability':base}
    distance,p,best=min(candidates,key=lambda z:z[0]); changes={k:float(best[k]-original[k]) for k in X.columns if abs(best[k]-original[k])>1e-9}
    return {'found':True,'base_probability':base,'new_probability':p,'distance':distance,'changes':changes}
