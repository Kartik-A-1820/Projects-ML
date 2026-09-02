import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from visiontrack.core import Detection, IoUTracker, LineCrossingCounter
tracker=IoUTracker(iou_threshold=0.05,max_missed=2)
counter=LineCrossingCounter((0,50,100,50))
frames=[[Detection((10,20,30,40),.9,0,'car')],[Detection((10,35,30,55),.9,0,'car')],[Detection((10,45,30,65),.9,0,'car')]]
for i,dets in enumerate(frames):
    tracks=tracker.update(dets); events=counter.update(tracks,i); print(i,[(t.track_id,t.center) for t in tracks],[e.__dict__ for e in events])
print('counts=',counter.counts)
