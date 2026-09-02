from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score

def main():
    ds=load_dataset('tweet_eval','sentiment')
    v=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=60000,sublinear_tf=True,strip_accents='unicode')
    xtr=v.fit_transform(ds['train']['text']); xv=v.transform(ds['validation']['text'])
    m=LogisticRegression(max_iter=500,class_weight='balanced'); m.fit(xtr,ds['train']['label']); pred=m.predict(xv)
    print('macro_f1=',f1_score(ds['validation']['label'],pred,average='macro')); print(classification_report(ds['validation']['label'],pred,digits=4))
if __name__=='__main__': main()
