# Week 31 — ContinualLearn-NLP

A resource-efficient continual-learning laboratory for NLP systems that must learn sequential domains without catastrophically forgetting earlier capabilities.

## Industry problem
Production language systems change continuously: support intents evolve, product taxonomies expand, fraud/security language shifts, and enterprise policies change. Re-training from scratch is expensive; naive sequential fine-tuning can erase prior capabilities.

## Current research connection
ACL 2026 FOREVER schedules replay using model-centric learning progress rather than fixed steps. ICLR 2026 Meta-UCF and EACL 2026 ELLA/SAFM explore memory-constant or parameter-efficient continual adaptation. This project implements a constrained-hardware engineering analogue: forgetting-aware replay, stability regularization, sequential evaluation, and a clean adapter point for a local PEFT/LoRA backend.

## Local implementation
- deterministic hashing text representation;
- expandable softmax classifier;
- stability regularization against the previous parameter anchor;
- bounded replay memory;
- forgetting-priority replay;
- sequential task stream;
- per-task accuracy, average accuracy and forgetting metrics;
- replay vs no-replay benchmark.

This dependency-light core runs on CPU and verifies the continual-learning control plane without model downloads. For the full experiment, replace the encoder/classifier with a 0.5B–1.5B local SLM plus LoRA/QLoRA while keeping replay/evaluation unchanged.

## Run
```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Hardware strategy
Ryzen 7/16 GB: CPU core is trivial. GTX 1650 Ti 4 GB: use <=1.5B model, 4-bit base weights, LoRA rank 4–8, sequence length 256–512, batch 1–2 with gradient accumulation. Do not train a multi-billion-parameter model from scratch.

## Experiments
1. sequential training without replay;
2. fixed replay;
3. forgetting-priority replay;
4. replay-capacity sweep;
5. regularization sweep;
6. optional LoRA backend;
7. task-order sensitivity.

Measure final average accuracy, backward transfer/forgetting, memory footprint, task adaptation accuracy and wall-clock cost.

## Resume bullet
Built a continual-learning NLP platform for sequential domain adaptation with bounded forgetting-priority replay, stability regularization, expandable task learning, catastrophic-forgetting metrics and replay/no-replay benchmarking; designed a low-VRAM LoRA/QLoRA extension and production architecture for streaming task ingestion, model/version lineage, replay governance, distributed training, canary rollout and drift-triggered adaptation.
