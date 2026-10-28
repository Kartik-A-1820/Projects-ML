# Week 14 — CodePilot-Mini
A local repository-aware coding-assistant core focused on the part modern coding agents often get wrong: **finding the right code, recovering repository context, planning a minimal patch, and validating it**.
The project is deliberately more than "prompt an LLM with code." It implements repository indexing, AST symbol extraction, issue-to-file retrieval, context budgeting, change-risk analysis and safe patch verification. An optional local coder model can be plugged in later.
## Capabilities
- repository scanner with ignore rules
- Python AST symbol index
- lexical file/chunk retrieval
- issue keyword + symbol-aware ranking
- context budget selection
- requirement/spec extraction
- dependency/import impact map
- change-risk score
- patch-plan generation
- unified diff application guard
- test-command execution with timeout
- retrieval Recall@K evaluation on a sample repository
- optional local Qwen coder model adapter point
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
Default workflow is CPU-only. A 0.5B–1.5B quantized coder can optionally be used for patch generation; retrieval, planning and validation remain independent.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
