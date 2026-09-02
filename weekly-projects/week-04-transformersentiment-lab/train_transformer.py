import argparse, json
from pathlib import Path
import numpy as np, torch
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
MODEL='microsoft/deberta-v3-small'

def main():
    p=argparse.ArgumentParser(); p.add_argument('--epochs',type=int,default=2); p.add_argument('--max-train',type=int,default=12000); a=p.parse_args()
    ds=load_dataset('tweet_eval','sentiment'); tok=AutoTokenizer.from_pretrained(MODEL,use_fast=True)
    tokenized=ds.map(lambda b: tok(b['text'],truncation=True,max_length=128),batched=True)
    train=tokenized['train'].select(range(min(a.max_train,len(tokenized['train'])))); val=tokenized['validation']
    model=AutoModelForSequenceClassification.from_pretrained(MODEL,num_labels=3); model.gradient_checkpointing_enable()
    args=TrainingArguments(output_dir='checkpoints/deberta-sentiment',num_train_epochs=a.epochs,learning_rate=2e-5,per_device_train_batch_size=4,per_device_eval_batch_size=8,gradient_accumulation_steps=4,fp16=bool(torch.cuda.is_available()),eval_strategy='epoch',save_strategy='epoch',load_best_model_at_end=True,metric_for_best_model='eval_loss',report_to=[],seed=42)
    trainer=Trainer(model=model,args=args,train_dataset=train,eval_dataset=val); trainer.train(); pred=trainer.predict(val)
    Path('artifacts').mkdir(exist_ok=True); Path('artifacts/predictions.json').write_text(json.dumps({'logits':np.asarray(pred.predictions).tolist(),'labels':list(map(int,val['label'])),'texts':list(val['text']),'model_name':MODEL}))
    trainer.save_model('models/deberta-sentiment')
if __name__=='__main__': main()
