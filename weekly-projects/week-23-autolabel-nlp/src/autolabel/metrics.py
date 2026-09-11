def evaluate(rows):
 accepted=[r for r in rows if not r['abstain']]
 correct=sum(r.get('gold')==r['label'] for r in accepted)
 return {
  'coverage':len(accepted)/max(1,len(rows)),
  'accepted_accuracy':correct/max(1,len(accepted)),
  'abstention_rate':1-len(accepted)/max(1,len(rows)),
  'review_rate':sum(r['review_score']>0 for r in rows)/max(1,len(rows))
 }
