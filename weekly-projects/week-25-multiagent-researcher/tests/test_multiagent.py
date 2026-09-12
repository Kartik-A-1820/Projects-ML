import json
from pathlib import Path
from maresearch.orchestrator import MultiAgentResearcher
from maresearch.baseline import SingleAgentResearcher
from maresearch.metrics import evidence_coverage
def evidence():return json.loads(Path("data/evidence.json").read_text())
def test_multi_agent_respects_budget():
    r=MultiAgentResearcher(evidence(),max_messages=3).run("enterprise model risk cost");assert r["messages"]<=3
def test_provenance_present():
    r=MultiAgentResearcher(evidence()).run("PEFT quantization risk");assert r["evidence_ids"]
def test_coverage_metric():
    ev=evidence();idx={e["id"]:e for s in ev.values() for e in s};assert evidence_coverage(["m1","s1","r1"],idx,["economics","systems","risk"])==1.0
def test_single_agent_has_less_or_equal_evidence_budget():
    assert len(SingleAgentResearcher(evidence(),2).run("x")["evidence_ids"])<=2
