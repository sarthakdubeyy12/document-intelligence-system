"""End-to-end document ingestion pipeline.

Coordinates the existing services in order: upload -> extract -> chunk -> embed
-> store. This layer only orchestrates the workflow and calls the existing
services; each service remains responsible for its own logic.
"""

from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile

from app.services.chunking_service import ProcessedDocument, chunk_documents
from app.services.embedding_service import embed_chunks
from app.services.pdf_service import (
    UPLOAD_DIR,
    PdfExtractionError,
    extract_text,
    save_uploads,
)
from app.services.vector_store_service import store_embeddings


@dataclass
class FailedDocument:
    """A document that could not be extracted, with the reason why."""

    filename: str
    error: str


@dataclass
class IngestionResult:
    """Summary of an ingestion run returned to the caller."""

    ingested: list[str]
    failed: list[FailedDocument]
    chunk_count: int
    stored_count: int


async def ingest_documents(files: list[UploadFile]) -> IngestionResult:
    """Run the full ingestion workflow and report what was ingested and what failed.

    Documents that cannot be extracted (e.g. encrypted or corrupted PDFs) are
    skipped and reported, so a single bad file does not abort the whole batch.
    """
    filenames = await save_uploads(files)
    processed, failed = _extract_documents(filenames)

    chunks = chunk_documents(processed)
    stored = store_embeddings(embed_chunks(chunks))

    return IngestionResult(
        ingested=[document.filename for document in processed],
        failed=failed,
        chunk_count=len(chunks),
        stored_count=len(stored),
    )


def _extract_documents(
    filenames: list[str],
) -> tuple[list[ProcessedDocument], list[FailedDocument]]:
    """Extract each saved file, separating successes from extraction failures."""
    processed: list[ProcessedDocument] = []
    failed: list[FailedDocument] = []
    for filename in filenames:
        try:
            document = extract_text(UPLOAD_DIR / filename)
        except PdfExtractionError as exc:
            failed.append(FailedDocument(filename=filename, error=str(exc)))
            continue
        processed.append(ProcessedDocument(filename=filename, document=document))
    return processed, failed


def process_documents(file_paths: list[Path]) -> list[ProcessedDocument]:
    """Extract text from each PDF, returning structured results for chunking.

    Fail-fast helper for extracting from known-good paths; ``ingest_documents``
    handles per-document failures for the full upload-driven workflow.
    """
    return [
        ProcessedDocument(filename=path.name, document=extract_text(path))
        for path in file_paths
    ]
