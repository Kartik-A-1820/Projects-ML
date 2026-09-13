import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from visionrag.synthetic import generate_dataset,make_image
from visionrag.index import ExemplarIndex
from visionrag.engine import VisionRAG
from visionrag.metrics import accuracy,abstention_rate,retrieval_recall_at_k

rows=generate_dataset()
Path("data/manifest.json").write_text(json.dumps(rows,indent=2))
e=VisionRAG(ExemplarIndex.build("data/manifest.json"),min_similarity=.70)
results=[]
for i,label in enumerate(["normal","scratch","dent"]*5):
    r=e.predict(make_image(label,9000+i))
    results.append({**r,"truth":label})
print({
 "accuracy_on_grounded":accuracy(results),
 "abstention_rate":abstention_rate(results),
 "retrieval_recall@3":sum(retrieval_recall_at_k(r["evidence"],r["truth"],3) for r in results)/len(results)
})
