# Week 27 — MLOps-ModelRegistry

A local governed model registry that makes models first-class lifecycle artifacts: immutable versions, checksums, signatures, lineage, aliases, promotion gates and rollback.

The default implementation is dependency-light and uses SQLite + local object storage. It also documents a production MLflow 3 integration path, where model registry concepts include lineage, versioning, aliases and tags.

## Why this is current

Modern MLOps registries are no longer just folders of `.pkl` files. Current MLflow registry guidance treats models as versioned lifecycle objects with lineage, aliases such as `champion`, tags, signatures and controlled promotion. This project implements those lifecycle principles locally without requiring a remote platform.

## Capabilities

- immutable model versions
- SHA-256 artifact integrity
- model signature/schema
- training-data snapshot hash
- code revision and run lineage
- evaluation metrics/tags
- validation gates
- aliases: candidate/champion/rollback
- compatibility checks
- atomic alias promotion
- rollback
- audit event history
- local SQLite registry
- sklearn demonstration
- optional MLflow 3 adapter architecture

## Hardware

CPU-only. Designed for Ryzen 7 / 16 GB RAM and free/open-source dependencies.

## Run

```bash
pip install -r requirements.txt
python run_demo.py
pytest -q
```

## Resume bullet

Built a governed MLOps model registry with immutable artifact versions, checksum verification, training/data/code lineage, input signatures, validation gates, champion/candidate aliases, atomic promotion and rollback; designed production scaling for MLflow-compatible registries, object storage, approval workflows, multi-environment IAM, canary deployment, auditability and disaster recovery.
