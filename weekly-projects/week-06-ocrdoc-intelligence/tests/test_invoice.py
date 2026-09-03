from pathlib import Path
from ocrdoc.backends import TextBackend
from ocrdoc.invoice import extract_invoice, validate_invoice

SAMPLE = Path("data/sample_invoice.txt").read_text(encoding="utf-8")

def test_text_backend():
    doc = TextBackend().convert("data/sample_invoice.txt")
    assert doc.metadata["backend"] == "text"
    assert "INV-2026-1042" in doc.text

def test_extract_invoice_and_items():
    invoice = extract_invoice(SAMPLE)
    assert invoice["invoice_number"]["value"] == "INV-2026-1042"
    assert invoice["total"]["value"] == 4189.0
    assert len(invoice["line_items"]) == 2

def test_validation_accepts_consistent_invoice():
    assert validate_invoice(extract_invoice(SAMPLE)) == []

def test_validation_catches_bad_total():
    bad = SAMPLE.replace("Total: INR 4189.00", "Total: INR 5000.00")
    assert "total_mismatch" in validate_invoice(extract_invoice(bad))
