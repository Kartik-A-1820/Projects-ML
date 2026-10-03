from src.metrics import *
def test_rank_metrics():
    r=[3,2,1]
    assert recall_at_k(r,2,2)==1
    assert mrr_at_k(r,2,3)==.5
    assert 0<ndcg_at_k(r,2,3)<1
def test_coverage_tail():
    assert coverage([[1,2],[2,3]],{1,2,3,4})==.75
    assert tail_share([[1,2]],{2})==.5
