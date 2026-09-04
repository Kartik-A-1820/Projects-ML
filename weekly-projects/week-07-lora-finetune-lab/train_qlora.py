from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
from lora_lab.data import load_jsonl,format_example

def main():
    import torch
    from datasets import Dataset
    from peft import LoraConfig, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig,TrainingArguments
    from trl import SFTTrainer
    parser=argparse.ArgumentParser(); parser.add_argument('--max-steps',type=int,default=30); args=parser.parse_args()
    model_name='Qwen/Qwen2.5-0.5B-Instruct'
    if not torch.cuda.is_available(): raise RuntimeError('QLoRA path requires CUDA; use validate_dataset.py on CPU')
    bnb=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=torch.float16)
    tok=AutoTokenizer.from_pretrained(model_name,use_fast=True); tok.pad_token=tok.eos_token
    model=AutoModelForCausalLM.from_pretrained(model_name,quantization_config=bnb,device_map='auto')
    model=prepare_model_for_kbit_training(model)
    lora=LoraConfig(r=16,lora_alpha=32,lora_dropout=.05,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj'])
    ds=Dataset.from_dict({'text':[format_example(r) for r in load_jsonl('data/train.jsonl')]})
    ta=TrainingArguments(output_dir='checkpoints/qwen05b',max_steps=args.max_steps,per_device_train_batch_size=1,gradient_accumulation_steps=16,learning_rate=2e-4,logging_steps=1,save_steps=max(10,args.max_steps),fp16=True,report_to=[],seed=42)
    trainer=SFTTrainer(model=model,args=ta,train_dataset=ds,peft_config=lora,dataset_text_field='text',max_seq_length=512,tokenizer=tok)
    trainer.train(); trainer.model.save_pretrained('adapters/qwen05b-domain')
if __name__=='__main__': main()
