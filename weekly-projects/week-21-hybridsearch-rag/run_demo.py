import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/"src"))
from hybridrag.core import HybridEngine
e=HybridEngine()
for q in ["E104","how can search find similar meaning with different wording","AC-17 privileged review frequency"]:
 r=e.search(q);print(q,"=>",r["family"],r["candidate_budget"],[x["id"] for x in r["hits"]])
