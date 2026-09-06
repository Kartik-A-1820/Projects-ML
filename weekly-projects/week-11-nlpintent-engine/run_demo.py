import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from intent_engine.io import load_rows
from intent_engine.model import IntentClassifier
from intent_engine.evaluation import classification_metrics, perturb

train=load_rows('data/intents.json'); eval_rows=load_rows('data/eval.json')
clf=IntentClassifier(oos_threshold=0.19,ambiguity_margin=0.01,similarity_threshold=0.05).fit([r['text'] for r in train],[r['intent'] for r in train])
pred=[clf.predict_one(r['text']).intent for r in eval_rows]
print(classification_metrics([r['intent'] for r in eval_rows],pred))
for r in eval_rows[:5]:
    p=clf.predict_one(perturb(r['text']))
    print('perturbed:',r['text'],'=>',p.intent,round(p.confidence,3),p.reason)
