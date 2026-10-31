"""CPU-friendly dynamics-masked reconstruction and frozen linear probing."""
import copy
import numpy as np
import torch
from torch import nn
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class Encoder(nn.Module):
    def __init__(self,width=32):
        super().__init__()
        self.net=nn.Sequential(nn.Conv1d(9,width,7,padding=3),nn.BatchNorm1d(width),nn.GELU(),nn.Conv1d(width,width,5,padding=2),nn.GELU())
    def forward(self,x):return self.net(x.transpose(1,2))

class MaskedReconstructor(nn.Module):
    def __init__(self,width=32):
        super().__init__();self.encoder=Encoder(width);self.head=nn.Conv1d(width,9,1)
    def forward(self,x):return self.head(self.encoder(x)).transpose(1,2)

def masked_positions(x,generator,rate=.20,dynamic=True):
    """Mask 20% of time points, with probability influenced by within-window jerk."""
    b,t,c=x.shape
    jerk=torch.zeros((b,t),device=x.device)
    jerk[:,1:]=torch.linalg.vector_norm(x[:,1:,:3]-x[:,:-1,:3],dim=2)
    if dynamic:
        prob=(jerk+jerk.mean(dim=1,keepdim=True)+1e-4)
        prob=prob/prob.sum(dim=1,keepdim=True)
    else: prob=torch.ones((b,t),device=x.device)/t
    count=max(1,int(rate*t))
    selected=torch.multinomial(prob,count,replacement=False,generator=generator)
    mask=torch.zeros((b,t,1),device=x.device,dtype=torch.bool)
    mask.scatter_(1,selected.unsqueeze(-1),True)
    return mask.expand(-1,-1,c)

def pretrain(x,seed=42,epochs=5,batch_size=128,device='cpu',dynamic=True):
    torch.manual_seed(seed);torch.set_num_threads(min(4,torch.get_num_threads()))
    model=MaskedReconstructor().to(device); opt=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=.01)
    x=torch.from_numpy(np.asarray(x,dtype=np.float32)); rng=np.random.default_rng(seed)
    gen=torch.Generator(device=device).manual_seed(seed)
    losses=[]
    for epoch in range(epochs):
        model.train();order=rng.permutation(len(x));batch_losses=[]
        for ids in np.array_split(order,max(1,int(np.ceil(len(order)/batch_size)))):
            batch=x[ids].to(device);mask=masked_positions(batch,gen,dynamic=dynamic)
            corrupted=batch.masked_fill(mask,0)
            pred=model(corrupted)
            loss=(pred[mask]-batch[mask]).square().mean()
            opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1.0);opt.step()
            batch_losses.append(float(loss.item()))
        losses.append(float(np.mean(batch_losses)))
    model.eval()
    return model,losses

@torch.no_grad()
def embed(encoder,x,device='cpu',batch_size=256):
    encoder=encoder.to(device).eval();vectors=[]
    for part in np.array_split(np.arange(len(x)),max(1,int(np.ceil(len(x)/batch_size)))):
        batch=torch.from_numpy(np.asarray(x[part],dtype=np.float32)).to(device)
        vectors.append(encoder(batch).mean(dim=2).cpu().numpy())
    return np.concatenate(vectors).astype(np.float32)

def fit_probe(z,y,idx,seed=42):
    clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=400,C=1.0,random_state=seed))
    clf.fit(z[idx],y[idx]);return clf

def stratified_budget(y,idx,fraction,seed=42):
    rng=np.random.default_rng(seed);indices=[]
    for cls in np.unique(y[idx]):
        members=idx[y[idx]==cls]
        indices.extend(rng.choice(members,size=max(2,int(np.ceil(len(members)*fraction))),replace=False))
    return np.array(sorted(indices),dtype=int)
