import numpy as np

def reference_data(n=1000,seed=42):
    rng=np.random.default_rng(seed)
    return {'amount':rng.lognormal(3.2,.45,n),'latency':rng.gamma(4,22,n),'score':rng.beta(8,2,n)}

def stream_window(n=300,seed=42,shift=0.0):
    rng=np.random.default_rng(seed)
    return {
        'amount':rng.lognormal(3.2+shift*.18,.45,n),
        'latency':rng.gamma(4,22*(1+shift*.20),n),
        'score':np.clip(rng.beta(8,2,n)-shift*.12,0,1),
    }
