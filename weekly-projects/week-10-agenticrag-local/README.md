# Week 10 — AgenticRAG-Local
A bounded, corrective RAG control loop that decides whether initial retrieval is sufficient,
reformulates weak queries, retries retrieval under a strict budget, and abstains when evidence remains insufficient.
This is deliberately **not** an unconstrained autonomous agent. Reliability, observability and finite budgets are first-class.
## Capabilities
- BM25 local retrieval
- retrieval evidence grader
- deterministic query reformulation
- bounded corrective loop
- explicit stop reasons
- citation/evidence return
- abstention on weak evidence
- offline evaluation
- optional local LLM adapter point
- proposed deployment architecture notes
## Hardware
Runs fully on Ryzen 7 / 16 GB RAM. Optional local generation can use a small quantized model,
but retrieval control and tests require no model downloads.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
