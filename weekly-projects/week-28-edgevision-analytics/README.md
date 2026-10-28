# Week 28 — EdgeVision-Analytics
An experimental edge computer-vision analytics pipeline for industrial inspection under tight compute, latency, and bandwidth budgets.
Rather than making the edge device run a heavyweight detector on every frame, the pipeline combines:
- input quality gates,
- region-of-interest tiling,
- frame skipping / adaptive sampling,
- lightweight anomaly scoring,
- event aggregation,
- latency/FPS budgeting,
- confidence-aware cloud escalation hooks,
- quantization-aware deployment metadata.
The default project is completely local and CPU-first. It uses deterministic synthetic inspection frames so the full control plane can be tested without downloading model weights.
## Capabilities
- synthetic industrial inspection stream
- ROI tiling
- blur / brightness quality checks
- adaptive frame sampling
- lightweight local defect scoring
- event aggregation across consecutive frames
- edge/cloud escalation decision
- end-to-end latency and throughput measurement
- precision / recall / F1 for defect events
- quantization metadata / deployment profile
- FastAPI single-frame endpoint
- deterministic tests
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
Default path:
- CPU/Numpy/Pillow only
- no pretrained weights
- 256×256 synthetic inspection frames
- micro-batch friendly
- optional production adapters for ONNX Runtime / OpenVINO / TensorRT
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```
