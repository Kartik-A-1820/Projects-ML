from pathlib import Path
import random
from PIL import Image,ImageDraw,ImageFilter

def make_image(label,seed,size=128):
    rng=random.Random(seed)
    base=rng.randint(145,185)
    img=Image.new("RGB",(size,size),(base,base+2,base+4))
    d=ImageDraw.Draw(img)
    # mild texture
    for _ in range(70):
        x=rng.randrange(size);y=rng.randrange(size);c=base+rng.randint(-12,12)
        d.point((x,y),fill=(c,c,c))
    if label=="scratch":
        y=rng.randint(35,90)
        d.line((15,y,112,y+rng.randint(-12,12)),fill=(45,45,45),width=3)
    elif label=="dent":
        x=rng.randint(45,80);y=rng.randint(45,80);r=rng.randint(15,24)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(105,110,118))
        img=img.filter(ImageFilter.GaussianBlur(radius=2.3))
    return img

def generate_dataset(root="data/generated",per_class=8):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    rows=[];i=0
    for label in ["normal","scratch","dent"]:
        for j in range(per_class):
            i+=1;path=root/f"{label}_{j:02d}.png"
            make_image(label,1000+i).save(path)
            rows.append({
                "id":f"x{i:03d}","path":str(path),"label":label,
                "machine":"press-A" if j%2==0 else "press-B",
                "illumination":"bright" if j%3 else "dim"
            })
    return rows
