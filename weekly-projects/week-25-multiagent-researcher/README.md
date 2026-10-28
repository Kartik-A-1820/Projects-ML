# Week 25 — MultiAgent-Researcher
A bounded, evidence-first multi-agent research orchestration benchmark. Instead of pretending that more agents always improve quality, it measures coordination overhead, communication density, evidence coverage, conflict resolution, and final-answer quality under explicit message/tool budgets.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_benchmark.py
python -m pytest -q
```
