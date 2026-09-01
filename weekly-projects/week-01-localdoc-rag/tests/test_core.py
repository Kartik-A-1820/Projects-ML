from localdoc_rag.core import build_context, chunk_text

def test_chunk_overlap():
    text = " ".join(f"w{i}" for i in range(30))
    chunks = chunk_text(text, "demo.md", size=10, overlap=2)
    assert len(chunks) >= 3
    assert "w8" in chunks[1].text

def test_context_citation():
    chunk = chunk_text("alpha beta", "demo.md")[0]
    context = build_context([(chunk, 0.1)])
    assert "[source_1]" in context
    assert "demo.md" in context
