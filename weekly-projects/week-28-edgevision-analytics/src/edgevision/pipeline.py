from __future__ import annotations
import time
from .quality import assess_quality
from .detector import detect
from .events import EventAggregator

class EdgeVisionPipeline:
    def __init__(self,frame_stride=2):
        self.frame_stride=frame_stride
        self.events=EventAggregator()

    def process(self,frame_id,image):
        start=time.perf_counter()
        if frame_id % self.frame_stride != 0:
            return {'frame_id':frame_id,'status':'skipped','latency_ms':0.0,'event_active':self.events.active}
        quality=assess_quality(image)
        if not quality['accepted']:
            latency=(time.perf_counter()-start)*1000
            return {'frame_id':frame_id,'status':'quality_reject','quality':quality,'detections':[],'escalate':True,'latency_ms':latency,'event_active':self.events.update(False)}
        detections=detect(image)
        top_conf=max((d['confidence'] for d in detections),default=0.0)
        event=self.events.update(bool(detections))
        escalate=bool(detections) and 0.45<=top_conf<=0.65
        latency=(time.perf_counter()-start)*1000
        return {'frame_id':frame_id,'status':'processed','quality':quality,'detections':detections,'top_confidence':top_conf,'escalate':escalate,'event_active':event,'latency_ms':latency}
