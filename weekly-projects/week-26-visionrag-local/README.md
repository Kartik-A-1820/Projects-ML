# Week 26 — VisionRAG-Local
A retrieval-augmented visual exemplar memory for industrial inspection: extract image features, retrieve visually similar labeled examples, fuse exemplar evidence with metadata, calibrate confidence, and abstain when the retrieved neighborhood is inconsistent.
This is intentionally different from:
- Week 09 VisionSearch-CLIP: pure multimodal retrieval/search
- Week 17 VisionAgent-Studio: tool-using visual agent
- Week 32 DocLayout-RAG: document/layout retrieval
Week 26 focuses on **retrieval-assisted visual decision-making** with evidence exemplars.
## Capabilities
- deterministic synthetic industrial-inspection image generator
- lightweight image embedding: color moments + edge/texture histograms
- optional metadata features
- cosine exemplar retrieval
- adaptive-k retrieval based on neighborhood agreement
- weighted neighbor voting
- confidence/margin calibration
- OOD / ambiguous-neighborhood abstention
- exemplar evidence trace
- retrieval Recall@K + classification accuracy + abstention evaluation
- FastAPI endpoint
- optional production adapter point for SigLIP/CLIP/DINOv2 embeddings
## Hardware
Default pipeline is CPU-only and runs comfortably on Ryzen 7 / 16 GB RAM. A small open vision encoder can later use the GTX 1650 Ti 4 GB with batch size 1–8.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Run
```bash
python -m pip install -r requirements.txt
python build_sample_data.py
python run_demo.py
python evaluate.py
python -m pytest -q
```
