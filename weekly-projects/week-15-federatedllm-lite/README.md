# Week 15 — FederatedLLM-Lite
Privacy-aware federated parameter-efficient fine-tuning for small language models under non-IID client data.
This project simulates a realistic cross-silo federated adaptation workflow on a single workstation: multiple clients keep text data local, train only LoRA-style adapter parameters, clip/noise local updates when privacy mode is enabled, aggregate weighted adapter deltas, evaluate the global model after every round, and report communication/heterogeneity metrics.
The default implementation uses a tiny PyTorch text classifier with LoRA-injected linear layers so the complete federated mechanics can run on Ryzen 7 / 16 GB RAM / GTX 1650 Ti 4 GB without downloading large model weights. The architecture includes a production upgrade path to Hugging Face PEFT with compact SLMs.
## Industry use cases
- healthcare networks adapting clinical language models without centralizing patient text
- banks collaboratively adapting fraud/support classifiers across branches or regions
- industrial companies sharing model improvements across plants while retaining proprietary logs locally
- telecom or device fleets adapting edge SLMs using private user/device data
- regulated enterprise copilots where raw prompt/feedback data cannot leave a tenant boundary
## Methodology
- federated learning orchestration and non-IID client simulation
- parameter-efficient fine-tuning / LoRA
- privacy hooks: update clipping + Gaussian noise
- secure-aggregation simulation with canceling masks
- weighted FedAvg over adapters only
- communication-cost accounting
- client/round metrics and worst-client reporting
- deterministic training and reproducibility
- FastAPI control endpoint
- tests, smoke benchmark and production architecture
- model/update lineage and rollout design
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM. Default run is CPU-safe with LoRA rank 4, four clients, one local epoch and no model download.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Setup
```bash
python -m pip install -r requirements.txt
python run_federated.py --config configs/config.yaml
python -m pytest -q
uvicorn federated_lite.api:app --app-dir src --host 127.0.0.1 --port 8150
```
## Recommended real-model experiment
Upgrade the tiny model to a 0.5B-class open SLM with Hugging Face PEFT, LoRA rank 4–8, batch size 1, gradient accumulation 8–16 and optional 4-bit loading where supported. Compare centralized LoRA, vanilla FedAvg-LoRA, clipped FedAvg-LoRA, clipped+noised FedAvg-LoRA and a frozen/alternating-factor variant inspired by current FedLoRA research.
