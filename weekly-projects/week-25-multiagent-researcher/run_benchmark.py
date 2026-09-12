import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from maresearch.orchestrator import MultiAgentResearcher
from maresearch.baseline import SingleAgentResearcher
from maresearch.metrics import evidence_coverage,efficiency_score

ev=json.loads(Path("data/evidence.json").read_text());tasks=json.loads(Path("data/tasks.json").read_text())
idx={e["id"]:e for shard in ev.values() for e in shard};systems={"single":SingleAgentResearcher(ev),"multi":MultiAgentResearcher(ev)}
for t in tasks:
    print("\nTASK",t["id"],t["question"])
    for name,s in systems.items():
        r=s.run(t["question"]);cov=evidence_coverage(r["evidence_ids"],idx,t["required_topics"])
        print(name,{"coverage":cov,"messages":r["messages"],"efficiency":efficiency_score(cov,r["messages"]),"evidence":r["evidence_ids"]})
