# Week 02 — SmartResume-NLP
A local-first, explainable resume-to-job matching and skill-gap intelligence system for comparing lexical and semantic matching.
## What it demonstrates
- leakage-aware resume/job text normalization
- transparent TF-IDF + cosine baseline
- optional sentence-transformer semantic scoring
- skill ontology normalization
- evidence-backed skill-gap extraction
- configurable score fusion
- fairness-oriented separation of identity/PII from ranking features
- deterministic tests and deployment design notes
## Local hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Install
```bash
python -m pip install -r requirements.txt
```
## Run
```bash
python run.py --resume data/sample_resume.txt --job data/sample_job.txt
```
## Tests
```bash
python -m pytest -q
```
