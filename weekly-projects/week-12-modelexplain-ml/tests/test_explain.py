from sklearn.ensemble import HistGradientBoostingClassifier
from modelexplain.data import make_dataset
from modelexplain.explain import local_surrogate,explanation_stability,counterfactual_search
from modelexplain.metrics import evaluate

def fitted():
    X,y=make_dataset(800,1); m=HistGradientBoostingClassifier(max_iter=60,random_state=1).fit(X,y); return X,y,m

def test_metrics():
    X,y,m=fitted(); p=m.predict_proba(X)[:,1]; r=evaluate(y,p); assert .5<=r['roc_auc']<=1 and 0<=r['ece']<=1

def test_local_explanation_has_features():
    X,y,m=fitted(); e=local_surrogate(m,X,0,n=100); assert set(e)==set(X.columns)

def test_stability_bounds():
    X,y,m=fitted(); s=explanation_stability(m,X,0); assert -1<=s<=1

def test_counterfactual_keeps_age_immutable():
    X,y,m=fitted(); r=counterfactual_search(m,X,0,target_probability=.8,max_candidates=100)
    if r['found']: assert 'age' not in r['changes']
