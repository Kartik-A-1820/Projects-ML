import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from continuallearn.trainer import ContinualTrainer
tasks=json.loads((ROOT/'sample_data/tasks.json').read_text());tr=ContinualTrainer()
for t in tasks:print(tr.learn(t['task'],t['samples'],epochs=20))
