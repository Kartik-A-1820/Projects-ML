# Week 30 — PromptShield-Local
A deterministic security gateway for tool-augmented AI agents. It treats model/tool outputs as untrusted data and enforces task-scoped policy at the tool-call boundary.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
uvicorn promptshield.api:app --app-dir src
```
## Hardware
CPU-only; negligible VRAM. A local SLM can be added behind the gateway, but security does not depend on it.
## Evaluation
The included corpus contains benign and adversarial cases. Extend it with MCP tool poisoning, skill-file injection, cross-origin instructions, parameter smuggling and multi-step exfiltration. Track attack-block rate, benign utility, false-positive rate and approval burden.
