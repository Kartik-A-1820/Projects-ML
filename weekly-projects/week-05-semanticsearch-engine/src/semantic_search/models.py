from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class SearchHit:
    doc_id: str
    title: str
    text: str
    score: float
    source: str
    metadata: dict = field(default_factory=dict)
