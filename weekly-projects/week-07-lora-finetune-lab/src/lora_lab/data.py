from __future__ import annotations
import json
from pathlib import Path

REQUIRED={"instruction","input","output"}

def load_jsonl(path:str)->list[dict]:
    rows=[]
    for i,line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        missing=REQUIRED-set(row)
        if missing: raise ValueError(f"line {i} missing {sorted(missing)}")
        if any(not str(row[k]).strip() for k in REQUIRED): raise ValueError(f"line {i} has empty required field")
        rows.append(row)
    if not rows: raise ValueError('dataset is empty')
    return rows

def format_example(row:dict)->str:
    return "### Instruction\n{}\n\n### Input\n{}\n\n### Response\n{}".format(row["instruction"], row["input"], row["output"])

def dataset_report(rows:list[dict])->dict:
    outputs=[r['output'] for r in rows]
    return {'rows':len(rows),'duplicate_outputs':len(outputs)-len(set(outputs)),'avg_output_chars':round(sum(map(len,outputs))/len(outputs),2)}
