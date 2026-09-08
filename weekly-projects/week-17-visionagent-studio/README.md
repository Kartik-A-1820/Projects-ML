# Week 17 — VisionAgent-Studio

A bounded multimodal visual-reasoning agent that selects deterministic image tools, stores visual observations in memory, revisits earlier evidence, and stops under explicit budgets.

## Why this matters
2026 multimodal-agent research increasingly combines planning, external visual tools, memory and self-critique rather than relying on one monolithic VLM pass.

## Capabilities
- dispatcher/planner
- visual tool registry
- image-memory abstraction
- tool-call budget
- iterative observation and critique
- deterministic synthetic image tools
- structured trace
- answer confidence + abstention
- tests and FastAPI endpoint
- production design for sandboxed visual tools and GPU model routing

## Hardware
CPU-first demo. Optional local VLM can be attached later. Designed for Ryzen 7 / 16 GB RAM / GTX 1650 Ti 4 GB.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Resume bullet
Built a bounded multimodal vision-agent platform with tool selection, episodic visual memory, iterative evidence collection, self-critique and explicit termination budgets; designed production scaling for sandboxed CV tools, GPU/VLM routing, image-memory storage, observability, multi-tenant isolation, policy-controlled tool execution and safe rollback.
