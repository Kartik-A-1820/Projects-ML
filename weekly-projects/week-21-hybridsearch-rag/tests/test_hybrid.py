from hybridrag.core import query_family,HybridEngine,rrf,weighted,expand
def test_exact_router():assert query_family("E104")=="exact"
def test_semantic_router():assert query_family("how can search find similar meaning with different wording")=="semantic"
def test_exact_id_retrieval():assert HybridEngine().search("AX-7742 bracket",3)["hits"][0]["id"]=="d2"
def test_mixed_policy_retrieves_security_policy():assert "d8" in [x["id"] for x in HybridEngine().search("AC-17 privileged review frequency",5)["hits"]]
def test_prf_expands():
 e=HybridEngine();s=e.sparse.search("refund missing",3);assert len(expand("refund missing",s))>=len("refund missing")
def test_fusions_return_ranked_results():
 e=HybridEngine();s=e.sparse.search("hybrid retrieval",5);d=e.dense.search("hybrid retrieval",5);assert rrf([s,d],top_k=3) and weighted(s,d,top_k=3)
