# AI/ML engineering and data-science labs

This repository contains two independent project series and earlier standalone
notebooks. Each project has its own dependencies and validation scope; there is
no single root environment that runs every lab.

| Series | Start here | Purpose |
| --- | --- | --- |
| AI/ML engineering labs | [weekly-projects](weekly-projects/) | Runnable systems, tests, and architecture discussions |
| Data-science labs | [data-science-labs](data-science-labs/) | Statistical/modeling experiments and dataset protocols |
| Earlier experiments | Root-level notebooks | Learning history; maturity varies |

## Current entry points

- [ContractTrace — Week 37](weekly-projects/week-37-contracttrace-agent-transactions/): transactional agent tool contracts and state verification.
- [ContinualLearn-NLP — Week 31](weekly-projects/week-31-continuallearn-nlp/): replay and forgetting experiments; the local SLM extension is separate from the CPU control-plane implementation.
- [Long-tail recommendation — DS Week 05](data-science-labs/ds-week-05-longtail-sequential-recommendation/): reconstructed runnable popularity/Markov/BPR comparison, ranking tests, and a synthetic smoke report.
- [Phishing domain shift — DS Week 07](data-science-labs/ds-week-07-phishing-domain-generalization/): documented synthetic verification; real-data status is recorded in its README.

## Run one lab

Clone the repository, choose a lab above, and follow its README from that lab's directory. Use a separate environment for each project; similarly named `src` modules and differing dependencies are not designed to share one root environment.

Start with a synthetic or deterministic smoke path where offered. Model downloads, real datasets, external services, and production design proposals are separate from the default implementation. See [CONTRIBUTING.md](CONTRIBUTING.md) for environment activation, validation, and contribution steps.

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

## Contribute

Useful contributions include a minimal bug reproduction, a missing test, a documented real-data evaluation, setup corrections, or a measured baseline comparison. Open an issue before a large redesign or a missing-week reconstruction.

The per-lab READMEs describe methods and execution; architecture documents can include proposed deployment extensions. Evaluate implemented behavior separately from those proposals. No standalone repository LICENSE is included, so clarify intended reuse terms and check each dataset/model's terms.
