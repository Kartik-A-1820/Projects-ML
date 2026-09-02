import numpy as np
from sentiment_lab.metrics import expected_calibration_error,find_temperature,negative_log_likelihood,softmax
from sentiment_lab.slices import slice_masks

def test_softmax():
    p=softmax(np.array([[1.,2.,3.],[0.,0.,0.]])); assert np.allclose(p.sum(axis=1),1.0)

def test_temperature_search():
    l=np.array([[3.,0.],[0.,3.],[2.,1.]]); y=np.array([0,1,0]); t=find_temperature(l,y); assert t>0; assert negative_log_likelihood(l,y,t)<=negative_log_likelihood(l,y,3.0)

def test_ece_and_slices():
    e=expected_calibration_error(np.array([[.9,.1],[.2,.8]]),np.array([0,1])); assert 0<=e<=1
    assert bool(slice_masks(['not good','tiny'])['has_negation'][0])
