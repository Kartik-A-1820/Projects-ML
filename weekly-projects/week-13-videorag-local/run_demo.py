import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from videorag.io import load_events
from videorag.retrieval import VideoRetriever,evidence_bundle

r=VideoRetriever(load_events("data/events.json"))
q="what visual evidence shows the fault was cleared"
hits=r.search(q,5)
print([(h.event_id,round(h.score,5),h.reasons) for h in hits])
print(evidence_bundle(q,hits,1200))
