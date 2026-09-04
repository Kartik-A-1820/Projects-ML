from multipdf_rag.ingest import ingest_text
from multipdf_rag.engine import Engine
from multipdf_rag.metrics import recall_at_k,reciprocal_rank

def test_page_provenance():
    chunks=ingest_text('data/policies.txt'); assert {c.page for c in chunks}=={1,2}; assert chunks[0].source=='policies.txt'

def test_exact_policy_retrieval():
    hits=Engine(['data/policies.txt','data/platform.txt']).retrieve('AC-17 privileged administrator MFA',3); assert hits[0].chunk.chunk_id=='policies.txt:p1:c0'

def test_answer_has_citation():
    result=Engine(['data/policies.txt','data/platform.txt']).query('What does AC-17 require?'); assert result['grounded']; assert result['citations'][0]['page']==1

def test_metrics():
    ids=['a','b']; assert recall_at_k(ids,['a'],1)==1.0; assert reciprocal_rank(ids,['b'])==0.5
