from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Detection:
    xyxy: tuple[float, float, float, float]
    confidence: float
    class_id: int
    label: str = "object"

@dataclass
class Track:
    track_id: int
    xyxy: tuple[float, float, float, float]
    class_id: int
    label: str
    confidence: float
    hits: int = 1
    missed: int = 0
    age: int = 1
    history: list[tuple[float, float]] = field(default_factory=list)

    @property
    def center(self):
        x1, y1, x2, y2 = self.xyxy
        return ((x1+x2)/2.0, (y1+y2)/2.0)

def iou(a, b):
    ax1, ay1, ax2, ay2 = a; bx1, by1, bx2, by2 = b
    ix1, iy1, ix2, iy2 = max(ax1,bx1), max(ay1,by1), min(ax2,bx2), min(ay2,by2)
    iw, ih = max(0.0, ix2-ix1), max(0.0, iy2-iy1)
    inter = iw*ih
    aa = max(0.0, ax2-ax1)*max(0.0, ay2-ay1)
    ab = max(0.0, bx2-bx1)*max(0.0, by2-by1)
    union = aa+ab-inter
    return 0.0 if union <= 0 else inter/union

class IoUTracker:
    def __init__(self, iou_threshold=0.2, max_missed=8, history_size=30):
        self.iou_threshold=iou_threshold; self.max_missed=max_missed; self.history_size=history_size
        self.tracks={}; self._next_id=1

    def update(self, detections):
        tids=list(self.tracks)
        candidates=[]
        for ti,tid in enumerate(tids):
            tr=self.tracks[tid]
            for di,det in enumerate(detections):
                if tr.class_id != det.class_id: continue
                s=iou(tr.xyxy, det.xyxy)
                if s >= self.iou_threshold: candidates.append((s,ti,di))
        candidates.sort(reverse=True)
        used_t=set(); used_d=set()
        for _,ti,di in candidates:
            if ti in used_t or di in used_d: continue
            tr=self.tracks[tids[ti]]; det=detections[di]
            tr.xyxy=det.xyxy; tr.confidence=det.confidence; tr.label=det.label
            tr.hits+=1; tr.missed=0; tr.age+=1; tr.history.append(tr.center)
            tr.history=tr.history[-self.history_size:]
            used_t.add(ti); used_d.add(di)
        for ti,tid in enumerate(tids):
            if ti not in used_t:
                self.tracks[tid].missed+=1; self.tracks[tid].age+=1
        for di,det in enumerate(detections):
            if di in used_d: continue
            tr=Track(self._next_id, det.xyxy, det.class_id, det.label, det.confidence)
            tr.history.append(tr.center); self.tracks[self._next_id]=tr; self._next_id+=1
        for tid in [tid for tid,tr in self.tracks.items() if tr.missed > self.max_missed]: del self.tracks[tid]
        return list(self.tracks.values())

def side_of_line(point, line):
    x,y=point; x1,y1,x2,y2=line
    return (x2-x1)*(y-y1)-(y2-y1)*(x-x1)

@dataclass
class CrossingEvent:
    track_id:int; label:str; direction:str; frame_index:int

class LineCrossingCounter:
    def __init__(self, line):
        self.line=line; self.last_side={}; self.counts={}
    def update(self, tracks, frame_index):
        events=[]
        for tr in tracks:
            cur=side_of_line(tr.center,self.line); prev=self.last_side.get(tr.track_id)
            if prev is not None and prev != 0 and cur != 0 and (prev>0)!=(cur>0):
                direction="A_TO_B" if prev<cur else "B_TO_A"
                key=f"{tr.label}:{direction}"; self.counts[key]=self.counts.get(key,0)+1
                events.append(CrossingEvent(tr.track_id,tr.label,direction,frame_index))
            self.last_side[tr.track_id]=cur
        return events
