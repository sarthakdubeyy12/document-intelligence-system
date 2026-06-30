"""Splitting extracted document text into retrieval-ready chunks."""

from dataclasses import dataclass

from app.services.document_pipeline import ProcessedDocument
from app.utils.text_utils import normalize_whitespace, split_text

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


@dataclass
class Chunk:
    """A retrieval-ready text chunk with its source metadata."""

    chunk_id: str
    filename: str
    page_number: int
    text: str


def chunk_documents(
    documents: list[ProcessedDocument],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:
    """Split each extracted document into overlapping chunks, preserving metadata."""
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(_chunk_document(document, chunk_size, chunk_overlap))
    return chunks


def _chunk_document(
    document: ProcessedDocument, chunk_size: int, chunk_overlap: int
) -> list[Chunk]:
    """Split a single document page by page so chunks retain their page number."""
    chunks: list[Chunk] = []
    for page in document.document.pages:
        pieces = [
            normalize_whitespace(piece)
            for piece in split_text(page.text, chunk_size, chunk_overlap)
        ]
        for index, text in enumerate(piece for piece in pieces if piece):
            chunks.append(
                Chunk(
                    chunk_id=f"{document.filename}-p{page.page_number}-{index}",
                    filename=document.filename,
                    page_number=page.page_number,
                    text=text,
                )
            )
    return chunks
