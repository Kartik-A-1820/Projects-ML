import hashlib,time,numpy as np
from .embedding import embed
from .store import Entry

def key_for(query,tenant,model_version,prompt_version):
    raw='|'.join([tenant,model_version,prompt_version,' '.join(query.lower().split())])
    return hashlib.sha256(raw.encode()).hexdigest()

def freshness_risk(entry,now=None,risk_per_hour=.01):
    age=max(0,(now or time.time())-entry.created_at)/3600
    return min(1.0,age*risk_per_hour)

class SemanticCache:
    def __init__(self,store,hit_threshold=.78,verify_lower_bound=.60,max_stale_risk=.12):
        self.store=store; self.hit_threshold=hit_threshold; self.verify_lower_bound=verify_lower_bound; self.max_stale_risk=max_stale_risk; self.verify_queue=[]
    def lookup(self,query,tenant='default',model_version='m1',prompt_version='p1',now=None):
        k=key_for(query,tenant,model_version,prompt_version)
        if k in self.store.entries:
            e=self.store.entries[k]
            if not self.store.expired(e,now) and freshness_risk(e,now)<=self.max_stale_risk:
                return {'status':'exact_hit','response':e.response,'score':1.0}
        qv=embed(query); best=None
        for e in self.store.values():
            if (e.tenant,e.model_version,e.prompt_version)!=(tenant,model_version,prompt_version): continue
            if self.store.expired(e,now) or freshness_risk(e,now)>self.max_stale_risk: continue
            s=float(np.dot(qv,e.vector))
            if best is None or s>best[0]: best=(s,e)
        if not best: return {'status':'miss','score':0.0}
        s,e=best
        if s>=self.hit_threshold: return {'status':'semantic_hit','response':e.response,'score':s,'source_key':e.key}
        if s>=self.verify_lower_bound:
            self.verify_queue.append({'query':query,'candidate_key':e.key,'score':s})
            return {'status':'verify_candidate','score':s}
        return {'status':'miss','score':s}
    def insert(self,query,response,tenant='default',model_version='m1',prompt_version='p1',ttl=3600,curated=False,now=None):
        k=key_for(query,tenant,model_version,prompt_version)
        self.store.put(Entry(k,query,response,embed(query),now or time.time(),ttl,tenant,model_version,prompt_version,curated))
        return k
