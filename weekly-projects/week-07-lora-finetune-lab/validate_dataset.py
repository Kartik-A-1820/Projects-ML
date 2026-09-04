import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from lora_lab.data import load_jsonl,dataset_report,format_example
for name in ['data/train.jsonl','data/eval.jsonl']:
    rows=load_jsonl(name); print(name,dataset_report(rows)); print(format_example(rows[0])[:180])
