import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'src'))
from llmcache.embedding import similarity
rows=json.loads(Path('data/pairs.json').read_text());th=.45;tp=fp=tn=fn=0
for x in rows:
 pred=similarity(x['a'],x['b'])>=th
 if pred and x['same']:tp+=1
 elif pred and not x['same']:fp+=1
 elif not pred and x['same']:fn+=1
 else:tn+=1
print({'threshold':th,'precision':tp/max(1,tp+fp),'recall':tp/max(1,tp+fn),'hit_ratio':(tp+fp)/len(rows),'false_reuse_rate':fp/max(1,tp+fp)})
