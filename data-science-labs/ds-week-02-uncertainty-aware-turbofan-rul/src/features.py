from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

SENSOR_COLS=[f's{i}' for i in range(1,22)]
SETTING_COLS=['setting1','setting2','setting3']
BASE_COLS=['unit','cycle']+SETTING_COLS+SENSOR_COLS

def add_rul(df,cap=125):
    out=df.copy();m=out.groupby('unit')['cycle'].transform('max');r=(m-out['cycle']).astype('float32')
    out['rul']=r.clip(upper=cap) if cap is not None else r
    return out

def load_cmapss_fd001(path):
    df=pd.read_csv(Path(path),sep=r'\s+',header=None,names=BASE_COLS,engine='python')
    df['unit']=df['unit'].astype('int32');df['cycle']=df['cycle'].astype('int32')
    for c in SETTING_COLS+SENSOR_COLS: df[c]=df[c].astype('float32')
    return add_rul(df)

def make_synthetic_fleet(n_engines=48,min_cycles=85,max_cycles=155,seed=42):
    rng=np.random.default_rng(seed);rows=[]
    for unit in range(1,n_engines+1):
        life=int(rng.integers(min_cycles,max_cycles+1));severity=rng.uniform(.8,1.25);regime=rng.normal(0,.15,3)
        for cycle in range(1,life+1):
            age=cycle/life;degradation=severity*max(0.,(age-.35)/.65)
            row={'unit':unit,'cycle':cycle,'setting1':regime[0]+rng.normal(0,.02),'setting2':regime[1]+rng.normal(0,.02),'setting3':regime[2]+rng.normal(0,.02)}
            for j in range(1,22):
                sign=-1. if j%3==0 else 1.;sensitivity=.15+(j%7)*.07;seasonal=.025*np.sin(cycle/(5+(j%5)));noise=rng.normal(0,.025+.003*(j%4))
                row[f's{j}']=1.+.03*j+seasonal+sign*sensitivity*degradation+noise
            rows.append(row)
    return add_rul(pd.DataFrame(rows))

def select_informative_sensors(train_df,min_std=1e-4):
    s=train_df[SENSOR_COLS].std();return s[s>min_std].index.tolist()

def add_health_indicator(train_df,other_frames,sensors,nominal_cycle_fraction=.20):
    mask=train_df['cycle']<=train_df.groupby('unit')['cycle'].transform('max')*nominal_cycle_fraction
    means=train_df.loc[mask,sensors].mean();stds=train_df.loc[mask,sensors].std().replace(0,1.)
    def transform(df):
        z=(df[sensors]-means)/stds;out=df.copy();out['health_index']=np.sqrt(z.pow(2).mean(axis=1)).astype('float32');return out
    return transform(train_df),[transform(x) for x in other_frames],means,stds

def add_temporal_features(df,sensors,windows=(5,15)):
    out=df.sort_values(['unit','cycle']).copy();g=out.groupby('unit',group_keys=False)
    for s in sensors[:8]:
        out[f'{s}_lag1']=g[s].shift(1)
        for w in windows:
            out[f'{s}_mean_{w}']=g[s].transform(lambda x:x.rolling(w,min_periods=2).mean())
            out[f'{s}_std_{w}']=g[s].transform(lambda x:x.rolling(w,min_periods=2).std())
            out[f'{s}_delta_{w}']=out[s]-g[s].shift(w)
    out['cycle_frac_proxy']=(out['cycle']/out.groupby('unit')['cycle'].transform('max')).astype('float32')
    return out

def production_feature_columns(df):
    blocked={'unit','rul','cycle_frac_proxy'}
    return [c for c in df.columns if c not in blocked and not c.startswith('setting')]

def assign_regime_from_train(train_df,frames,quantile=.60):
    threshold=float(train_df['health_index'].quantile(quantile))
    def transform(df):
        out=df.copy();out['regime']=(out['health_index']>=threshold).astype('int8');return out
    return transform(train_df),[transform(x) for x in frames],threshold
