import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from edgevision.synthetic import make_stream
from edgevision.pipeline import EdgeVisionPipeline

p=EdgeVisionPipeline(frame_stride=2)
for row in make_stream(n=12,defect_start=4,defect_end=8):
    r=p.process(row['frame_id'],row['image'])
    print(row['frame_id'],r['status'],len(r.get('detections',[])),r['event_active'],r.get('escalate',False))
