# AI/ML engineering and data-science portfolio

This repository contains two independent project series and earlier standalone
notebooks. Each project has its own dependencies and validation scope; there is
no single root environment that runs every lab.

| Series | Start here | Purpose |
| --- | --- | --- |
| Tuesday AI/ML engineering | [weekly-projects](weekly-projects/) | Runnable systems, tests, and architecture discussions |
| Saturday data science | [data-science-labs](data-science-labs/) | Statistical/modeling experiments and dataset protocols |
| Earlier experiments | Root-level notebooks | Learning history; maturity varies |

## Current entry points

- [ContractTrace — Week 37](weekly-projects/week-37-contracttrace-agent-transactions/): transactional agent tool contracts and state verification.
- [ContinualLearn-NLP — Week 31](weekly-projects/week-31-continuallearn-nlp/): replay and forgetting experiments; the local SLM extension is separate from the CPU control-plane implementation.
- [Long-tail recommendation — DS Week 05](data-science-labs/ds-week-05-longtail-sequential-recommendation/): reconstructed runnable popularity/Markov/BPR comparison, ranking tests, and a synthetic smoke report.
- [Phishing domain shift — DS Week 07](data-science-labs/ds-week-07-phishing-domain-generalization/): documented synthetic verification; real-data status is recorded in its README.

## Inventory versus verified behavior

[PORTFOLIO_STATUS.md](PORTFOLIO_STATUS.md) records the observed repository coverage
and unresolved migration gaps. The migration ledger's historical checks do not
mean every runtime, model download, real dataset, or external destination was
retested during maintenance.

```bash
python scripts/audit_portfolio.py
# Write a machine-readable inventory:
python scripts/audit_portfolio.py --output portfolio_inventory.json
```

The audit checks required files and missing week folders. It does not execute
projects or certify correctness. Use the README and tests inside a selected
project. DS and AI/ML week numbers are separate; do not fill a numbering gap by
silently inventing or renaming a project.
