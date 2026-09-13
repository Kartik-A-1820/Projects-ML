from __future__ import annotations
import numpy as np
from PIL import Image

def _gray(arr):
    if arr.ndim==2:return arr.astype(np.float32)/255.0
    rgb=arr[...,:3].astype(np.float32)/255.0
    return .299*rgb[...,0]+.587*rgb[...,1]+.114*rgb[...,2]

def embed_image(image: Image.Image) -> np.ndarray:
    arr=np.asarray(image.convert("RGB").resize((96,96)),dtype=np.float32)/255.0
    # color moments
    means=arr.mean(axis=(0,1)); stds=arr.std(axis=(0,1))
    g=_gray((arr*255).astype(np.uint8))
    gx=np.abs(np.diff(g,axis=1,prepend=g[:,:1]))
    gy=np.abs(np.diff(g,axis=0,prepend=g[:1,:]))
    mag=np.sqrt(gx*gx+gy*gy)
    edge_hist,_=np.histogram(mag,bins=8,range=(0,1),density=True)
    # local contrast quadrants
    h,w=g.shape
    quads=[
        g[:h//2,:w//2],g[:h//2,w//2:],
        g[h//2:,:w//2],g[h//2:,w//2:]
    ]
    contrast=np.array([q.std() for q in quads],dtype=np.float32)
    v=np.concatenate([means,stds,edge_hist.astype(np.float32),contrast])
    n=np.linalg.norm(v)
    return v if n==0 else v/n

def cosine(a,b):
    a=np.asarray(a,dtype=np.float32);b=np.asarray(b,dtype=np.float32)
    den=np.linalg.norm(a)*np.linalg.norm(b)
    return 0.0 if den==0 else float(np.dot(a,b)/den)
