import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from modelexplain.data import make_dataset
from modelexplain.metrics import evaluate
from modelexplain.explain import global_permutation_importance,local_surrogate,explanation_stability,counterfactual_search

X,y=make_dataset(); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,stratify=y,random_state=42)
m=HistGradientBoostingClassifier(max_iter=140,learning_rate=.06,max_leaf_nodes=24,random_state=42).fit(Xtr,ytr)
p=m.predict_proba(Xte)[:,1]
print('metrics',evaluate(yte,p)); print('global',global_permutation_importance(m,Xte,yte)[:4])
print('local',local_surrogate(m,Xte.reset_index(drop=True),0)); print('stability',round(explanation_stability(m,Xte.reset_index(drop=True),0),4))
print('counterfactual',counterfactual_search(m,Xte.reset_index(drop=True),0))
