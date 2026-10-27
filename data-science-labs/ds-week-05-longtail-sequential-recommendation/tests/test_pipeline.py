import pytest
from run_lab import synthetic,split_events,run
from src.recommender import Recommenders

def test_chronology_and_catalog_use_training_only():
    events=[(0,i,5,i) for i in range(7)]+[(1,i,5,i) for i in range(10,17)]
    train,val,test=split_events(events[::-1])
    assert train[0]==[0,1,2,3,4] and val[0]==5 and test[0]==6
    model=Recommenders(train,epochs=1)
    assert 5 not in model.items and 6 not in model.items
    for method in ('popularity','markov','bpr','bpr_tail'):
        ranking=model.recommend(0,train[0]+[val[0]],method,100,.5)
        assert set(ranking).isdisjoint(train[0])
        assert set(ranking).issubset(model.items)

def test_reconstruction_is_deterministic_and_bounded():
    events=synthetic(users=10,items=30)
    first=run(events,'SYNTHETIC_TEST',epochs=1)
    assert first==run(events,'SYNTHETIC_TEST',epochs=1)
    for split in ('validation','test'):
        for metrics in first[split].values():
            assert all(0<=metrics[key]<=1 for key in ('recall','ndcg','mrr','coverage','tail_exposure'))

def test_empty_and_fully_observed_catalog():
    with pytest.raises(ValueError):
        split_events([])
    model=Recommenders({0:[1,2,3]},epochs=2)
    assert model.recommend(0,[1,2,3],'bpr',5)==[]
