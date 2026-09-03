from __future__ import annotations

from dataclasses import dataclass, asdict
import re

MONEY = r"([A-Z]{3}\s*)?([0-9][0-9,]*(?:\.[0-9]{1,2})?)"

@dataclass
class Evidence:
    value: str | float | None
    matched_text: str | None
    confidence: float

@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    amount: float

def _match(pattern: str, text: str, flags=re.IGNORECASE):
    m = re.search(pattern, text, flags)
    if not m:
        return None, None
    return m.group(1).strip(), m.group(0).strip()

def _money(pattern: str, text: str) -> Evidence:
    m = re.search(pattern + MONEY, text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return Evidence(None, None, 0.0)
    value = float(m.groups()[-1].replace(",", ""))
    return Evidence(value, m.group(0).strip(), 0.98)

def extract_line_items(text: str) -> list[LineItem]:
    items = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4 or parts[0].lower() in {"item", "description"}:
            continue
        try:
            qty = float(parts[1]); unit_price = float(parts[2].replace(",", "")); amount = float(parts[3].replace(",", ""))
        except ValueError:
            continue
        items.append(LineItem(parts[0], qty, unit_price, amount))
    return items

def extract_invoice(text: str) -> dict:
    invoice_no, invoice_match = _match(r"invoice\s*(?:no|number|#)\s*[:\-]\s*([A-Z0-9\-/]+)", text)
    invoice_date, date_match = _match(r"invoice\s*date\s*[:\-]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    po_no, po_match = _match(r"purchase\s*order\s*[:\-]\s*([A-Z0-9\-/]+)", text)
    gstin, gstin_match = _match(r"(?:vendor\s*)?gstin\s*[:\-]\s*([A-Z0-9]{15})", text)
    return {
        "invoice_number": asdict(Evidence(invoice_no, invoice_match, 0.99 if invoice_no else 0.0)),
        "invoice_date": asdict(Evidence(invoice_date, date_match, 0.98 if invoice_date else 0.0)),
        "purchase_order": asdict(Evidence(po_no, po_match, 0.96 if po_no else 0.0)),
        "vendor_gstin": asdict(Evidence(gstin, gstin_match, 0.98 if gstin else 0.0)),
        "subtotal": asdict(_money(r"^\s*subtotal\s*[:\-]\s*", text)),
        "tax": asdict(_money(r"^\s*tax\s*[:\-]\s*", text)),
        "total": asdict(_money(r"^\s*total\s*[:\-]\s*", text)),
        "line_items": [asdict(x) for x in extract_line_items(text)],
    }

def validate_invoice(invoice: dict, tolerance: float = 0.02) -> list[str]:
    issues = []
    if not invoice["invoice_number"]["value"]:
        issues.append("missing_invoice_number")
    if invoice["total"]["value"] is None:
        issues.append("missing_total")
    items = invoice["line_items"]
    for index, item in enumerate(items):
        expected = item["quantity"] * item["unit_price"]
        if abs(expected - item["amount"]) > max(tolerance, tolerance * max(1.0, item["amount"])):
            issues.append(f"line_{index+1}_amount_mismatch")
    subtotal = invoice["subtotal"]["value"]
    if subtotal is not None and items:
        item_sum = sum(x["amount"] for x in items)
        if abs(item_sum - subtotal) > max(tolerance, tolerance * max(1.0, subtotal)):
            issues.append("subtotal_mismatch")
    tax = invoice["tax"]["value"]; total = invoice["total"]["value"]
    if subtotal is not None and tax is not None and total is not None and abs((subtotal + tax) - total) > max(tolerance, tolerance * max(1.0, total)):
        issues.append("total_mismatch")
    return issues
