import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from visionsearch.core import DeterministicTextImageEncoder, VectorIndex

rows=json.loads(Path("data/catalog.json").read_text())
enc=DeterministicTextImageEncoder()
idx=VectorIndex()
for r in rows:
    idx.add(r["id"], enc.encode_image_descriptor(r["caption"]), r)
for score, item_id, meta in idx.search(enc.encode_text("red truck vehicle"), top_k=3):
    print(item_id, round(score,4), meta["caption"])
