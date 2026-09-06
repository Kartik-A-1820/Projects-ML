import numpy as np
import pandas as pd

FEATURES=['income','utilization','late_payments','credit_age','debt_ratio','age']

def make_dataset(n=2500,seed=42):
    rng=np.random.default_rng(seed)
    income=rng.lognormal(10.5,.55,n)
    utilization=np.clip(rng.beta(2.2,3.8,n),0,1)
    late=rng.poisson(1.1,n)
    credit_age=np.clip(rng.normal(7,4,n),.2,25)
    debt_ratio=np.clip(rng.beta(2.0,4.0,n),0,1.5)
    age=np.clip(rng.normal(38,11,n),18,75)
    logit=(-2.1+2.7*utilization+.38*late+1.3*debt_ratio-.000015*income-.07*credit_age)
    p=1/(1+np.exp(-logit)); y=rng.binomial(1,p)
    X=pd.DataFrame({'income':income,'utilization':utilization,'late_payments':late,'credit_age':credit_age,'debt_ratio':debt_ratio,'age':age})
    return X,pd.Series(y,name='default')
