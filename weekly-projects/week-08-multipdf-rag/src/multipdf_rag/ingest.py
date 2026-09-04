from __future__ import annotations
from pathlib import Path
import re
from .schema import Chunk

def split_pages_from_text(text:str):
    parts=re.split(r'\[PAGE\s+(\d+)\]',text)
    if len(parts)==1: return [(1,text)]
    pages=[]
    for i in range(1,len(parts),2): pages.append((int(parts[i]),parts[i+1].strip()))
    return pages

def chunk_page(text:str,source:str,page:int,size:int=120,overlap:int=25)->list[Chunk]:
    words=text.split(); step=max(1,size-overlap); out=[]
    for start in range(0,len(words),step):
        part=words[start:start+size]
        if not part: break
        out.append(Chunk(f'{Path(source).name}:p{page}:c{start//step}',Path(source).name,page,' '.join(part)))
        if start+size>=len(words): break
    return out

def ingest_text(path:str,size:int=120,overlap:int=25)->list[Chunk]:
    text=Path(path).read_text(encoding='utf-8',errors='ignore'); out=[]
    for page,body in split_pages_from_text(text): out.extend(chunk_page(body,path,page,size,overlap))
    return out

def ingest_pdf(path:str,size:int=120,overlap:int=25)->list[Chunk]:
    import fitz
    doc=fitz.open(path); out=[]
    for i,page in enumerate(doc,start=1): out.extend(chunk_page(page.get_text('text'),path,i,size,overlap))
    return out
