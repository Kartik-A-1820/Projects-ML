# Week 14 — CodePilot-Mini (2026 Rebuild)

A local repository-aware coding-assistant core focused on the part modern coding agents often get wrong: **finding the right code, recovering repository context, planning a minimal patch, and validating it**.

The project is deliberately more than "prompt an LLM with code." It implements repository indexing, AST symbol extraction, issue-to-file retrieval, context budgeting, change-risk analysis and safe patch verification. An optional local coder model can be plugged in later.

## 2026 design direction

Recent coding-agent research isolates repository exploration/context retrieval as a major bottleneck:
- Agent Retrieval Bench evaluates upstream file retrieval separately from patch generation.
- SWE-Explore benchmarks ranked code-region exploration under a fixed context budget.
- CodeGrep (August 2026) reports fewer rounds/tokens by specializing repository retrieval.
- SWE-RPG (August 2026) shows implicit requirement recovery remains a major failure source.

This project adapts those lessons into a constrained, auditable local coding-assistant pipeline.

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

## Run

```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Resume bullet

Built a repository-aware coding-agent core that indexes AST symbols and file context, localizes issue-relevant code under a strict context budget, generates traceable change plans, scores change risk and validates patches through guarded diff application and tests; designed production scaling around sandboxed worktrees, retrieval-quality gates, model routing, secure tool execution, trajectory observability and repository/version lineage.
