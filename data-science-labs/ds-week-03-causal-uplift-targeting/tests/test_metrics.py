import numpy as np
from src.metrics import ate, policy_value_ipw, qini_auc

def test_ate_positive():
    y=np.array([0,1,0,1,1,1]); w=np.array([0,0,0,1,1,1]); assert ate(y,w)>0

def test_policy_value_finite():
    y=np.array([0,1,0,1]);w=np.array([0,0,1,1]);p=np.array([0,1,0,1]); assert np.isfinite(policy_value_ipw(y,w,p))

def test_qini_finite():
    y=np.array([0,1,0,1,1,0,1,0]);w=np.array([0,0,1,1,0,1,1,0]);u=np.arange(8); assert np.isfinite(qini_auc(y,w,u))
