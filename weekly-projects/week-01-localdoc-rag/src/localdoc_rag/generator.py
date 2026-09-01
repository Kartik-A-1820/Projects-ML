from __future__ import annotations
import torch

class LocalGenerator:
    def __init__(self, model_name: str, device: str = "auto") -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        dtype = torch.float16 if device == "cuda" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=dtype, low_cpu_mem_usage=True).to(device)
        self.model.eval()

    @torch.inference_mode()
    def answer(self, question: str, context: str, max_new_tokens: int = 220) -> str:
        messages = [{"role":"system","content":"Answer only from supplied context. Cite [source_1]. If evidence is insufficient, say so."},{"role":"user","content":f"Context:\n{context}\n\nQuestion:\n{question}"}]
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=3072).to(self.device)
        output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, repetition_penalty=1.05, pad_token_id=self.tokenizer.eos_token_id)
        generated = output[0, inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(generated, skip_special_tokens=True).strip()
