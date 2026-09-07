from videorag.io import load_events
from videorag.retrieval import VideoRetriever,infer_intent,evidence_bundle
from videorag.metrics import recall_at_k

def engine():
    return VideoRetriever(load_events("data/events.json"))

def test_visual_query_routes_visual():
    assert infer_intent("what visual evidence is shown")=="visual_query"

def test_retrieves_j14_event():
    hits=engine().search("connector J14 torque",3)
    assert hits[0].event_id=="e3"

def test_temporal_expansion_can_include_neighbor():
    ids=[h.event_id for h in engine().search("what happens after J14 repair",5)]
    assert "e4" in ids

def test_evidence_has_timestamp_and_citation():
    b=evidence_bundle("test",engine().search("final motor test",3))
    assert "[e5" in b and "110-145s" in b

def test_metric():
    assert recall_at_k(["e3","e4"],["e3"],1)==1.0
