import numpy as np
def concordance_index(duration,event,risk):
    duration=np.asarray(duration,float);event=np.asarray(event,int);risk=np.asarray(risk,float)
    good=tied=n=0
    for i in range(len(duration)):
        if not event[i]: continue
        mask=duration>duration[i];n+=int(mask.sum());good+=int((risk[i]>risk[mask]).sum());tied+=int((risk[i]==risk[mask]).sum())
    return float((good+.5*tied)/n) if n else np.nan
def brier_at_horizon(duration,event,event_prob,h):
    duration=np.asarray(duration,float);event=np.asarray(event,int);p=np.asarray(event_prob,float)
    known=(duration>=h)|((event==1)&(duration<=h));y=((event==1)&(duration<=h)).astype(float)
    return float(np.mean((p[known]-y[known])**2))
