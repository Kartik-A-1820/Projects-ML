"""Small BatchEnsemble-inspired classifier; NOT a reproduction of official TabM."""
import copy
import numpy as np


def fit_tabm_lite(x_train,y_train,x_val,y_val,seed=42,epochs=18,batch=512,k=4):
    import torch
    from torch import nn
    from sklearn.metrics import average_precision_score
    torch.manual_seed(seed)
    torch.set_num_threads(min(4,torch.get_num_threads()))
    device='cuda' if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory >= 3e9 else 'cpu'
    class SharedEnsemble(nn.Module):
        def __init__(self,d):
            super().__init__()
            self.r=nn.Parameter(torch.ones(k,d)+torch.randn(k,d)*0.05)
            self.shared=nn.Sequential(nn.Linear(d,48),nn.ReLU(),nn.Dropout(.08),nn.Linear(48,24),nn.ReLU())
            self.s=nn.Parameter(torch.ones(k,24))
            self.head=nn.Parameter(torch.randn(k,24)*.03)
            self.bias=nn.Parameter(torch.zeros(k))
        def forward(self,x):
            b,n=x.shape
            h=self.shared((x[:,None,:]*self.r[None,:,:]).reshape(-1,n)).reshape(b,k,24)
            return ((h*self.s[None,:,:])*self.head[None,:,:]).sum(-1)+self.bias
    model=SharedEnsemble(x_train.shape[1]).to(device)
    opt=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=.0003)
    xt=torch.tensor(x_train,dtype=torch.float32);yt=torch.tensor(y_train,dtype=torch.float32)
    xv=torch.tensor(x_val,dtype=torch.float32,device=device)
    best=-1;state=None;patience=0
    for epoch in range(epochs):
        model.train()
        rng=torch.Generator().manual_seed(seed+epoch)
        for ix in torch.randperm(len(xt),generator=rng).split(batch):
            xx=xt[ix].to(device);yy=yt[ix].to(device)
            opt.zero_grad(set_to_none=True)
            logits=model(xx)
            # Member-wise loss, not loss of averaged probability.
            loss=nn.functional.binary_cross_entropy_with_logits(logits,yy[:,None].expand_as(logits))
            loss.backward();opt.step()
        model.eval()
        with torch.no_grad():
            pv=torch.sigmoid(model(xv)).mean(dim=1).cpu().numpy()
        metric=average_precision_score(y_val,pv)
        if metric>best+1e-5:
            best=metric;state=copy.deepcopy(model.state_dict());patience=0
        else:
            patience+=1
            if patience>=4: break
    model.load_state_dict(state)
    return model,{'device':device,'best_validation_pr_auc':float(best),'epochs_ran':epoch+1,'ensemble_members':k}


def tabm_predict(model,x):
    import torch
    device=next(model.parameters()).device
    model.eval();result=[]
    with torch.no_grad():
        for chunk in np.array_split(np.asarray(x,dtype=np.float32),max(1,int(np.ceil(len(x)/2048)))):
            t=torch.as_tensor(chunk,device=device)
            result.append(torch.sigmoid(model(t)).mean(1).cpu().numpy())
    return np.concatenate(result)