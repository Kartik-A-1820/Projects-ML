import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from visionrag.synthetic import generate_dataset

rows=generate_dataset()
Path("data/manifest.json").write_text(json.dumps(rows,indent=2))
print("generated",len(rows),"exemplars")
