"""Lightweight orchestration for document text extraction."""

from dataclasses import dataclass
from pathlib import Path

from app.services.pdf_service import ExtractedDocument, extract_text


@dataclass
class ProcessedDocument:
    """Extracted text content paired with its source filename."""

    filename: str
    document: ExtractedDocument


def process_documents(file_paths: list[Path]) -> list[ProcessedDocument]:
    """Extract text from each PDF, returning structured results for chunking.

    Extraction is delegated entirely to the PDF service; this layer only
    coordinates the call across documents and records each source filename.
    """
    return [
        ProcessedDocument(filename=path.name, document=extract_text(path))
        for path in file_paths
    ]
