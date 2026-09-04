from dataclasses import dataclass,field
@dataclass(frozen=True)
class Chunk:
    chunk_id:str
    source:str
    page:int
    text:str
    metadata:dict=field(default_factory=dict)
@dataclass(frozen=True)
class Hit:
    chunk:Chunk
    score:float
    source:str
