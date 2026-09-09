from .detectors import injection_score,secret_leak_score
from .normalize import normalize_text
from .policy import assemble_context

class RAGGuard:
    def __init__(self,input_threshold=.65): self.input_threshold=input_threshold
    def inspect_input(self,text):
        normalized=normalize_text(text); score,hits=injection_score(normalized)
        return {"normalized":normalized,"score":score,"hits":hits,"allowed":score<self.input_threshold}
    def inspect_context(self,docs):
        context,decisions=assemble_context(docs)
        return {"context":context,"decisions":decisions,"allowed_docs":[d["doc_id"] for d in decisions if d["allowed"]]}
    def inspect_output(self,text):
        score,hits=secret_leak_score(text)
        return {"score":score,"hits":hits,"allowed":score==0}
