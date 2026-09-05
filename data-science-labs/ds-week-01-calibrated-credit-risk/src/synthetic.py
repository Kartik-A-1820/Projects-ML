import numpy as np
import pandas as pd

def make_credit_like(n=4000,seed=42):
    rng=np.random.default_rng(seed); limit=rng.choice([20000,50000,100000,150000,200000,300000,500000],size=n).astype(float); age=rng.integers(21,70,size=n); sex=rng.integers(1,3,size=n); education=rng.choice([1,2,3,4],size=n,p=[.25,.45,.25,.05]); marriage=rng.choice([1,2,3],size=n,p=[.45,.5,.05]); base=np.clip(rng.beta(2,2,size=n)+rng.normal(0,.08,n),0,1.6); latent=rng.normal(0,1,n); status=[]; bills=[]; pays=[]
    for m in range(6):
        delay=np.clip(np.round(latent+rng.normal(0,1,n)-.4).astype(int),-2,6); status.append(delay); bill=limit*np.clip(base+rng.normal(0,.12,n)+.04*m,-.1,1.8); payment=np.maximum(0,bill*np.clip(rng.beta(2.5,6,size=n)-.04*np.maximum(delay,0),0,1)); bills.append(bill); pays.append(payment)
    logit=-2.3+1.15*np.maximum(status[0],0)+.55*np.maximum(status[1],0)+1.4*(base>1.0)-.0000012*limit; p=1/(1+np.exp(-logit)); y=rng.binomial(1,p)
    data={'ID':np.arange(1,n+1),'LIMIT_BAL':limit,'SEX':sex,'EDUCATION':education,'MARRIAGE':marriage,'AGE':age}
    for c,v in zip(['PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6'],status): data[c]=v
    for i,v in enumerate(bills,1): data[f'BILL_AMT{i}']=v
    for i,v in enumerate(pays,1): data[f'PAY_AMT{i}']=v
    return pd.DataFrame(data),pd.Series(y,name='default')
