import json,time
from pathlib import Path
class AuditLog:
    def __init__(self,path): self.path=Path(path)
    def write(self,event):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        row={"ts":time.time(),**event}
        with self.path.open("a",encoding="utf-8") as f:f.write(json.dumps(row,sort_keys=True)+"\n")
