from dataclasses import dataclass, field

@dataclass(frozen=True)
class VideoEvent:
    event_id: str
    start: float
    end: float
    transcript: str = ""
    ocr: str = ""
    visual: str = ""
    links: list[str] = field(default_factory=list)

    def modality_text(self, modality: str) -> str:
        return str(getattr(self, modality, ""))

@dataclass(frozen=True)
class EvidenceHit:
    event_id: str
    start: float
    end: float
    score: float
    reasons: tuple[str, ...]
    transcript: str
    ocr: str
    visual: str
