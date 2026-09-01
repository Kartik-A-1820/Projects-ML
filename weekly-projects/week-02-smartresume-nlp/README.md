# Week 02 — SmartResume-NLP (2026 Rebuild)

A local-first, explainable resume-to-job matching and skill-gap intelligence system designed as a Senior/Staff-adjacent NLP portfolio project.

## What it demonstrates
- leakage-aware resume/job text normalization
- transparent TF-IDF + cosine baseline
- optional sentence-transformer semantic scoring
- skill ontology normalization
- evidence-backed skill-gap extraction
- configurable score fusion
- fairness-oriented separation of identity/PII from ranking features
- deterministic tests and production scaling design

## Local hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.

## Install
```bash
python -m venv .venv
pip install -r requirements.txt
```

## Run
```bash
python run.py --resume data/sample_resume.txt --job data/sample_job.txt
```

## Tests
```bash
pytest -q
```

## Resume bullet
Built an explainable local NLP matching engine for resume-to-role ranking and skill-gap analysis, combining lexical relevance, ontology-normalized skills, PII-safe feature separation and configurable score fusion; designed a production architecture for multi-tenant ingestion, model/version lineage, fairness monitoring, vector retrieval and auditable decision support.
