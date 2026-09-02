from __future__ import annotations
import re, numpy as np

def slice_masks(texts):
    return {
        'short': np.array([len(t.split())<=8 for t in texts]),
        'long': np.array([len(t.split())>=25 for t in texts]),
        'has_url': np.array([bool(re.search(r'https?://|www\.',t)) for t in texts]),
        'has_emoji_like': np.array([any(ord(ch)>10000 for ch in t) for t in texts]),
        'has_negation': np.array([bool(re.search(r"\b(no|not|never|n't)\b",t.lower())) for t in texts]),
    }

def accuracy_by_slice(preds,labels,texts):
    preds=np.asarray(preds); labels=np.asarray(labels); out={}
    for name,mask in slice_masks(texts).items(): out[name]=None if not mask.any() else float((preds[mask]==labels[mask]).mean())
    return out
