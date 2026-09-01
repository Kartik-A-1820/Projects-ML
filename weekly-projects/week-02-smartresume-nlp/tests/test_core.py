from smartresume.core import extract_skills, match_resume_to_job, normalize_text
def test_pii_removed():
    c=normalize_text('Jane jane@example.com +91 99999 88888 Python Engineer'); assert 'jane@example.com' not in c and '99999' not in c and 'python' in c
def test_skill_normalization():
    s=extract_skills('Built Retrieval-Augmented Generation with PyTorch and K8s'); assert 'rag' in s and 'pytorch' in s and 'kubernetes' in s
def test_match_identifies_gap():
    r=match_resume_to_job('Python ML engineer with NLP, PyTorch, Docker and SQL.','Need Python, machine learning, NLP, PyTorch, Docker, SQL and Kubernetes.'); assert r.overall_score>0 and 'kubernetes' in r.missing_skills and 'python' in r.matched_skills
