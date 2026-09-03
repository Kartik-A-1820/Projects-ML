from dataclasses import dataclass, field


@dataclass
class TextBlock:
    page: int
    text: str
    kind: str = "text"
    bbox: tuple[float, float, float, float] | None = None


@dataclass
class ParsedDocument:
    source: str
    blocks: list[TextBlock]
    metadata: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n".join(block.text for block in self.blocks if block.text.strip())
