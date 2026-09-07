import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from videorag.io import load_events
from videorag.retrieval import VideoRetriever
from videorag.metrics import recall_at_k,reciprocal_rank

r=VideoRetriever(load_events("data/events.json"))
qs=json.loads(Path("data/eval_queries.json").read_text())
rows=[]
for q in qs:
    ids=[h.event_id for h in r.search(q["query"],5)]
    rows.append((recall_at_k(ids,q["relevant"],5),reciprocal_rank(ids,q["relevant"])))
    print(q["query"],ids)
print("mean_recall@5=",round(sum(x[0] for x in rows)/len(rows),4))
print("mrr=",round(sum(x[1] for x in rows)/len(rows),4))
