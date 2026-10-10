"""Leakage-safe 24h PM2.5 panel forecasting features, splits and interval evaluation."""
from collections import deque
from pathlib import Path
import numpy as np
import pandas as pd

POLLUTANTS=["PM2.5","PM10","SO2","NO2","CO","O3"]
WEATHER=["TEMP","PRES","DEWP","RAIN","WSPM"]
COMPASS={name:i*22.5 for i,name in enumerate(["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"])}

def load_uci(root):
    paths=sorted(Path(root).rglob("PRSA_Data_*.csv"))
    if not paths:return None
    parts=[]
    for path in paths:
        x=pd.read_csv(path)
        x["station"]=x.get("station",pd.Series([path.stem.split("_")[2]]*len(x))).fillna(path.stem.split("_")[2])
        x["ts"]=pd.to_datetime(x[["year","month","day","hour"]])
        parts.append(x[["station","ts",*POLLUTANTS,*WEATHER,"wd"]])
    return pd.concat(parts,ignore_index=True)

def synthetic_panel(seed=42,n_stations=6,start="2015-01-01",end="2016-12-31"):
    """Seeded synthetic smoke data; not real air-quality measurements."""
    r=np.random.default_rng(seed);ts=pd.date_range(start,end,freq="h",inclusive="left")
    t=np.arange(len(ts),dtype=np.float32)
    parts=[]
    for s in range(n_stations):
        daily=np.sin(2*np.pi*t/24);annual=np.sin(2*np.pi*t/(365.25*24))
        temp=13+13*annual+5*daily+r.normal(0,3,len(t))
        wspm=np.maximum(.1,2.5+1.2*np.sin(2*np.pi*t/(24*7))+r.normal(0,.7,len(t)))
        pm=np.maximum(1,55+8*s+28*annual+13*np.sin(2*np.pi*t/72+s)+r.normal(0,11,len(t))-3*wspm)
        pm=np.maximum(1,pm+np.where(t>len(t)*.8,12,0))
        d=pd.DataFrame({"station":f"S{s:02d}","ts":ts,"PM2.5":pm,"PM10":pm*1.45+r.normal(0,5,len(t)),
          "SO2":np.maximum(0,pm*.15+r.normal(0,3,len(t))),"NO2":np.maximum(0,pm*.35+r.normal(0,6,len(t))),
          "CO":np.maximum(0,pm*15+r.normal(0,80,len(t))),"O3":np.maximum(0,45+15*daily-.1*pm+r.normal(0,7,len(t))),
          "TEMP":temp,"PRES":1010+r.normal(0,7,len(t)),"DEWP":temp-7-r.random(len(t))*5,
          "RAIN":np.maximum(0,r.normal(-.7,1.5,len(t))),"WSPM":wspm,"wd":r.choice(list(COMPASS),len(t))})
        for col in ["PM2.5","TEMP","NO2"]:
            d.loc[r.choice(len(d),int(.012*len(d)),replace=False),col]=np.nan
        parts.append(d)
    return pd.concat(parts,ignore_index=True)

