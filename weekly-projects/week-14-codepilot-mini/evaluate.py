import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from codepilot.index import scan_repository
from codepilot.retrieval import RepositoryRetriever
from codepilot.metrics import recall_at_k,reciprocal_rank

r=RepositoryRetriever(scan_repository("sample_repo"))
rows=json.loads(Path("data/eval_issues.json").read_text())
metrics=[]
for x in rows:
    ranked=[f.path for _,f in r.search(x["issue"],5)]
    rec=recall_at_k(ranked,x["relevant"],5); rr=reciprocal_rank(ranked,x["relevant"])
    metrics.append((rec,rr))
    print(x["issue"],ranked)
print("mean_recall@5=",round(sum(x[0] for x in metrics)/len(metrics),4))
print("mrr=",round(sum(x[1] for x in metrics)/len(metrics),4))
