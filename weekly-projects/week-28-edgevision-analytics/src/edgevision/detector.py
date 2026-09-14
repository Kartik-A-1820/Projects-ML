from __future__ import annotations
import numpy as np

def tiles(image,tile_size=64,stride=64):
    h,w=image.shape
    for y in range(0,max(1,h-tile_size+1),stride):
        for x in range(0,max(1,w-tile_size+1),stride):
            yield x,y,image[y:y+tile_size,x:x+tile_size]

def detect(image,tile_size=64,stride=64,z_threshold=3.5):
    global_mean=float(image.mean()); global_std=max(float(image.std()),1e-6); hits=[]
    for x,y,tile in tiles(image,tile_size,stride):
        score=(float(tile.max())-global_mean)/global_std
        if score>=z_threshold:
            conf=float(min(0.99,0.45+(score-z_threshold)*0.12))
            hits.append({'bbox':[x,y,x+tile.shape[1],y+tile.shape[0]],'score':float(score),'confidence':conf})
    hits.sort(key=lambda h:-h['score'])
    return hits
