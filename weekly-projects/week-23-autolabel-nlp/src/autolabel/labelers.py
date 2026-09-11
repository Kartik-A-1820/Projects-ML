LABELS=['payment','refund','account','shipping']
RULES={
'payment':{'payment','declined','transaction','merchant'},
'refund':{'refund','reimbursement','returned','missing'},
'account':{'password','login','account','profile','unlock','access'},
'shipping':{'shipment','package','delivery','courier','tracking'},
}
def keyword_labeler(text):
 t=set(text.lower().split()); scores={k:len(v&t) for k,v in RULES.items()};m=max(scores.values())
 return None if m==0 else max(scores,key=scores.get)
def phrase_labeler(text):
 q=text.lower()
 if 'refund' in q or 'reimbursement' in q:return 'refund'
 if 'password' in q or 'login' in q or 'profile' in q:return 'account'
 if 'shipment' in q or 'courier' in q or 'tracking' in q:return 'shipping'
 if 'payment' in q or 'declined' in q:return 'payment'
 return None
def synthetic_slm_labeler(text):
 # deterministic stand-in for an optional local SLM annotator
 q=text.lower()
 scores={k:sum(term in q for term in terms) for k,terms in RULES.items()};m=max(scores.values())
 return None if m==0 else max(scores,key=scores.get)
def all_votes(text): return [keyword_labeler(text),phrase_labeler(text),synthetic_slm_labeler(text)]
