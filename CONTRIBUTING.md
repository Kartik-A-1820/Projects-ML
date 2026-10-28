# Contributing to the AI/ML labs

Each lab is an independent experiment. Choose one folder and one concrete problem; do not install every requirements file into a shared root environment.

## Setup

Clone the repository, then change into a lab directory. Use its stated Python version; Python 3.11 is the starting point for the current examples.

```bash
git clone https://github.com/Kartik-A-1820/Projects-ML.git
cd Projects-ML/weekly-projects/week-01-localdoc-rag
python -m venv .venv
```

Activate the environment before installing dependencies:

| Shell | Command |
| --- | --- |
| Linux/macOS | `source .venv/bin/activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |

```bash
python -m pip install -r requirements.txt
```

Follow that lab's run/test commands from the same directory. Jupyter and optional models may need separate packages or downloads; inspect its requirements and README first. A Bash `PYTHONPATH=src ...` prefix corresponds to setting `$env:PYTHONPATH='src'` before the command in PowerShell.

## Validate the relevant change

- Add a focused regression test for behavior changes and run the affected lab's tests.
- A notebook change should be checked from a fresh kernel, with executed cells and data mode recorded.
- Documentation changes should check commands, file paths, and correspondence with the implementation.
- API changes should use temporary storage and synthetic/public fixtures, not live credentials or private documents.

The root inventory can be checked with `python scripts/audit_portfolio.py` from the repository root. It checks file presence, not runtime correctness. There is no single root test command for every lab.

## Report evidence precisely

Record the commit, environment, dataset source/version, split, seed, hardware, baseline, metric definition, commands, and raw results. Label synthetic smoke tests, model downloads, real-data runs, and external integrations separately.

Do not promote a proposed architecture into a capability claim. Preserve historical metrics with their provenance. A successful smoke test is not evidence of production reliability, security, fairness, or real-data generalization.

## Pull requests

Fork, create a branch, and explain the problem, change, validation, and remaining limits. Discuss larger redesigns and missing-week recovery in an issue first. Do not create duplicate weeks or relabel an unrelated lab to fill an inventory gap.

Do not commit credentials, environments, downloaded datasets, private documents, or large model artifacts. Use small redistributable fixtures and state their source and terms.

No standalone LICENSE file is included. Clarify repository reuse terms with the maintainer; third-party model and dataset terms remain separate.
