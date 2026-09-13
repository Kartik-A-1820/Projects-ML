import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from visionrag.synthetic import generate_dataset,make_image
from visionrag.index import ExemplarIndex
from visionrag.engine import VisionRAG

rows=generate_dataset()
Path("data/manifest.json").write_text(json.dumps(rows,indent=2))
e=VisionRAG(ExemplarIndex.build("data/manifest.json"),min_similarity=.70)
for label,seed in [("scratch",7001),("dent",7002),("normal",7003)]:
    r=e.predict(make_image(label,seed),machine="press-A")
    print(label,"=>",r["status"],r["label"],round(r["confidence"],3),r["adaptive_k"],[x["label"] for x in r["evidence"]])
