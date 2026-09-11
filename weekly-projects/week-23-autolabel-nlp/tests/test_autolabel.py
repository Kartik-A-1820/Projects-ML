from autolabel.labelers import all_votes
from autolabel.aggregate import aggregate
from autolabel.active import select_for_review
from autolabel.pipeline import label_rows
from autolabel.metrics import evaluate

def test_votes_exist(): assert len(all_votes('refund missing'))==3
def test_consensus_label(): assert aggregate(['refund','refund','payment'],min_confidence=.66)['label']=='refund'
def test_abstains_on_split(): assert aggregate(['refund','payment','account'])['abstain']
def test_review_prefers_uncertainty():
 rows=[{'text':'a','review_score':0.1},{'text':'b','review_score':0.9}];assert select_for_review(rows,1)[0]['text']=='b'
def test_pipeline_and_metrics():
 items=[{'text':'refund missing','gold':'refund'},{'text':'reset password','gold':'account'}];rows,_=label_rows(items);m=evaluate(rows);assert 0<=m['coverage']<=1 and 0<=m['accepted_accuracy']<=1
