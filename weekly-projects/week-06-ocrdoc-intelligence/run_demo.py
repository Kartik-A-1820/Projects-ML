import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from ocrdoc.pipeline import process_document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_invoice.txt")
    args = parser.parse_args()
    result = process_document(args.input, backend="text")
    print(json.dumps({
        "invoice_number": result["invoice"]["invoice_number"]["value"],
        "total": result["invoice"]["total"]["value"],
        "line_items": len(result["invoice"]["line_items"]),
        "validation_issues": result["validation_issues"],
        "accepted": result["accepted"],
    }, indent=2))


if __name__ == "__main__":
    main()
