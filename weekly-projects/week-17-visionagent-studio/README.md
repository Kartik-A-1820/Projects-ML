# Week 17 — VisionAgent-Studio
A bounded multimodal visual-reasoning agent that selects deterministic image tools, stores visual observations in memory, revisits earlier evidence, and stops under explicit budgets.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
