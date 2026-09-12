import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from tinyllm.tokenizer import HashTokenizer
from tinyllm.model import TinyEncoder
from tinyllm.data import load_rows,TextDataset
from tinyllm.train import fit,accuracy,resolve_device

tok=HashTokenizer()
train=TextDataset(load_rows("data/train.json"),tok)
eval_rows=load_rows("data/eval.json")
task=TextDataset([r for r in eval_rows if r["slice"]=="task"],tok)
ret=TextDataset([r for r in eval_rows if r["slice"]=="retention"],tok)
device=resolve_device("auto")
results=[]
for name,mode,active in [("full","full",None),("lora","lora",4),("masked_lora","lora",2)]:
    m=TinyEncoder(mode=mode,rank=4,active_rank=active)
    m,sec=fit(m,train,device=device)
    results.append({"experiment":name,"task_accuracy":accuracy(m,task,device),"retention_accuracy":accuracy(m,ret,device),"trainable":m.trainable_parameters(),"total":m.total_parameters(),"trainable_ratio":m.trainable_parameters()/m.total_parameters(),"seconds":round(sec,4)})
print(json.dumps(results,indent=2))
