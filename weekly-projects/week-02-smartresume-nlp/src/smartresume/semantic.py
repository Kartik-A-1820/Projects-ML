class SemanticScorer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', device='cpu'):
        from sentence_transformers import SentenceTransformer
        self.model=SentenceTransformer(model_name,device=device)
    def score(self,resume_text,job_text):
        import numpy as np
        e=self.model.encode([resume_text,job_text],normalize_embeddings=True,show_progress_bar=False)
        return float(np.dot(e[0],e[1]))
