import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from lora_lab.data import load_jsonl,dataset_report
from lora_lab.metrics import evaluate_pairs
print(dataset_report(load_jsonl('data/train.jsonl')))
print(evaluate_pairs(json.loads(Path('data/sample_predictions.json').read_text(encoding='utf-8'))))
