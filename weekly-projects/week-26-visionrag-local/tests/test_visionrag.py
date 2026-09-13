import json
from pathlib import Path
from visionrag.synthetic import generate_dataset,make_image
from visionrag.index import ExemplarIndex
from visionrag.engine import VisionRAG,adaptive_k
from visionrag.features import embed_image

def setup_engine(tmp_path):
    rows=generate_dataset(tmp_path/"imgs",per_class=4)
    p=tmp_path/"manifest.json";p.write_text(json.dumps(rows))
    return VisionRAG(ExemplarIndex.build(p),min_similarity=.65)

def test_embedding_dimension():
    assert len(embed_image(make_image("normal",1)))==18

def test_adaptive_k_reduces_on_agreement():
    class X:
        def __init__(self,label):self.label=label
    rows=[(.9,X("a")),(.8,X("a")),(.7,X("a")),(.6,X("b"))]
    assert adaptive_k(rows,3,4)==3

def test_scratch_retrieves_evidence(tmp_path):
    r=setup_engine(tmp_path).predict(make_image("scratch",777))
    assert r["evidence"] and r["adaptive_k"]>=1

def test_prediction_trace_has_similarity(tmp_path):
    r=setup_engine(tmp_path).predict(make_image("dent",778))
    assert "top_similarity" in r and all("similarity" in x for x in r["evidence"])
