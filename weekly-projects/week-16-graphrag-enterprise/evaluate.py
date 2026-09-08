import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from graphrag_enterprise.engine import GraphRAG
from graphrag_enterprise.metrics import recall_at_k,reciprocal_rank
e=GraphRAG(); rows=json.loads(Path("data/eval.json").read_text()); vals=[]
for x in rows:
    r=e.search(x["query"]); ids=[h["id"] for h in r["hits"]]
    vals.append((recall_at_k(ids,x["relevant_docs"],5),reciprocal_rank(ids,x["relevant_docs"])))
    print(x["query"],r["route"],ids)
print("mean_recall@5=",round(sum(x[0] for x in vals)/len(vals),4))
print("mrr=",round(sum(x[1] for x in vals)/len(vals),4))
