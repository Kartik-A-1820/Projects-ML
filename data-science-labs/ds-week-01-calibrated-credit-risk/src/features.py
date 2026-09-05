from __future__ import annotations
import numpy as np
import pandas as pd

PAY_STATUS=["PAY_0","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6"]
BILLS=[f"BILL_AMT{i}" for i in range(1,7)]
PAYS=[f"PAY_AMT{i}" for i in range(1,7)]
SENSITIVE_DIAGNOSTIC=["SEX","MARRIAGE","EDUCATION","AGE"]

def _row_slope(frame):
    x=np.arange(frame.shape[1],dtype=float); xc=x-x.mean(); denom=float(np.dot(xc,xc))
    values=frame.to_numpy(dtype=float); centered=values-values.mean(axis=1,keepdims=True)
    return (centered@xc)/denom

def engineer_credit_features(df):
    out=df.copy(); limit=out["LIMIT_BAL"].clip(lower=1.0)
    bills=out[BILLS].astype(float); pays=out[PAYS].astype(float); status=out[PAY_STATUS].astype(float)
    util=bills.div(limit,axis=0); pay_ratio=pays/(bills.abs().to_numpy()+1.0)
    out["util_mean"]=util.mean(axis=1); out["util_max"]=util.max(axis=1); out["util_std"]=util.std(axis=1)
    out["bill_pressure"]=bills.mean(axis=1)/limit; out["bill_volatility"]=bills.std(axis=1)/limit; out["bill_slope"]=_row_slope(bills)/limit
    out["payment_ratio_mean"]=pay_ratio.mean(axis=1); out["payment_ratio_max"]=pay_ratio.max(axis=1); out["payment_ratio_std"]=pay_ratio.std(axis=1)
    out["payment_volatility"]=pays.std(axis=1)/limit; out["payment_slope"]=_row_slope(pays)/limit
    out["delinq_count"]=(status>0).sum(axis=1); out["severe_delinq_count"]=(status>=2).sum(axis=1)
    out["delinq_max"]=status.max(axis=1); out["delinq_mean"]=status.mean(axis=1)
    weights=np.array([6,5,4,3,2,1],dtype=float)
    out["delinq_recency_weighted"]=(status.to_numpy()*weights).sum(axis=1)/weights.sum()
    out["delinq_recent_minus_old"]=status.iloc[:,:2].mean(axis=1)-status.iloc[:,-2:].mean(axis=1)
    return out.replace([np.inf,-np.inf],np.nan).fillna(0.0)

def model_matrix(df):
    out=engineer_credit_features(df)
    return out.drop(columns=[c for c in ["ID",*SENSITIVE_DIAGNOSTIC] if c in out.columns])
