"""Leakage-aware URL-only phishing modeling; no network fetches at prediction time."""
from __future__ import annotations

import ipaddress
import math
import re
from collections import Counter
from urllib.parse import urlsplit, parse_qsl

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (average_precision_score, roc_auc_score, brier_score_loss,
                             log_loss, precision_score, recall_score, f1_score)

SEED = 20261024
SUSPICIOUS = ('verify', 'signin', 'account', 'secure', 'billing', 'confirm', 'login', 'wallet', 'reset', 'password')
FEATURES = ('url_length', 'host_length', 'path_length', 'query_length', 'host_digits', 'digit_ratio',
            'special_ratio', 'url_entropy', 'host_entropy', 'path_depth', 'param_count', 'hyphens',
            'subdomain_count', 'has_at', 'is_https', 'is_ip', 'punycode', 'suspicious_count',
            'max_token_length', 'encoded_chars')


def normalized_url(url: str) -> str:
    s = str(url).strip()
    return s if '://' in s else 'http://' + s


def hostname(url: str) -> str:
    try:
        return (urlsplit(normalized_url(url)).hostname or '').lower().rstrip('.')
    except ValueError:
        return ''


def group_domain(url: str) -> str:
    """Conservative root-domain approximation; see DATASET.md for ccTLD caveat."""
    host = hostname(url)
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    labels = [p for p in host.split('.') if p]
    if len(labels) <= 2:
        return host
    if len(labels[-1]) == 2 and labels[-2] in {'co','com','org','net','gov','ac','edu'}:
        return '.'.join(labels[-3:])
    return '.'.join(labels[-2:])


def entropy(s: str) -> float:
    if not s:
        return 0.0
    n = len(s)
    return -sum((v/n) * math.log2(v/n) for v in Counter(s).values())


def extract_one(url: str) -> dict[str, float]:
    s = str(url).strip()
    try:
        p = urlsplit(normalized_url(s))
        host = (p.hostname or '').lower()
        path, query = p.path or '', p.query or ''
    except ValueError:
        host, path, query = '', '', ''
        p = urlsplit('http://invalid.example')
    try:
        is_ip = int(bool(ipaddress.ip_address(host)))
    except ValueError:
        is_ip = 0
    tokens = re.findall(r'[a-zA-Z0-9]+', s)
    return {
        'url_length': len(s), 'host_length': len(host), 'path_length': len(path),
        'query_length': len(query), 'host_digits': sum(c.isdigit() for c in host),
        'digit_ratio': sum(c.isdigit() for c in s)/max(len(s),1),
        'special_ratio': sum(c in '@%&?=-_' for c in s)/max(len(s),1),
        'url_entropy': entropy(s), 'host_entropy': entropy(host),
        'path_depth': sum(bool(part) for part in path.split('/')),
        'param_count': len(parse_qsl(query, keep_blank_values=True)),
        'hyphens': host.count('-'), 'subdomain_count': max(0,len(host.split('.'))-2),
        'has_at': int('@' in s), 'is_https': int(p.scheme.lower() == 'https'),
        'is_ip': is_ip, 'punycode': int('xn--' in host),
        'suspicious_count': sum(word in s.lower() for word in SUSPICIOUS),
        'max_token_length': max((len(t) for t in tokens),default=0),
        'encoded_chars': s.count('%'),
    }


def featurize(urls) -> pd.DataFrame:
    return pd.DataFrame((extract_one(u) for u in urls), columns=FEATURES).astype('float32')