def features(raw,horizon=24):
    """Uses only measurements <= origin time; target from t+h; hourly grid prevents shift misalignment."""
    raw=raw.copy();raw["ts"]=pd.to_datetime(raw["ts"])
    groups=[]
    for station,x in raw.groupby("station",sort=True):
        x=x.sort_values("ts").drop_duplicates("ts",keep="last").set_index("ts")
        x=x.reindex(pd.date_range(x.index.min(),x.index.max(),freq="h"))
        x.index.name="ts";x["station"]=station
        pm=x["PM2.5"].astype("float32")
        x["target"]=pm.shift(-horizon)
        x["label_ts"]=x.index+pd.Timedelta(hours=horizon)
        for lag in [1,3,24,168]:x[f"pm25_lag_{lag}"]=pm.shift(lag)
        for window in [6,24,168]:
            x[f"pm25_mean_{window}"]=pm.rolling(window,min_periods=max(2,window//2)).mean()
        x["pm25_std_24"]=pm.rolling(24,min_periods=12).std()
        x["pm25_delta_24"]=pm-pm.shift(24)
        x["pm25_pm10_ratio"]=pm/(x["PM10"].clip(lower=1))
        x["dewpoint_spread"]=x["TEMP"]-x["DEWP"]
        x["ventilation_proxy"]=x["WSPM"]*x["dewpoint_spread"].clip(lower=0)
        wind=x["wd"].map(COMPASS)
        x["wind_sin"]=np.sin(np.deg2rad(wind));x["wind_cos"]=np.cos(np.deg2rad(wind))
        hour=x.index.hour;day=x.index.dayofyear
        x["hour_sin"]=np.sin(2*np.pi*hour/24);x["hour_cos"]=np.cos(2*np.pi*hour/24)
        x["annual_sin"]=np.sin(2*np.pi*day/365.25);x["annual_cos"]=np.cos(2*np.pi*day/365.25)
        x["weekday"]=x.index.dayofweek.astype("int8")
        x["pm25_missing_now"]=pm.isna().astype("int8")
        groups.append(x.reset_index().rename(columns={"index":"ts"}))
    df=pd.concat(groups,ignore_index=True)
    df=df.dropna(subset=["target"])
    df=df.sort_values(["ts","station"]).reset_index(drop=True)
    for col in df.select_dtypes(include=["float64"]).columns:df[col]=df[col].astype("float32")
    return df

DROP={"target","ts","label_ts","wd","No"}

def feature_columns(df):return [c for c in df.columns if c not in DROP]

def split_panel(df,heldout_stations=2,fracs=(.55,.15,.12,.18)):
    """Global time boundaries; label_ts <= split end; holdout stations excluded from fitting/calibration."""
    hours=np.sort(df["ts"].unique());n=len(hours)
    cuts=[pd.Timestamp(hours[min(n-1,int(n*p))]) for p in np.cumsum(fracs)[:3]]
    train_end,val_end,cal_end=cuts
    stations=sorted(df.station.unique());heldout=set(stations[-heldout_stations:]) if heldout_stations else set()
    seen=~df.station.isin(heldout)
    train=df[seen & (df.label_ts<=train_end)]
    val=df[seen & (df.ts>train_end) & (df.label_ts<=val_end)]
    cal=df[seen & (df.ts>val_end) & (df.label_ts<=cal_end)]
    test=df[df.ts>cal_end]
    assert train.label_ts.max()<=train_end and val.label_ts.max()<=val_end and cal.label_ts.max()<=cal_end
    assert not set(train.station).intersection(heldout)
    return {"train":train,"val":val,"cal":cal,"test":test,"heldout":heldout,"cuts":cuts}

def conformal_quantile(scores,alpha=.1):
    a=np.asarray(scores,dtype=float);a=a[np.isfinite(a)]
    if len(a)==0:raise ValueError("No finite calibration scores")
    level=min(1.,np.ceil((len(a)+1)*(1-alpha))/len(a))
    return float(np.quantile(a,level,method="higher"))

def interval_metrics(y,lo,hi,alpha=.1):
    y=np.asarray(y);lo=np.asarray(lo);hi=np.asarray(hi)
    valid=np.isfinite(y)&np.isfinite(lo)&np.isfinite(hi)
    if not valid.any():return {"n":0,"coverage":None,"width":None,"winkler":None}
    y=y[valid];lo=lo[valid];hi=hi[valid]
    penalty=2/alpha*((lo-y).clip(min=0)+(y-hi).clip(min=0))
    return {"n":int(len(y)),"coverage":float(np.mean((y>=lo)&(y<=hi))),"width":float(np.mean(hi-lo)),"winkler":float(np.mean(hi-lo+penalty))}

def delayed_adaptive_cqr(origin_ts,label_ts,y,base_lo,base_hi,cal_scores,alpha=.1,eta=.003,horizon_hours=24,window=3000):
    """Online rolling CQR with ACI alpha adjustment and strict delayed feedback.
    Each origin's interval is frozen before its label is known. Feedback only matures after >=h hours.
    All same-origin stations share the same pre-feedback threshold.
    """
    origin=pd.to_datetime(origin_ts).to_numpy();label=pd.to_datetime(label_ts).to_numpy()
    y=np.asarray(y,float);bl=np.asarray(base_lo,float);bh=np.asarray(base_hi,float)
    order=np.argsort(origin,kind="stable");scores=deque(np.asarray(cal_scores,float)[-window:].tolist(),maxlen=window)
    pending=deque();lo=np.empty(len(y));hi=np.empty(len(y));alpha_now=float(alpha)
    feedback_delays=[];n_feedback=0;idx=0
    while idx<len(order):
        current=origin[order[idx]]
        # At origin t, feedback is available only for targets with timestamp <= t.
        while pending and pending[0][0]<=current:
            mature,orig,score,miss=pending.popleft()
            scores.append(float(score));alpha_now=float(np.clip(alpha_now+eta*(alpha-float(miss)),.02,.35))
            feedback_delays.append(float((current-orig)/np.timedelta64(1,"h")));n_feedback+=1
        q=conformal_quantile(list(scores),alpha_now)
        j=idx
        while j<len(order) and origin[order[j]]==current:
            i=order[j];lo[i]=bl[i]-q;hi[i]=bh[i]+q
            score=max(bl[i]-y[i],y[i]-bh[i])
            miss=(y[i]<lo[i]) or (y[i]>hi[i])
            pending.append((label[i],origin[i],score,miss));j+=1
        idx=j
    return lo,hi,{"feedback_updates":n_feedback,"min_feedback_delay_hours":min(feedback_delays) if feedback_delays else None,"final_alpha":alpha_now}