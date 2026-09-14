# Week 28 — EdgeVision-Analytics

A production-minded edge computer-vision analytics pipeline for industrial inspection under tight compute, latency, and bandwidth budgets.

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

## Why this is current

Edge deployment in 2026 is increasingly about the **accuracy/latency/power/memory frontier**, not model accuracy alone. Current OpenVINO tooling emphasizes post-training quantization and low-precision inference, while recent industrial inspection work continues to benchmark optimized YOLO-style detectors on edge devices.

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

## Run

```bash
pip install -r requirements.txt
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet

Built an edge-optimized industrial vision analytics pipeline with image-quality gating, ROI tiling, adaptive frame sampling, local anomaly scoring, temporal event aggregation, confidence-aware escalation and latency/FPS benchmarking; designed production deployment for ONNX/OpenVINO/TensorRT, INT8 quantization, GPU/CPU/NPU routing, edge buffering, fleet telemetry, model rollout, failover and bandwidth-aware cloud escalation.