def clean_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Remove conflicting URL labels entirely, then exact URL duplicates; 1=phishing."""
    if not {'URL','label'}.issubset(df.columns):
        raise ValueError('Requires URL and label columns')
    d = df[['URL','label']].copy()
    d = d.dropna(subset=['URL','label'])
    d['URL'] = d['URL'].astype(str).str.strip()
    d['label'] = pd.to_numeric(d['label'], errors='coerce')
    d = d[d['label'].isin([0,1]) & d['URL'].ne('')].copy()
    contradictory = d.groupby('URL')['label'].nunique()
    conflicting = set(contradictory[contradictory>1].index)
    d = d[~d['URL'].isin(conflicting)].drop_duplicates('URL').reset_index(drop=True)
    d['target'] = (1-d['label']).astype('int8')
    d['domain_group'] = d['URL'].map(group_domain)
    d = d[d['domain_group'].ne('')].reset_index(drop=True)
    return d, {'conflicting_urls_removed':len(conflicting), 'clean_rows':len(d),
               'unique_groups':int(d['domain_group'].nunique())}


def make_synthetic(seed=SEED, domains=500, urls_per_domain=4) -> pd.DataFrame:
    """Reserved .example hosts only; nontrivial but NOT a benchmark for real-world efficacy."""
    rng = np.random.default_rng(seed)
    rows=[]
    for i in range(domains):
        label = int(rng.random() < 0.44)  # phishing class 1
        root = f"{rng.choice(['cloud','store','service','portal','support','client'])}{i:04d}.example"
        for j in range(urls_per_domain):
            phishing = label
            suspicious = rng.random() < (0.64 if phishing else 0.21)
            word = rng.choice(['verify','login','reset','account']) if suspicious else rng.choice(['home','docs','catalog','help'])
            https = rng.random() < (0.66 if phishing else 0.82)
            sub = rng.choice(['www.','secure.','id.',''])
            query = f'?ref={rng.integers(10,999)}' if rng.random()<0.48 else ''
            if rng.random() < (0.32 if phishing else 0.13):
                query += ('&' if query else '?')+f'account={rng.integers(100,999)}'
            url = f"{'https' if https else 'http'}://{sub}{root}/{word}/{rng.choice(['info','update','view','start'])}{query}&n={j}"
            rows.append({'URL':url,'label':1-phishing})
    return pd.DataFrame(rows)


def group_splits(df: pd.DataFrame, seed=SEED):
    """Group-disjoint train/validation/calibration/test, no test-driven reseeding."""
    idx = np.arange(len(df))
    groups = df['domain_group'].to_numpy()
    def take(pool, fraction, s):
        a,b = next(GroupShuffleSplit(n_splits=1,test_size=fraction,random_state=s).split(
            pool, groups=groups[pool]))
        return pool[a],pool[b]
    remain, test = take(idx, .15, seed)
    remain, cal = take(remain, .12, seed+1)
    train, val = take(remain, .20, seed+2)
    out={'train':train,'validation':val,'calibration':cal,'test':test}
    for a,ix in out.items():
        if len(set(df.iloc[ix]['target']))!=2:
            raise ValueError(f'{a} split has only one class; inspect domain imbalance')
        for b,jx in out.items():
            if a!=b and set(groups[ix]) & set(groups[jx]):
                raise AssertionError('Domain leakage')
    return out


def score(y, p, threshold=0.5, fp_cost=5., fn_cost=25.):
    y=np.asarray(y,dtype=int);p=np.clip(np.asarray(p,dtype=float),1e-7,1-1e-7)
    pred=(p>=threshold).astype(int)
    fp=int(((pred==1)&(y==0)).sum());fn=int(((pred==0)&(y==1)).sum())
    return {'n':len(y), 'prevalence':float(y.mean()),
            'pr_auc':float(average_precision_score(y,p)),
            'roc_auc':float(roc_auc_score(y,p)) if len(set(y))==2 else None,
            'brier':float(brier_score_loss(y,p)),
            'log_loss':float(log_loss(y,p,labels=[0,1])),
            'precision':float(precision_score(y,pred,zero_division=0)),
            'recall':float(recall_score(y,pred,zero_division=0)),
            'f1':float(f1_score(y,pred,zero_division=0)),
            'false_positives':fp,'false_negatives':fn,
            'cost_per_url':float((fp_cost*fp+fn_cost*fn)/len(y))}


def grouped_bootstrap_ci(y,p,groups,metric='pr_auc',seed=SEED,n_boot=200):
    """Bootstrap domain clusters, not individual URLs."""
    y=np.asarray(y);p=np.asarray(p);g=np.asarray(groups)
    keys,inv=np.unique(g,return_inverse=True)
    positions=[np.where(inv==i)[0] for i in range(len(keys))]
    rng=np.random.default_rng(seed)
    vals=[]
    for _ in range(n_boot):
        ix=np.concatenate([positions[i] for i in rng.integers(0,len(keys),len(keys))])
        if len(set(y[ix]))<2:
            continue
        vals.append(score(y[ix],p[ix])[metric])
    if not vals: return [None,None]
    return np.quantile(vals,[.025,.975]).tolist()


def tracking_perturb(url: str) -> str:
    return str(url)+ ('&' if '?' in str(url) else '?')+'utm_source=security_audit'