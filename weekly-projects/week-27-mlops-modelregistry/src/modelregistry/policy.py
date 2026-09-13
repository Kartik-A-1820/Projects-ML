from __future__ import annotations

def validate_candidate(model_meta,policy):
    reasons=[]
    if policy.get("require_signature") and not model_meta.get("signature"):reasons.append("missing_signature")
    if policy.get("require_data_hash") and not model_meta.get("data_hash"):reasons.append("missing_data_hash")
    for k,v in policy.get("required_metrics",{}).items():
        if float(model_meta.get("metrics",{}).get(k,float("-inf")))<float(v):
            reasons.append(f"metric:{k}")
    for k,v in policy.get("required_tags",{}).items():
        if model_meta.get("tags",{}).get(k)!=v:reasons.append(f"tag:{k}")
    return {"passed":not reasons,"reasons":reasons}

def signatures_compatible(champion,candidate):
    a=champion.get("signature",{});b=candidate.get("signature",{})
    return a.get("inputs")==b.get("inputs") and a.get("outputs")==b.get("outputs")
