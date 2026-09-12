import json
from pathlib import Path
import torch
from torch.utils.data import Dataset
class TextDataset(Dataset):
    def __init__(self,rows,tok):self.rows=rows;self.tok=tok
    def __len__(self):return len(self.rows)
    def __getitem__(self,i):
        r=self.rows[i];return self.tok.encode(r["text"]),torch.tensor(r["label"],dtype=torch.long)
def load_rows(path):return json.loads(Path(path).read_text())
