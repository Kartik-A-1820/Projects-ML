# Week 27 — MLOps-ModelRegistry
A local governed model registry that makes models first-class lifecycle artifacts: immutable versions, checksums, signatures, lineage, aliases, promotion gates and rollback.
The default implementation is dependency-light and uses SQLite + local object storage. It also documents a production MLflow 3 integration path, where model registry concepts include lineage, versioning, aliases and tags.
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
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python -m pytest -q
```
