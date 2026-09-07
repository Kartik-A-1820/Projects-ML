from __future__ import annotations
import re

ACTION_WORDS={"fix","add","change","update","remove","clamp","prevent","ensure","cover","test"}

def extract_requirements(issue):
    clean=" ".join(issue.strip().split())
    pieces=[x.strip() for x in re.split(r"[.;]|\band\b",clean,flags=re.I) if x.strip()]
    requirements=[]
    for p in pieces:
        if any(w in p.lower().split() for w in ACTION_WORDS) or len(pieces)==1:
            requirements.append(p)
    return requirements or [clean]

def risk_score(files):
    score=0
    for f in files:
        if f.path.startswith("tests/"): score+=0.3
        else: score+=1.0
        if "service" in f.path or "api" in f.path: score+=0.5
        if len(f.imports)>5: score+=0.3
    return round(score,2)

def build_plan(issue,hits):
    files=[f for _,f in hits]
    reqs=extract_requirements(issue)
    steps=[]
    for f in files:
        reason="test/regression coverage" if f.path.startswith("tests/") else "implementation or dependency context"
        steps.append({"file":f.path,"reason":reason,"symbols":list(f.symbols)})
    return {"requirements":reqs,"candidate_files":steps,"risk_score":risk_score(files)}
