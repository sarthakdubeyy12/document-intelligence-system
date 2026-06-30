"""Semantic retrieval of document chunks for user queries."""

from dataclasses import dataclass

from app.repositories import vector_repository
from app.services.embedding_service import embed_query

DEFAULT_TOP_K = 5


@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector store with its similarity score."""

    chunk_id: str
    filename: str
    page_number: int
    text: str
    score: float


def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[RetrievedChunk]:
    """Retrieve the ``top_k`` stored chunks most semantically similar to ``query``."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    if not query.strip():
        return []

    embedding = embed_query(query)
    records = vector_repository.query_similar(embedding, top_k)
    return [_to_retrieved_chunk(record) for record in records]


def _to_retrieved_chunk(record: dict) -> RetrievedChunk:
    """Convert a vector store record into a retrieved chunk with a similarity score."""
    metadata = record["metadata"]
    return RetrievedChunk(
        chunk_id=record["id"],
        filename=metadata["filename"],
        page_number=metadata["page_number"],
        text=record["text"],
        score=_to_similarity(record["distance"]),
    )


def _to_similarity(distance: float) -> float:
    """Convert ChromaDB's squared-L2 distance into cosine similarity.

    Embeddings are L2-normalized, so for a squared-L2 distance ``d`` the cosine
    similarity is ``1 - d / 2`` (higher means more similar).
    """
    return 1.0 - distance / 2.0
