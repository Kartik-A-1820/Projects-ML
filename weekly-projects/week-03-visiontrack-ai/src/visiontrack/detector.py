from .core import Detection

class UltralyticsDetector:
    def __init__(self, model_name="yolo26n.pt", confidence=0.25, device=None):
        from ultralytics import YOLO
        self.model=YOLO(model_name); self.confidence=confidence; self.device=device
    def predict(self, frame):
        out=[]
        for result in self.model.predict(frame, conf=self.confidence, device=self.device, verbose=False):
            if result.boxes is None: continue
            for box in result.boxes:
                cls=int(box.cls[0]); out.append(Detection(tuple(float(v) for v in box.xyxy[0].tolist()), float(box.conf[0]), cls, str(result.names.get(cls,cls))))
        return out
