import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from continuallearn.trainer import ContinualTrainer
tasks=json.loads((ROOT/'sample_data/tasks.json').read_text())
def run(replay):
    tr=ContinualTrainer(replay_per_task=replay);rows=[]
    for t in tasks:rows.append(tr.learn(t['task'],t['samples'],epochs=30))
    return rows[-1]
print(json.dumps({'no_replay':run(0),'forgetting_priority_replay':run(24)},indent=2))
