# Week 25 — MultiAgent-Researcher

A bounded, evidence-first multi-agent research orchestration benchmark. Instead of pretending that more agents always improve quality, it measures coordination overhead, communication density, evidence coverage, conflict resolution, and final-answer quality under explicit message/tool budgets.

## Why this is current
ACL 2026 SILO-BENCH reports a communication-reasoning gap: agents may communicate heavily without converting that interaction into better distributed computation. 2026 enterprise benchmarks also emphasize role specialization, permissions and approval constraints.

## Capabilities
- role-specialized research agents
- isolated evidence shards
- orchestrator-worker pattern
- shared blackboard
- critic/verifier stage
- message and token-proxy budgets
- evidence provenance
- conflict detection
- coordination-density metrics
- single-agent vs multi-agent benchmark
- deterministic offline fixture

## Hardware
CPU-only deterministic implementation; no model downloads required.

## Run
```bash
pip install -r requirements.txt
python run_benchmark.py
pytest -q
```

## Resume bullet
Built a bounded multi-agent research orchestration benchmark comparing single-agent and role-specialized collaboration under information silos, with provenance-preserving evidence exchange, critic verification, message budgets and coordination-cost metrics; designed production scaling for durable agent state, sandboxed tools, role/permission isolation, observability, multi-tenant workspaces, failure recovery and policy-controlled rollout.
