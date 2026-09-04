import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from lora_lab.metrics import evaluate_pairs
p=argparse.ArgumentParser(); p.add_argument('--predictions',required=True); a=p.parse_args()
rows=json.loads(Path(a.predictions).read_text(encoding='utf-8')); print(evaluate_pairs(rows))
