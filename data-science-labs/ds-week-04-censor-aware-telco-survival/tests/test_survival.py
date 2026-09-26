import numpy as np
from src.metrics import concordance_index,brier_at_horizon
from src.survival import km_curve,DiscreteTimeHazard
def test_km_decreases():
    s=[x[1] for x in km_curve([1,2,3,4],[1,0,1,1])];assert all(a>=b for a,b in zip(s,s[1:]))
def test_cindex_perfect(): assert concordance_index([1,2,3],[1,1,1],[3,2,1])==1.
def test_brier_finite(): assert np.isfinite(brier_at_horizon([2,5,8],[1,0,1],[.8,.2,.4],4))
def test_model_shapes():
    X=np.array([[0.],[1.],[2.],[3.]],dtype=np.float32);m=DiscreteTimeHazard(6).fit(X,np.array([2,4,5,6]),np.array([1,0,1,0]));assert m.survival(X,[2,4]).shape==(4,2)
