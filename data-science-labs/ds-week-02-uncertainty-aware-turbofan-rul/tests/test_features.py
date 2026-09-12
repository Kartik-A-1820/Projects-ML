import numpy as np
from src.features import make_synthetic_fleet,select_informative_sensors,add_health_indicator,add_temporal_features,production_feature_columns
from src.metrics import regression_metrics,interval_metrics

def test_synthetic_rul_nonnegative_and_ends_zero():
    df=make_synthetic_fleet(n_engines=5,seed=1);assert df['rul'].min()==0;assert (df.sort_values(['unit','cycle']).groupby('unit').tail(1)['rul']==0).all()

def test_temporal_features_are_production_safe():
    df=make_synthetic_fleet(n_engines=4,min_cycles=30,max_cycles=35,seed=2);s=select_informative_sensors(df);out=add_temporal_features(df,s);assert any(c.endswith('_lag1') for c in out.columns);assert 'cycle_frac_proxy' not in production_feature_columns(out)

def test_health_indicator_finite():
    df=make_synthetic_fleet(n_engines=6,seed=3);train,others,_,_=add_health_indicator(df,[df.copy()],select_informative_sensors(df));assert np.isfinite(train['health_index']).all();assert np.isfinite(others[0]['health_index']).all()

def test_metrics_bounds():
    y=np.array([10,20,30]);p=np.array([11,18,31]);m=regression_metrics(y,p);assert m['rmse']>=0;assert 0<=interval_metrics(y,y-2,y+2)['coverage']<=1
