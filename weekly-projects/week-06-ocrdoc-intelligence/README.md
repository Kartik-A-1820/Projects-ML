# Week 06 — OCRDoc-Intelligence (2026 Rebuild)

A local document-intelligence pipeline that converts business documents into normalized text/Markdown, extracts structured invoice fields, validates evidence, and preserves page/source provenance.

The core project runs without downloading OCR models. Real PDF/image parsing is provided through optional **Docling** and **PyMuPDF** adapters, while the architecture documents a production upgrade path to modern document VLM parsers such as PaddleOCR-VL.

## Features
- backend-neutral document schema
- native text/PDF adapter path
- optional Docling OCR/layout/table adapter
- invoice field extraction
- line-item table extraction from normalized text
- validation and confidence/evidence metadata
- Markdown + JSON output
- provenance by page/source
- deterministic synthetic tests
- production scaling architecture

## 2026 relevance
Modern document AI is moving beyond plain OCR toward layout-aware parsing of text, tables, figures, formulas and document hierarchy. Docling exposes a unified document representation with layout/provenance, while PaddleOCR-VL-1.5 targets robust multilingual document parsing with a compact 0.9B VLM.

## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.

Local default:
- native text first;
- OCR only when needed;
- CPU-safe extraction and validation;
- optional Docling acceleration;
- no paid OCR API.

## Smoke demo
```bash
python run_demo.py --input data/sample_invoice.txt
```

## Optional real PDF conversion
```bash
pip install "docling>=2"
python convert_document.py --input invoice.pdf --backend docling
```

## Tests
```bash
pytest -q
```

## Resume bullet
Built a local document-intelligence pipeline with backend-neutral OCR/layout conversion, structured invoice extraction, table normalization, evidence/provenance tracking and validation gates; designed a production architecture for asynchronous document ingestion, CPU/GPU OCR tiers, model routing, human review, lineage, PII controls and scalable structured-document APIs.
