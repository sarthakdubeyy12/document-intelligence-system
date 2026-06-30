"""Storage of document embeddings into the vector store."""

from app.repositories import vector_repository
from app.services.chunking_service import Chunk
from app.services.embedding_service import EmbeddedChunk


def store_embeddings(embedded_chunks: list[EmbeddedChunk]) -> list[str]:
    """Store embedded chunks, skipping any whose chunk id is already stored.

    Returns the chunk ids that were newly stored.
    """
    if not embedded_chunks:
        return []

    ids = [item.chunk.chunk_id for item in embedded_chunks]
    existing = vector_repository.get_existing_ids(ids)
    new_items = [item for item in embedded_chunks if item.chunk.chunk_id not in existing]
    if not new_items:
        return []

    vector_repository.add_embeddings(
        ids=[item.chunk.chunk_id for item in new_items],
        embeddings=[item.embedding for item in new_items],
        metadatas=[_build_metadata(item.chunk) for item in new_items],
        documents=[item.chunk.text for item in new_items],
    )
    return [item.chunk.chunk_id for item in new_items]


def _build_metadata(chunk: Chunk) -> dict:
    """Build the metadata stored alongside a chunk's embedding."""
    return {
        "chunk_id": chunk.chunk_id,
        "filename": chunk.filename,
        "page_number": chunk.page_number,
    }
