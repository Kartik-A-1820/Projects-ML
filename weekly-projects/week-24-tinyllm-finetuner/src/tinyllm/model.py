import math, torch
from torch import nn

class LoRALinear(nn.Module):
    def __init__(self,in_f,out_f,rank=4,alpha=8.0,active_rank=None):
        super().__init__()
        self.base=nn.Linear(in_f,out_f)
        self.rank=rank;self.alpha=alpha;self.active_rank=active_rank or rank
        self.A=nn.Parameter(torch.empty(rank,in_f))
        self.B=nn.Parameter(torch.zeros(out_f,rank))
        nn.init.kaiming_uniform_(self.A,a=math.sqrt(5))
    def forward(self,x):
        base=self.base(x)
        mask=torch.zeros(self.rank,device=x.device,dtype=x.dtype)
        mask[:self.active_rank]=1
        A=self.A*mask[:,None]
        B=self.B*mask[None,:]
        return base + ((x@A.t())@B.t())*(self.alpha/self.rank)

class TinyEncoder(nn.Module):
    def __init__(self,vocab=512,d_model=64,nhead=4,layers=2,ff=128,classes=4,mode="full",rank=4,active_rank=None):
        super().__init__()
        self.emb=nn.Embedding(vocab,d_model,padding_idx=0)
        enc_layer=nn.TransformerEncoderLayer(d_model,nhead,ff,batch_first=True,dropout=0.0)
        self.encoder=nn.TransformerEncoder(enc_layer,layers)
        self.mode=mode
        if mode=="full":
            self.head=nn.Linear(d_model,classes)
        else:
            self.head=LoRALinear(d_model,classes,rank=rank,alpha=2*rank,active_rank=active_rank)
            for p in self.emb.parameters(): p.requires_grad=False
            for p in self.encoder.parameters(): p.requires_grad=False
            for p in self.head.base.parameters(): p.requires_grad=False
    def forward(self,x):
        mask=x.eq(0)
        h=self.encoder(self.emb(x),src_key_padding_mask=mask)
        valid=(~mask).float().unsqueeze(-1)
        pooled=(h*valid).sum(1)/valid.sum(1).clamp_min(1)
        return self.head(pooled)
    def trainable_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    def total_parameters(self):
        return sum(p.numel() for p in self.parameters())
