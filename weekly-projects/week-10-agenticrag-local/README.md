# Week 10 — AgenticRAG-Local (2026 Rebuild)

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
- production scaling architecture

## Hardware
Runs fully on Ryzen 7 / 16 GB RAM. Optional local generation can use a small quantized model,
but retrieval control and tests require no model downloads.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Resume bullet
Built a bounded corrective Agentic RAG control plane that grades retrieval evidence, reformulates weak queries, retries within explicit cost/latency budgets and abstains on insufficient context; added deterministic evaluation, traceable stop reasons and a production architecture for stateful orchestration, retrieval tools, queue isolation, model routing, observability and policy-enforced tool execution.
