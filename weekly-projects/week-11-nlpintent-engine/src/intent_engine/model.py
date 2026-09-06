from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class IntentPrediction:
    intent: str
    confidence: float
    second_best: float
    nearest_similarity: float
    accepted: bool
    reason: str

class IntentClassifier:
    def __init__(self,oos_threshold=0.19,ambiguity_margin=0.01,similarity_threshold=0.05):
        self.oos_threshold=oos_threshold
        self.ambiguity_margin=ambiguity_margin
        self.similarity_threshold=similarity_threshold
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,strip_accents='unicode',lowercase=True)
        self.model=LogisticRegression(max_iter=600,class_weight='balanced',random_state=42)
        self._train_X=None

    def fit(self,texts,labels):
        X=self.vectorizer.fit_transform(texts)
        self._train_X=X
        self.model.fit(X,labels)
        return self

    def predict_one(self,text):
        X=self.vectorizer.transform([text])
        probs=self.model.predict_proba(X)[0]
        order=np.argsort(-probs)
        best,second=int(order[0]),int(order[1])
        conf=float(probs[best]); second_prob=float(probs[second]); margin=conf-second_prob
        nearest=float(cosine_similarity(X,self._train_X).max()) if X.nnz else 0.0
        if nearest<self.similarity_threshold:
            return IntentPrediction('out_of_scope',conf,second_prob,nearest,False,'low_similarity')
        if conf<self.oos_threshold:
            return IntentPrediction('out_of_scope',conf,second_prob,nearest,False,'low_confidence')
        if margin<self.ambiguity_margin:
            return IntentPrediction('out_of_scope',conf,second_prob,nearest,False,'ambiguous')
        return IntentPrediction(str(self.model.classes_[best]),conf,second_prob,nearest,True,'accepted')
