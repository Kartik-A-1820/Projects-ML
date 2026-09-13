from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from PIL import Image
from .features import embed_image,cosine

@dataclass(frozen=True)
class Exemplar:
    item_id:str
    path:str
    label:str
    machine:str
    illumination:str
    embedding:list[float]

class ExemplarIndex:
    def __init__(self,items):
        self.items=list(items)
    @classmethod
    def build(cls,manifest_path):
        rows=json.loads(Path(manifest_path).read_text())
        items=[]
        for r in rows:
            emb=embed_image(Image.open(r["path"]))
            items.append(Exemplar(
                r["id"],r["path"],r["label"],r["machine"],r["illumination"],emb.tolist()
            ))
        return cls(items)
    def search(self,image,k=7,machine=None,metadata_weight=.12):
        q=embed_image(image); rows=[]
        for x in self.items:
            s=cosine(q,x.embedding)
            if machine and x.machine==machine:s+=metadata_weight
            rows.append((s,x))
        rows.sort(key=lambda z:(-z[0],z[1].item_id))
        return rows[:k]
