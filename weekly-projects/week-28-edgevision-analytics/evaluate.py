import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from edgevision.synthetic import make_stream
from edgevision.pipeline import EdgeVisionPipeline
from edgevision.metrics import classification_metrics,latency_metrics

stream=make_stream(n=50,defect_start=20,defect_end=29,seed=7)
p=EdgeVisionPipeline(frame_stride=2)
truth=[];pred=[];lat=[];processed=0
for row in stream:
    r=p.process(row['frame_id'],row['image'])
    if r['status']=='processed':
        processed+=1;truth.append(row['defect']);pred.append(bool(r['detections']));lat.append(r['latency_ms'])
print({'processed_frames':processed,'total_frames':len(stream),'classification':classification_metrics(truth,pred),'latency':latency_metrics(lat)})
