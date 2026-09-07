from __future__ import annotations
from collections import defaultdict
import re

from .bm25 import BM25
from .models import VideoEvent, EvidenceHit

MODALITIES=("transcript","ocr","visual")

def infer_intent(query: str) -> str:
    q=query.lower()
    visual_words={"show","shown","look","visual","see","led","image","color","display"}
    text_words={"say","said","name","number","torque","code","text","written"}
    toks=set(re.findall(r"[a-z0-9]+",q))
    if toks & visual_words: return "visual_query"
    if toks & text_words: return "text_query"
    return "default"

class VideoRetriever:
    def __init__(self, events: list[VideoEvent]):
        self.events=events
        self.by_id={e.event_id:e for e in events}
        self.indexes={m:BM25([e.modality_text(m) for e in events]) for m in MODALITIES}

    def _weights(self, intent):
        table={
            "default":{"transcript":1.0,"ocr":0.8,"visual":0.8},
            "text_query":{"transcript":1.2,"ocr":1.0,"visual":0.6},
            "visual_query":{"transcript":0.7,"ocr":0.7,"visual":1.3},
        }
        return table[intent]

    def search(self, query: str, top_k=5, modality_top_k=6, rrf_k=60, expand_temporal=True):
        intent=infer_intent(query)
        weights=self._weights(intent)
        fused=defaultdict(float)
        reasons=defaultdict(list)

        for modality in MODALITIES:
            for rank, (_, idx) in enumerate(self.indexes[modality].search(query,modality_top_k),1):
                e=self.events[idx]
                fused[e.event_id] += weights[modality]/(rrf_k+rank)
                reasons[e.event_id].append(modality)

        ranked=sorted(fused,key=lambda eid:(-fused[eid],eid))
        if expand_temporal and ranked:
            seeds=ranked[:min(3,len(ranked))]
            for eid in seeds:
                event=self.by_id[eid]
                for linked in event.links:
                    if linked in self.by_id:
                        fused[linked] += 0.22/(rrf_k+1)
                        reasons[linked].append("temporal_link")
            ranked=sorted(fused,key=lambda eid:(-fused[eid],eid))

        hits=[]
        for eid in ranked[:top_k]:
            e=self.by_id[eid]
            hits.append(EvidenceHit(
                event_id=eid,start=e.start,end=e.end,score=float(fused[eid]),
                reasons=tuple(sorted(set(reasons[eid]))),
                transcript=e.transcript,ocr=e.ocr,visual=e.visual,
            ))
        return hits

def evidence_bundle(query: str, hits: list[EvidenceHit], budget_chars=3500) -> str:
    parts=[f"QUESTION: {query}"]
    used=len(parts[0])
    for h in hits:
        block=(
            f"\n[{h.event_id} {h.start:.0f}-{h.end:.0f}s | {','.join(h.reasons)}]\n"
            f"TRANSCRIPT: {h.transcript}\nOCR: {h.ocr}\nVISUAL: {h.visual}"
        )
        if used+len(block)>budget_chars: break
        parts.append(block); used+=len(block)
    return "\n".join(parts)
