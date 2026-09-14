from __future__ import annotations
import numpy as np

def make_frame(size=256, defect=False, seed=42, low_light=False, blur=False):
    rng=np.random.default_rng(seed)
    x=np.linspace(0,1,size)
    base=0.45 + 0.08*np.sin(2*np.pi*x)[None,:] + rng.normal(0,0.02,(size,size))
    img=np.clip(base,0,1)
    box=None
    if defect:
        h=w=max(10,size//12)
        y=int(rng.integers(size//4,3*size//4-h)); x0=int(rng.integers(size//4,3*size//4-w))
        img[y:y+h,x0:x0+w]=np.clip(img[y:y+h,x0:x0+w]+0.42,0,1); box=(x0,y,x0+w,y+h)
    if low_light: img*=0.20
    if blur:
        padded=np.pad(img,1,mode='edge'); out=np.zeros_like(img)
        for dy in range(3):
            for dx in range(3): out += padded[dy:dy+size,dx:dx+size]
        img=out/9.0
    return img.astype('float32'),box

def make_stream(n=40, defect_start=18, defect_end=24, seed=42):
    rows=[]
    for i in range(n):
        defect=defect_start<=i<=defect_end; frame,box=make_frame(defect=defect,seed=seed+i)
        rows.append({'frame_id':i,'image':frame,'defect':defect,'box':box})
    return rows
