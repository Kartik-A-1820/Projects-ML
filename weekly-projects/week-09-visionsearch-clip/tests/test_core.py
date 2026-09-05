from visionsearch.core import DeterministicTextImageEncoder, VectorIndex
from visionsearch.metrics import recall_at_k, reciprocal_rank


def test_semantic_token_overlap():
    enc=DeterministicTextImageEncoder()
    idx=VectorIndex()
    idx.add("a",enc.encode_image_descriptor("red truck highway"),{"category":"vehicle"})
    idx.add("b",enc.encode_image_descriptor("invoice table document"),{"category":"document"})
    assert idx.search(enc.encode_text("red truck"),1)[0][1]=="a"


def test_filtering():
    enc=DeterministicTextImageEncoder(); idx=VectorIndex()
    idx.add("a",enc.encode_text("red truck"),{"category":"vehicle"})
    idx.add("b",enc.encode_text("truck invoice"),{"category":"document"})
    hits=idx.search(enc.encode_text("truck"),5,{"category":"document"})
    assert [x[1] for x in hits]==["b"]


def test_metrics():
    assert recall_at_k(["a","b"],{"a"},1)==1.0
    assert reciprocal_rank(["b","a"],{"a"})==0.5
