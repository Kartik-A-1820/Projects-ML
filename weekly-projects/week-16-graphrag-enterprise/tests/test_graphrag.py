from graphrag_enterprise.router import route
from graphrag_enterprise.engine import GraphRAG
def test_simple_query_lexical():
    assert route("what database stores Atlas metadata")[0]=="lexical"
def test_complex_query_graph():
    assert route("what constraint applies to the plant that operates the service consuming Atlas results")[0]=="graph"
def test_atlas_db():
    r=GraphRAG().search("Atlas PostgreSQL transactional metadata")
    assert r["hits"][0]["id"]=="d1"
def test_multihop_has_policy_doc():
    ids=[x["id"] for x in GraphRAG().search("what infrastructure constraint applies to the plant that operates the service consuming Atlas results")["hits"]]
    assert "d5" in ids
