# Week 26 — VisionRAG-Local

A retrieval-augmented visual exemplar memory for industrial inspection: extract image features, retrieve visually similar labeled examples, fuse exemplar evidence with metadata, calibrate confidence, and abstain when the retrieved neighborhood is inconsistent.

This is intentionally different from:
- Week 09 VisionSearch-CLIP: pure multimodal retrieval/search
- Week 17 VisionAgent-Studio: tool-using visual agent
- Week 32 DocLayout-RAG: document/layout retrieval

Week 26 focuses on **retrieval-assisted visual decision-making** with evidence exemplars.

## 2026 relevance

Recent multimodal-RAG research increasingly treats retrieval as a reasoning primitive rather than a simple search step:
- MM-BRIGHT shows multimodal reasoning-intensive retrieval remains difficult.
- SAR-RAG demonstrates image-exemplar retrieval as an external memory for visual target recognition.
- Current visual/document RAG research emphasizes candidate efficiency, adaptive retrieval and grounded evidence.

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

## Run

```bash
pip install -r requirements.txt
python build_sample_data.py
python run_demo.py
python evaluate.py
pytest -q
```

## Resume bullet

Built a retrieval-augmented visual inspection system that converts images into a searchable exemplar memory, dynamically selects evidence depth from neighborhood agreement, fuses visual similarity with metadata, calibrates confidence and abstains on ambiguous/OOD cases; added retrieval/classification evaluation and a production architecture for GPU embedding services, vector sharding, exemplar governance, online index versioning and evidence-level observability.
