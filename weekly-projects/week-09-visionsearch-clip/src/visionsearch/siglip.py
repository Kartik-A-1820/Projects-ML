from __future__ import annotations
import numpy as np

class SigLIP2Encoder:
    def __init__(self, model_name="google/siglip2-base-patch16-224", device="cpu"):
        import torch
        from transformers import AutoModel, AutoProcessor
        self.torch = torch
        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device).eval()

    def encode_text(self, text):
        inputs = self.processor(text=[text], padding="max_length", return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            features = self.model.get_text_features(**inputs)
        v = features[0].detach().float().cpu().numpy()
        return v / max(np.linalg.norm(v), 1e-12)

    def encode_image(self, image):
        inputs = self.processor(images=[image], return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            features = self.model.get_image_features(**inputs)
        v = features[0].detach().float().cpu().numpy()
        return v / max(np.linalg.norm(v), 1e-12)
