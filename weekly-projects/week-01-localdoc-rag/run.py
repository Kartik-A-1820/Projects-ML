import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from localdoc_rag.app import RAGService

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    args = parser.parse_args()
    result = RAGService().query(args.question)
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(source)

if __name__ == "__main__":
    main()
