from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .backends import get_backend
from .invoice import extract_invoice, validate_invoice


def process_document(path: str, backend: str = "text") -> dict:
    document = get_backend(backend).convert(path)
    invoice = extract_invoice(document.text)
    issues = validate_invoice(invoice)
    return {"source": document.source, "backend": document.metadata.get("backend"), "text": document.text, "blocks": [asdict(x) for x in document.blocks], "invoice": invoice, "validation_issues": issues, "accepted": len(issues) == 0}


def save_result(result: dict, output_json: str | None = None, output_markdown: str | None = None):
    if output_json:
        path = Path(output_json); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if output_markdown:
        inv = result["invoice"]
        md = ["# Extracted Invoice", f"- Invoice: {inv['invoice_number']['value']}", f"- Date: {inv['invoice_date']['value']}", f"- PO: {inv['purchase_order']['value']}", f"- Total: {inv['total']['value']}", f"- Accepted: {result['accepted']}", "", "## Validation", *[f"- {x}" for x in result["validation_issues"]]]
        path = Path(output_markdown); path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(md), encoding="utf-8")
