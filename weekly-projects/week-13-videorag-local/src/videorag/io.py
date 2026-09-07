import json
from pathlib import Path
from .models import VideoEvent

def load_events(path):
    rows=json.loads(Path(path).read_text(encoding="utf-8"))
    return [VideoEvent(**r) for r in rows]
