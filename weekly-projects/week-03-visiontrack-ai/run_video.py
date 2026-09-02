import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from visiontrack.core import IoUTracker, LineCrossingCounter
from visiontrack.detector import UltralyticsDetector

def main():
    import cv2
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--model',default='yolo26n.pt'); p.add_argument('--output',default='artifacts/events.jsonl'); a=p.parse_args()
    detector=UltralyticsDetector(a.model); tracker=IoUTracker(); counter=LineCrossingCounter((0,300,1280,300)); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(a.source); idx=0
    with out.open('w',encoding='utf-8') as f:
        while True:
            ok,frame=cap.read()
            if not ok: break
            tracks=tracker.update(detector.predict(frame)); events=counter.update(tracks,idx)
            for e in events: f.write(json.dumps(e.__dict__)+'\n')
            idx+=1
    cap.release(); print('frames=',idx); print('counts=',counter.counts)
if __name__=='__main__': main()
