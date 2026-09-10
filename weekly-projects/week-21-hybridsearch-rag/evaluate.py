import json,sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from hybridrag.core import HybridEngine,recall_at_k,reciprocal_rank,ndcg_at_k
rows=json.loads(Path("data/eval.json").read_text());e=HybridEngine();by=defaultdict(list)
for x in rows:
 r=e.search(x["query"]);ids=[h["id"] for h in r["hits"]];m=(recall_at_k(ids,x["relevant"],5),reciprocal_rank(ids,x["relevant"]),ndcg_at_k(ids,x["relevant"],5));by[r["family"]].append(m);print(x["query"],"=>",r["family"],ids,m)
for fam,vals in by.items():print(fam,{"recall@5":sum(x[0] for x in vals)/len(vals),"mrr":sum(x[1] for x in vals)/len(vals),"ndcg@5":sum(x[2] for x in vals)/len(vals)})
