import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from datasynth.generator import generate
from datasynth.quality import gate_dataset
from datasynth.utility import train_on_synth_test_on_real
ref=json.loads(Path("data/reference.json").read_text());rows=[]
for i,label in enumerate(["payment","refund","account","shipping"]): rows += generate(label,8,42+i)
g=gate_dataset(rows,ref,copy_threshold=.90)
print("accepted",len(g["accepted"]),"rejected",len(g["rejected"]),"diversity",round(g["diversity"],3),"balance",g["label_balance"])
print("utility",train_on_synth_test_on_real(g["accepted"],ref))
