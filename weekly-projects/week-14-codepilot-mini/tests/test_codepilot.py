from pathlib import Path
import tempfile
from codepilot.index import scan_repository,python_metadata
from codepilot.retrieval import RepositoryRetriever,select_context
from codepilot.planning import extract_requirements,build_plan
from codepilot.patching import guarded_replace

def files():
    return scan_repository("sample_repo")

def test_ast_symbols():
    symbols,_=python_metadata(Path("sample_repo/orders/pricing.py").read_text())
    assert "calculate_total" in symbols

def test_issue_localizes_pricing_and_test():
    hits=RepositoryRetriever(files()).search("negative total discount clamp add regression test",4)
    paths=[f.path for _,f in hits]
    assert "orders/pricing.py" in paths
    assert "tests/test_pricing.py" in paths

def test_context_budget_and_plan():
    hits=RepositoryRetriever(files()).search("discount total regression test",4)
    chosen=select_context(hits,3000)
    plan=build_plan("clamp total at zero and add regression test",chosen)
    assert plan["candidate_files"] and plan["requirements"]

def test_guarded_replace_prevents_escape_and_applies():
    with tempfile.TemporaryDirectory() as td:
        src=Path(td)/"x.py"; src.write_text("value = 1\n")
        guarded_replace(td,"x.py","1","2")
        assert "2" in src.read_text()
        try:
            guarded_replace(td,"../escape.py","x","y")
            assert False
        except ValueError:
            pass

def test_requirements():
    r=extract_requirements("fix negative totals and add a regression test")
    assert len(r)>=1
