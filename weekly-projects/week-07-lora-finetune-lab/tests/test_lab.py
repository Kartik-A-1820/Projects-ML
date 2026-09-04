import json
from lora_lab.data import load_jsonl,format_example,dataset_report
from lora_lab.metrics import canonical,evaluate_pairs

def test_dataset_valid():
    rows=load_jsonl('data/train.jsonl'); assert len(rows)==4; assert '### Response' in format_example(rows[0]); assert dataset_report(rows)['rows']==4

def test_structured_json_order_ignored():
    a='{\"severity\":\"high\",\"action\":\"scale\"}'; b='{\"action\":\"scale\",\"severity\":\"high\"}'
    assert canonical(a)==canonical(b)

def test_sample_eval_perfect():
    rows=json.load(open('data/sample_predictions.json',encoding='utf-8')); assert evaluate_pairs(rows)['accuracy']==1.0
