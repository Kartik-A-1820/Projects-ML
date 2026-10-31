import numpy as np
from src.har import synthetic,split_subjects,engineer,rotate_and_noise
from src.learning import masked_positions,stratified_budget
from src.metrics import evaluate,cluster_ci,selective,temperature_calibrate
import torch

def test_subject_isolation():
    x,y,s,split,_=synthetic(n_subjects=20,windows_per_subject=12)
    parts=split_subjects(s,split)
    for a,idx in parts.items():
        for b,jdx in parts.items():
            if a!=b:assert set(s[idx]).isdisjoint(s[jdx])

def test_features_no_nan():
    x,*_=synthetic(n_subjects=8,windows_per_subject=8)
    f=engineer(x);assert len(f)==len(x) and np.isfinite(f.to_numpy()).all()
    assert not any('subject' in c or 'label' in c for c in f.columns)

def test_augment_shape():
    x,*_=synthetic(n_subjects=8,windows_per_subject=8)
    z=rotate_and_noise(x,drop_gyro=True)
    assert z.shape==x.shape and np.all(z[:,:,3:6]==0)

def test_mask_and_budget():
    x,y,s,sp,_=synthetic(n_subjects=10,windows_per_subject=12)
    mask=masked_positions(torch.tensor(x[:8]),torch.Generator().manual_seed(2))
    assert mask.shape==(8,128,9) and mask.any()
    idx=np.arange(len(y));small=stratified_budget(y,idx,.1)
    assert set(y[small])==set(y) and len(small)<len(idx)

def test_metrics():
    y=np.array([0,1,0,1,0,1]);p=np.array([[.8,.2],[.1,.9],[.6,.4],[.3,.7],[.7,.3],[.4,.6]])
    assert evaluate(y,p)['accuracy']==1
    assert len(cluster_ci(y,p,np.array([1,1,2,2,3,3]),n_boot=8))==2
    assert selective(y,p)['coverage']<=1
    temp,q=temperature_calibrate(p,y,p)
    assert temp>0 and np.allclose(q.sum(axis=1),1)
