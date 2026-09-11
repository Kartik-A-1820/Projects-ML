import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from autolabel.pipeline import label_rows
from autolabel.metrics import evaluate
rows=json.loads(Path('data/items.json').read_text());labeled,review=label_rows(rows,review_budget=4)
print(evaluate(labeled));print('review_queue',[x['text'] for x in review])
