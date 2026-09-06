from __future__ import annotations

def classification_metrics(y_true,y_pred):
    labels=sorted(set(y_true)|set(y_pred)); per_class={}
    for label in labels:
        tp=sum(a==label and b==label for a,b in zip(y_true,y_pred))
        fp=sum(a!=label and b==label for a,b in zip(y_true,y_pred))
        fn=sum(a==label and b!=label for a,b in zip(y_true,y_pred))
        precision=tp/(tp+fp) if tp+fp else 0.0
        recall=tp/(tp+fn) if tp+fn else 0.0
        f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
        per_class[label]={"precision":precision,"recall":recall,"f1":f1}
    macro_f1=sum(x['f1'] for x in per_class.values())/len(per_class)
    accuracy=sum(a==b for a,b in zip(y_true,y_pred))/len(y_true)
    return {"accuracy":accuracy,"macro_f1":macro_f1,"per_class":per_class}

def perturb(text):
    swaps={"payment":"transaction","refund":"reimbursement","password":"passcode","order":"shipment","subscription":"membership"}
    out=text.lower()
    for a,b in swaps.items(): out=out.replace(a,b)
    return out
