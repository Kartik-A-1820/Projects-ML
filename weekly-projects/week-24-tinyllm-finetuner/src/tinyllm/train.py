import time,torch
from torch.utils.data import DataLoader

def resolve_device(v):
    if v=="auto":return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(v)

def fit(model,ds,epochs=8,batch_size=8,lr=.01,device="cpu",seed=42):
    torch.manual_seed(seed);m=model.to(device);m.train()
    opt=torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],lr=lr)
    lossfn=torch.nn.CrossEntropyLoss();loader=DataLoader(ds,batch_size=batch_size,shuffle=True)
    start=time.perf_counter()
    for _ in range(epochs):
        for x,y in loader:
            x,y=x.to(device),y.to(device);opt.zero_grad(set_to_none=True)
            loss=lossfn(m(x),y);loss.backward();opt.step()
    return m,time.perf_counter()-start

@torch.inference_mode()
def accuracy(model,ds,device="cpu"):
    model.eval();loader=DataLoader(ds,batch_size=32);c=t=0
    for x,y in loader:
        x,y=x.to(device),y.to(device);p=model(x).argmax(-1)
        c+=int((p==y).sum());t+=int(y.numel())
    return c/max(1,t)
