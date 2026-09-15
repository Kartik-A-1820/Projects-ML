# Week 30 — PromptShield-Local

A deterministic security gateway for tool-augmented AI agents. It treats model/tool outputs as untrusted data and enforces task-scoped policy at the tool-call boundary.

## Current relevance
Agentic systems increasingly connect LLMs to files, browsers, email, databases and MCP servers. Recent 2026 work on indirect prompt injection argues for deterministic tool-boundary enforcement rather than relying only on model alignment. The project implements that architectural idea without requiring a paid API or a large model.

## Capabilities
- default-deny tool allowlist
- argument schema restriction
- path-scope enforcement
- indirect prompt-injection pattern detection
- human approval for high-risk actions
- per-session tool budgets
- secret redaction in audit logs
- FastAPI policy gateway
- deterministic attack corpus and evaluation

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
uvicorn promptshield.api:app --app-dir src
```

## Hardware
CPU-only; negligible VRAM. A local SLM can be added behind the gateway, but security does not depend on it.

## Evaluation
The included corpus contains benign and adversarial cases. Extend it with MCP tool poisoning, skill-file injection, cross-origin instructions, parameter smuggling and multi-step exfiltration. Track attack-block rate, benign utility, false-positive rate and approval burden.

## Resume bullet
Built a deterministic security control plane for tool-augmented AI agents with default-deny authorization, indirect prompt-injection defenses, argument/path scoping, human approval gates, secret-safe audit logging, tool-call budgets and adversarial evaluation; designed production scaling for MCP/tool proxies, distributed policy enforcement, multi-tenant IAM, signed policy/model versions, SIEM telemetry and progressive rollout.
