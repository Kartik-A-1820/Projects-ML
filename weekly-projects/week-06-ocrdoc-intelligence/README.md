# Week 06 — OCRDoc-Intelligence
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
- proposed deployment architecture notes
## Hardware target
Ryzen 7 4800-series CPU, 16 GB RAM, GTX 1650 Ti 4 GB VRAM.
Local default:
- native text first;
- OCR only when needed;
- CPU-safe extraction and validation;
- optional Docling acceleration;
- no paid OCR API.
Run commands from this lab's directory in an activated, isolated environment. See the [setup and contribution guide](../../CONTRIBUTING.md) before starting.
## Smoke demo
```bash
python run_demo.py --input data/sample_invoice.txt
```
## Optional real PDF conversion
```bash
python -m pip install "docling>=2"
python convert_document.py --input invoice.pdf --backend docling
```
## Tests
```bash
python -m pytest -q
```
