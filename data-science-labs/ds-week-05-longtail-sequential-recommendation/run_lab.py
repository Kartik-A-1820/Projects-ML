"""Runnable reconstruction of DS Week 05; old metrics are historical only."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
from src.metrics import recall_at_k, mrr_at_k, ndcg_at_k, coverage, tail_share
from src.recommender import Recommenders

def synthetic(users=100, items=100, seed=42):
    if users<1 or items<10:
        raise ValueError('Need positive users and at least 10 items')
    rng=np.random.default_rng(seed)
    probabilities=1./np.arange(1,items+1)**.8
    probabilities/=probabilities.sum()
    return [(user,int(item),5,step) for user in range(users) for step,item in enumerate(rng.choice(items,min(20,items),replace=False,p=probabilities))]

def load_movielens(path):
    result=[]
    for line in Path(path).read_text().splitlines():
        user,item,rating,timestamp=line.split('::')
        result.append((int(user),int(item),float(rating),int(timestamp)))
    return result

def split_events(events):
    by_user=defaultdict(list)
    for user,item,rating,timestamp in events:
        if rating>=4:
            by_user[user].append((timestamp,item))
    train,validation,test={},{},{}
    for user,events in sorted(by_user.items()):
        # First positive per user/item; repeat-consumption prediction is out of scope.
        seen=set()
        history=[]
        for timestamp,item in sorted(events):
            if item not in seen:
                seen.add(item)
                history.append(item)
        if len(history)>=5:
            train[user],validation[user],test[user]=history[:-2],history[-2],history[-1]
    if not train:
        raise ValueError('No users with at least five distinct positive items')
    return train,validation,test

def evaluate(model,train,validation,test,split='test',k=10,tail_bonus=.5,seed=42):
    results={}
    for method in ('popularity','markov','bpr','bpr_tail'):
        rankings=[]
        values=[]
        cold=0
        for user,history in sorted(train.items()):
            context=history+([validation[user]] if split=='test' else [])
            target=test[user] if split=='test' else validation[user]
            cold+=target not in model.item_index
            ranking=model.recommend(user,context,method,k,tail_bonus)
            rankings.append(ranking)
            values.append((recall_at_k(ranking,target,k),ndcg_at_k(ranking,target,k),mrr_at_k(ranking,target,k)))
        array=np.asarray(values)
        rng=np.random.default_rng(seed)
        bootstrap=[float(array[rng.integers(len(array),size=len(array)),1].mean()) for _ in range(200)]
        results[method]={'recall':float(array[:,0].mean()),'ndcg':float(array[:,1].mean()),'mrr':float(array[:,2].mean()),'coverage':coverage(rankings,model.items),'tail_exposure':tail_share(rankings,model.tail),'ndcg_ci95':np.quantile(bootstrap,[.025,.975]).tolist(),'cold_targets':int(cold)}
    return results

def run(events,source,seed=42,k=10,epochs=3,tail_bonus=.5):
    train,validation,test=split_events(events)
    model=Recommenders(train,seed=seed,epochs=epochs)
    return {'source':source,'seed':seed,'k':k,'epochs':epochs,'tail_bonus':tail_bonus,'users':len(train),'train_catalog':len(model.items),'train_events':sum(map(len,train.values())),'python':platform.python_version(),'numpy':np.__version__,'validation':evaluate(model,train,validation,test,'validation',k,tail_bonus,seed),'test':evaluate(model,train,validation,test,'test',k,tail_bonus,seed),'limitations':['Synthetic runs verify code only, not MovieLens quality.','Per-user chronology is not a globally time-censored deployment simulation.','Unseen held-out targets remain misses; training catalog uses no held-out items.','Tail exposure is descriptive, not a causal exposure-bias correction.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--ratings',type=Path,help='MovieLens 1M ratings.dat; no automatic download')
    parser.add_argument('--output',type=Path,default=Path('artifacts/maintenance_smoke.json'))
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--k',type=int,default=10)
    parser.add_argument('--epochs',type=int,default=3)
    parser.add_argument('--tail-bonus',type=float,default=.5)
    args=parser.parse_args()
    if args.k<1 or args.epochs<1 or args.tail_bonus<0:
        parser.error('k/epochs must be positive and tail-bonus nonnegative')
    if args.ratings:
        events=load_movielens(args.ratings)
        source='MOVIELENS_1M:'+hashlib.sha256(args.ratings.read_bytes()).hexdigest()
    else:
        events=synthetic(seed=args.seed)
        source='SYNTHETIC_SMOKE_RECONSTRUCTION'
    report=run(events,source,args.seed,args.k,args.epochs,args.tail_bonus)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
