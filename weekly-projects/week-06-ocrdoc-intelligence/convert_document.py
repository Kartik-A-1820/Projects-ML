import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from ocrdoc.pipeline import process_document, save_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--backend", choices=["text", "pymupdf", "docling"], default="docling")
    parser.add_argument("--json", default="artifacts/document.json")
    parser.add_argument("--markdown", default="artifacts/document.md")
    args = parser.parse_args()

    result = process_document(args.input, backend=args.backend)
    save_result(result, args.json, args.markdown)
    print(json.dumps({
        "accepted": result["accepted"],
        "validation_issues": result["validation_issues"],
        "backend": result["backend"],
    }, indent=2))


if __name__ == "__main__":
    main()
