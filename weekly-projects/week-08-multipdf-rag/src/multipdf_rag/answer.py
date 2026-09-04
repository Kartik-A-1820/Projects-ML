from __future__ import annotations
import re
from .schema import Hit

def sentences(text): return [s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if s.strip()]
def evidence_answer(query:str,hits:list[Hit],max_sentences=3)->dict:
    q=set(re.findall(r'[a-z0-9-]+',query.lower())); ranked=[]
    for h in hits:
        for s in sentences(h.chunk.text):
            overlap=len(q & set(re.findall(r'[a-z0-9-]+',s.lower())))
            ranked.append((overlap,h.chunk.chunk_id,h.chunk.source,h.chunk.page,s))
    ranked.sort(key=lambda x:(-x[0],x[1])); chosen=[x for x in ranked if x[0]>0][:max_sentences]
    if not chosen: return {'answer':'Insufficient evidence in retrieved documents.','citations':[],'grounded':False}
    return {'answer':' '.join(x[4] for x in chosen),'citations':[{'chunk_id':x[1],'source':x[2],'page':x[3]} for x in chosen],'grounded':True}
