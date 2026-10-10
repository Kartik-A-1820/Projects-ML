import numpy as np,pandas as pd
from src.forecasting import synthetic_panel,features,split_panel,conformal_quantile,interval_metrics,delayed_adaptive_cqr

def test_features_do_not_look_forward():
    x=synthetic_panel(n_stations=1,start="2015-01-01",end="2015-02-01")
    a=features(x,24)
    x.loc[(x.ts==pd.Timestamp("2015-01-12 12:00")),"PM2.5"]=999999.
    b=features(x,24)
    # A future spike cannot change features for a prior origin.
    col="pm25_mean_24";t=pd.Timestamp("2015-01-10 12:00")
    assert np.isclose(a.loc[a.ts==t,col].iloc[0],b.loc[b.ts==t,col].iloc[0],equal_nan=True)

def test_label_aware_split():
    x=features(synthetic_panel(n_stations=3,start="2015-01-01",end="2015-06-01"))
    s=split_panel(x,1)
    for name,cut in zip(["train","val","cal"],s["cuts"]):
        assert s[name].label_ts.max()<=cut
    assert s["heldout"].isdisjoint(set(s["train"].station))

def test_conformal_and_interval():
    assert conformal_quantile([0,1,2,3,4,5,6,7,8,9],.2)>=7
    m=interval_metrics([2,5],[1,1],[3,4],.1)
    assert m["coverage"]==.5 and m["winkler"]>m["width"]

def test_delayed_feedback_no_peeking():
    t=pd.date_range("2016-01-01",periods=100,freq="h")
    y=np.full(100,20.);y[1]=99999.
    l,h,info=delayed_adaptive_cqr(t,t+pd.Timedelta(hours=24),y,np.zeros(100),np.ones(100),[1.]*50,window=100)
    # A huge surprise at hour 1 cannot alter intervals before hour 25.
    assert np.allclose(h[:25],h[0]);assert info["min_feedback_delay_hours"]>=24