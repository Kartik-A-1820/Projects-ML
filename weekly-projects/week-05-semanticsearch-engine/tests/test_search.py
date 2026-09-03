from semantic_search.bm25 import BM25Index
from semantic_search.fusion import reciprocal_rank_fusion
from semantic_search.metrics import ndcg_at_k, recall_at_k, reciprocal_rank
from semantic_search.models import Document, SearchHit


DOCS = [
    Document("a", "Error E104", "payment gateway timeout E104", {"domain": "fintech"}),
    Document("b", "Search", "semantic dense embeddings", {"domain": "search"}),
    Document("c", "BM25", "exact keyword error codes", {"domain": "search"}),
]


def test_bm25_exact_identifier():
    hits = BM25Index(DOCS).search("E104 timeout", top_k=2)
    assert hits[0].doc_id == "a"


def test_metadata_filter():
    hits = BM25Index(DOCS).search("error", filters={"domain": "search"})
    assert all(h.metadata["domain"] == "search" for h in hits)


def test_rrf_and_metrics():
    a = SearchHit("a", "a", "a", .9, "dense")
    b = SearchHit("b", "b", "b", .8, "dense")
    fused = reciprocal_rank_fusion([[a, b], [b, a]], top_k=2)
    assert {x.doc_id for x in fused} == {"a", "b"}
    ranked = ["a", "b"]
    relevant = {"a"}
    assert recall_at_k(ranked, relevant, 1) == 1.0
    assert reciprocal_rank(ranked, relevant) == 1.0
    assert ndcg_at_k(ranked, relevant, 2) == 1.0
