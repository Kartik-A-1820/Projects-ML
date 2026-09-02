import argparse,json,sys
from pathlib import Path
import numpy as np
from sklearn.metrics import classification_report,f1_score
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from sentiment_lab.metrics import expected_calibration_error,find_temperature,softmax
from sentiment_lab.slices import accuracy_by_slice

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); a=p.parse_args(); d=json.loads(Path(a.input).read_text())
    logits=np.asarray(d['logits']); labels=np.asarray(d['labels']); texts=d['texts']; t=find_temperature(logits,labels)
    raw=softmax(logits); cal=softmax(logits,t); pred=cal.argmax(axis=1)
    print('temperature=',round(t,4)); print('macro_f1=',round(f1_score(labels,pred,average='macro'),4)); print('ece_raw=',round(expected_calibration_error(raw,labels),4)); print('ece_calibrated=',round(expected_calibration_error(cal,labels),4)); print('slice_accuracy=',accuracy_by_slice(pred,labels,texts)); print(classification_report(labels,pred,digits=4))
if __name__=='__main__': main()
