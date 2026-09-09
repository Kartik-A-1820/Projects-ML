import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from ragguard.detectors import injection_score
rows=json.loads(Path("data/eval.json").read_text());tp=tn=fp=fn=0
for r in rows:
    pred=injection_score(r["text"])[0]>=.65
    if pred and r["malicious"]:tp+=1
    elif pred and not r["malicious"]:fp+=1
    elif not pred and r["malicious"]:fn+=1
    else:tn+=1
precision=tp/(tp+fp) if tp+fp else 0;recall=tp/(tp+fn) if tp+fn else 0;fpr=fp/(fp+tn) if fp+tn else 0
print({"tp":tp,"tn":tn,"fp":fp,"fn":fn,"precision":precision,"recall":recall,"false_positive_rate":fpr})
