from intent_engine.model import IntentClassifier
from intent_engine.evaluation import classification_metrics, perturb

X=['payment failed','card declined','refund missing','refund status','forgot password','reset password','track package','order status']
y=['pay','pay','refund','refund','auth','auth','track','track']

def model(): return IntentClassifier(oos_threshold=.19,ambiguity_margin=.01,similarity_threshold=.05).fit(X,y)

def test_known_intent():
    assert model().predict_one('card payment declined').intent=='pay'

def test_unknown_can_reject():
    p=IntentClassifier(oos_threshold=.70,ambiguity_margin=.01,similarity_threshold=.05).fit(X,y).predict_one('weather forecast tomorrow')
    assert p.intent=='out_of_scope'

def test_metrics():
    m=classification_metrics(['a','b'],['a','b'])
    assert m['accuracy']==1 and m['macro_f1']==1

def test_perturb(): assert 'transaction' in perturb('payment failed')
