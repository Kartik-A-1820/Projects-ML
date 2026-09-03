from __future__ import annotations

from pathlib import Path

from .schema import ParsedDocument, TextBlock


class TextBackend:
    def convert(self, path: str) -> ParsedDocument:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        return ParsedDocument(path, [TextBlock(page=1, text=text)], {"backend": "text"})


class PyMuPDFBackend:
    def convert(self, path: str) -> ParsedDocument:
        import fitz
        doc = fitz.open(path)
        blocks = []
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text")
            if text.strip():
                blocks.append(TextBlock(page=page_number, text=text, kind="native_pdf_text"))
        return ParsedDocument(path, blocks, {"backend": "pymupdf"})


class DoclingBackend:
    def convert(self, path: str) -> ParsedDocument:
        from docling.document_converter import DocumentConverter
        result = DocumentConverter().convert(path)
        markdown = result.document.export_to_markdown()
        return ParsedDocument(source=path, blocks=[TextBlock(page=1, text=markdown, kind="docling_markdown")], metadata={"backend": "docling"})


def get_backend(name: str):
    normalized = name.lower().strip()
    if normalized == "text":
        return TextBackend()
    if normalized == "pymupdf":
        return PyMuPDFBackend()
    if normalized == "docling":
        return DoclingBackend()
    raise ValueError(f"unknown backend: {name}")
