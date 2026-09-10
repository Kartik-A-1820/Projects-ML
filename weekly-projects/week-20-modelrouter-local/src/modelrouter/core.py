from __future__ import annotations
from dataclasses import dataclass
import json,re
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
HARD={"design","debug","prove","root","cause","adversarial","architecture","confounders","tradeoffs","optimize"};SECURITY={"security","authentication","privilege","adversarial","unsafe","attack"};CODING={"code","sql","regex","cuda","async","dynamic","programming","debug"}
def featurize(query,metadata=None):
 metadata=metadata or {};q=query.lower();toks=re.findall(r"[a-z0-9_]+",q);return np.array([min(len(toks)/80,1.5),float(metadata.get("requires_tools",any(x in q for x in ["logs","metrics","filesystem","tool"]))),min(float(metadata.get("reasoning_steps",1))/5,1),float(metadata.get("coding",any(x in toks for x in CODING))),float(metadata.get("safety",any(x in toks for x in SECURITY))),min(sum(x in toks for x in HARD)/3,1)],dtype=np.float32)
@dataclass(frozen=True)
class RouteDecision: model:str;score:float;reason:str
@dataclass(frozen=True)
class ModelSpec: name:str;quality_prior:float;cost_units:float;p95_latency_ms:int;reliability:float=.99;healthy:bool=True
DEFAULT_MODELS=[ModelSpec("small",.64,1,180),ModelSpec("medium",.79,2.7,420),ModelSpec("strong",.91,8,1200)]
class MarginalGainRouter:
 def __init__(self,strong_gain_threshold=.16,medium_gain_threshold=.08):
  self.st=strong_gain_threshold;self.mt=medium_gain_threshold;self.strong=LogisticRegression(max_iter=500,random_state=42);self.medium=LogisticRegression(max_iter=500,random_state=43)
 def fit(self,rows):
  X=np.stack([featurize(r["query"],r) for r in rows]);ys=np.array([r["strong"]-r["small"]>=self.st for r in rows],int);ym=np.array([r["medium"]-r["small"]>=self.mt for r in rows],int);self.strong.fit(X,ys);self.medium.fit(X,ym);return self
 def predict(self,q,meta=None):
  X=featurize(q,meta).reshape(1,-1);ps=float(self.strong.predict_proba(X)[0,1]);pm=float(self.medium.predict_proba(X)[0,1]);return ("strong",ps) if ps>=.5 else (("medium",pm) if pm>=.5 else ("small",max(1-ps,1-pm)))
def load_rows(path="data/routing_supervision.json"):return json.loads(Path(path).read_text())
def choose(models,desired,max_cost,max_latency,reliability=.9):
 eligible=[m for m in models if m.healthy and m.reliability>=reliability and m.cost_units<=max_cost and m.p95_latency_ms<=max_latency]
 if not eligible:raise RuntimeError("no eligible model")
 order={"small":0,"medium":1,"strong":2};target=order[desired];return sorted(eligible,key=lambda m:(abs(order[m.name]-target),m.cost_units))[0]
class ModelRouter:
 def __init__(self,models=None,learned=None):self.models=models or DEFAULT_MODELS;self.learned=learned
 def route(self,q,meta=None,max_cost=8,max_latency_ms=1400,reliability_floor=.9):
  desired,score=self.learned.predict(q,meta);m=choose(self.models,desired,max_cost,max_latency_ms,reliability_floor);return RouteDecision(m.name,score,"learned_marginal_gain"+("+constraint_fallback" if m.name!=desired else ""))
def evaluate_routes(rows,decisions,costs):
 qs=[r[d] for r,d in zip(rows,decisions)];cs=[costs[d] for d in decisions];oracle=[max(("small","medium","strong"),key=lambda m:r[m]-.02*costs[m]) for r in rows];return {"mean_quality":float(np.mean(qs)),"mean_cost":float(np.mean(cs)),"strong_call_rate":sum(d=="strong" for d in decisions)/len(decisions),"quality_regret_vs_oracle":float(np.mean([r[o] for r,o in zip(rows,oracle)])-np.mean(qs))}
