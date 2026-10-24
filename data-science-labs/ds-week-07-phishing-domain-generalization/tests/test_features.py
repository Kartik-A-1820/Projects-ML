import numpy as np
import pandas as pd
from phishing_lab import (extract_one,featurize,clean_frame,make_synthetic,group_splits,
                          group_domain,tracking_perturb,grouped_bootstrap_ci)

def test_url_only_features():
    x=extract_one('https://secure.example.com/verify/login?token=123')
    assert x['suspicious_count']>=2 and x['param_count']==1
    assert set(x)==set(featurize(['https://x.example/']).columns)
    assert 'target' not in x

def test_domain_grouping():
    assert group_domain('https://a.b.example.com/a')==group_domain('https://b.example.com/b')
    assert group_domain('https://a.example.co.uk')=='example.co.uk'

def test_conflict_removed():
    d,stats=clean_frame(pd.DataFrame({'URL':['http://a.example','http://a.example','http://b.example'], 'label':[0,1,1]}))
    assert len(d)==1 and stats['conflicting_urls_removed']==1

def test_group_disjoint():
    d,_=clean_frame(make_synthetic(domains=120))
    s=group_splits(d)
    for a,i in s.items():
        for b,j in s.items():
            if a!=b: assert set(d.iloc[i].domain_group).isdisjoint(d.iloc[j].domain_group)

def test_perturb_and_bootstrap():
    assert 'utm_source=' in tracking_perturb('https://a.example/?x=1')
    y=np.array([0,1,0,1]*10);p=np.array([.1,.9,.3,.7]*10)
    ci=grouped_bootstrap_ci(y,p,np.arange(40),n_boot=20)
    assert ci[0]<=ci[1]