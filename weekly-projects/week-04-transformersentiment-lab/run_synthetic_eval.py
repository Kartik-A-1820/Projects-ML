import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from sentiment_lab.metrics import expected_calibration_error,find_temperature,softmax
logits=np.array([[5.,1.,.1],[.5,2.,.2],[.3,1.,3.],[3.,1.,.5]]); labels=np.array([0,1,2,0]); t=find_temperature(logits,labels)
print('temperature=',round(t,3)); print('ece=',round(expected_calibration_error(softmax(logits,t),labels),4))
