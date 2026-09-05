from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from src.synthetic import make_credit_like
from src.features import model_matrix
X,y=make_credit_like(1200,42); Xm=model_matrix(X); Xtr,Xte,ytr,yte=train_test_split(Xm,y,test_size=.25,stratify=y,random_state=42); m=HistGradientBoostingClassifier(max_iter=80,learning_rate=.08,max_leaf_nodes=15,random_state=42).fit(Xtr,ytr); p=m.predict_proba(Xte)[:,1]; auc=roc_auc_score(yte,p); print({'rows':len(X),'features':Xm.shape[1],'roc_auc':round(float(auc),4)}); assert auc>.65
