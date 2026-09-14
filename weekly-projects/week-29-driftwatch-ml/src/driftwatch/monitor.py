from __future__ import annotations
from dataclasses import dataclass
from .stats import ks_test,psi,mean_shift_effect,linear_mmd

@dataclass
class FeatureResult:
    feature:str
    drifted:bool
    severity:float
    ks_stat:float
    p_value:float
    psi:float
    mean_shift:float
    linear_mmd:float
    reason:str

class DriftMonitor:
    def __init__(self,min_batch_size=200,alpha=.01,psi_threshold=.2,mean_shift_threshold=.25):
        self.min_batch_size=min_batch_size; self.alpha=alpha
        self.psi_threshold=psi_threshold; self.mean_shift_threshold=mean_shift_threshold

    def inspect(self,reference:dict,current:dict):
        names=sorted(set(reference)&set(current))
        if not names:return []
        corrected_alpha=self.alpha/max(1,len(names)); rows=[]
        for name in names:
            r=reference[name]; c=current[name]
            if len(r)<self.min_batch_size or len(c)<self.min_batch_size:
                rows.append(FeatureResult(name,False,0,0,1,0,0,0,'insufficient_samples')); continue
            ks,p=ks_test(r,c); ps=psi(r,c); ms=mean_shift_effect(r,c); mmd=linear_mmd(r,c)
            signals=int(p<corrected_alpha)+int(ps>=self.psi_threshold)+int(ms>=self.mean_shift_threshold)
            drifted=signals>=2
            severity=max(min(1.0,ks*2),min(1.0,ps/0.5),min(1.0,ms/1.0))
            rows.append(FeatureResult(name,drifted,severity,ks,p,ps,ms,mmd,f'{signals}_of_3_signals'))
        return rows
