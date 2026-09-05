import numpy as np
from src.synthetic import make_credit_like
from src.features import engineer_credit_features,model_matrix
from src.metrics import expected_calibration_error
from src.conformal import conformal_quantile,prediction_sets,coverage_and_size

def test_feature_engineering():
    X,_=make_credit_like(200,7); eng=engineer_credit_features(X); assert np.isfinite(eng.to_numpy(dtype=float)).all(); mm=model_matrix(X)
    for c in ['ID','SEX','MARRIAGE','EDUCATION','AGE']: assert c not in mm.columns
    assert 'delinq_recency_weighted' in mm.columns

def test_ece_bounds():
    assert 0<=expected_calibration_error(np.array([0,1]),np.array([.1,.9]))<=1

def test_conformal():
    y=np.array([0,1,0,1,1,0]); p=np.array([.1,.8,.2,.7,.6,.4]); q=conformal_quantile(y,p,.2); s=prediction_sets(p,q); cov,size=coverage_and_size(y,s); assert s.shape==(6,2); assert 0<=cov<=1 and 0<=size<=2
