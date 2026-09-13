from __future__ import annotations
from .policy import validate_candidate,signatures_compatible

def promote(registry,name,candidate_version,policy):
    cand=registry.get(name,candidate_version)
    if not registry.verify_artifact(name,candidate_version):
        return {"promoted":False,"reasons":["artifact_checksum_failed"]}
    v=validate_candidate(cand,policy)
    if not v["passed"]:return {"promoted":False,"reasons":v["reasons"]}
    try:
        champ=registry.resolve_alias(name,"champion")
        if not signatures_compatible(champ,cand):
            return {"promoted":False,"reasons":["signature_incompatible"]}
        registry.set_alias(name,"rollback",champ["version"])
    except KeyError:
        pass
    registry.set_alias(name,"champion",candidate_version)
    registry.set_alias(name,"candidate",candidate_version)
    return {"promoted":True,"version":candidate_version,"reasons":[]}

def rollback(registry,name):
    old=registry.resolve_alias(name,"rollback")
    current=registry.resolve_alias(name,"champion")
    registry.set_alias(name,"champion",old["version"])
    registry.set_alias(name,"rollback",current["version"])
    return {"champion":old["version"],"rollback":current["version"]}
