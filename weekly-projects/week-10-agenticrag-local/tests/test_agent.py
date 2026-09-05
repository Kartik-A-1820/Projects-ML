from agenticrag.retrieval import BM25
from agenticrag.control import CorrectiveRAG, reformulate

DOCS=[
 {"id":"a","title":"E104","text":"payment gateway timeout e104 retry idempotently"},
 {"id":"b","title":"OOMKilled","text":"container exceeded memory limit kubernetes oomkilled"}
]

def test_known_query_grounded():
    r=CorrectiveRAG(BM25(DOCS)).run("e104 payment timeout")
    assert r["status"]=="grounded"
    assert r["hits"][0]["id"]=="a"

def test_bounded_unknown_abstains():
    r=CorrectiveRAG(BM25(DOCS),max_steps=2).run("quantum banana protocol")
    assert r["status"]=="abstain"
    assert len(r["trace"])<=2

def test_reformulation_alias():
    assert "oomkilled" in reformulate("out of memory")
