from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_on_synth_test_on_real(synthetic,real):
    if not synthetic or not real:return 0.0
    v=TfidfVectorizer(ngram_range=(1,2)); X=v.fit_transform([r["text"] for r in synthetic]); y=[r["label"] for r in synthetic]
    m=LogisticRegression(max_iter=400).fit(X,y); pred=m.predict(v.transform([r["text"] for r in real]))
    return float(accuracy_score([r["label"] for r in real],pred))
