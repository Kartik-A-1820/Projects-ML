from __future__ import annotations
import json, re

def canonical(text:str):
    t=text.strip()
    try:
        obj=json.loads(t)
        return json.dumps(obj,sort_keys=True,separators=(',',':'))
    except Exception:
        return re.sub(r'\s+',' ',t).strip().lower()

def exact_or_structured_match(expected:str,predicted:str)->float:
    return 1.0 if canonical(expected)==canonical(predicted) else 0.0

def evaluate_pairs(rows:list[dict])->dict:
    scores=[exact_or_structured_match(r['expected'],r['predicted']) for r in rows]
    return {'count':len(scores),'accuracy':sum(scores)/len(scores) if scores else 0.0}
