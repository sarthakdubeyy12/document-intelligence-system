"""Persistent ChromaDB vector store repository.

All ChromaDB-specific access lives here so the rest of the application can work
with the vector store without depending on ChromaDB directly.
"""

from functools import lru_cache
from pathlib import Path

import chromadb

# storage/ lives at the project root, alongside the backend/ package.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_DIR = PROJECT_ROOT / "storage" / "chroma"
COLLECTION_NAME = "documents"


@lru_cache
def get_client() -> chromadb.ClientAPI:
    """Return a cached persistent ChromaDB client.

    Data is written under ``storage/chroma`` so it survives application restarts.
    """
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


@lru_cache
def get_collection() -> chromadb.Collection:
    """Return the document collection, creating it on first use."""
    return get_client().get_or_create_collection(name=COLLECTION_NAME)


def get_existing_ids(ids: list[str]) -> set[str]:
    """Return the subset of the given ids that are already stored."""
    if not ids:
        return set()
    found = get_collection().get(ids=ids, include=[])
    return set(found["ids"])


def add_embeddings(
    ids: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
    documents: list[str],
) -> None:
    """Add embedding vectors with their documents and metadata to the collection."""
    get_collection().add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents,
    )


def query_similar(embedding: list[float], top_k: int) -> list[dict]:
    """Return up to ``top_k`` stored chunks most similar to ``embedding``.

    Each record holds the chunk's id, text, metadata, and raw vector distance,
    hiding ChromaDB's nested result shape from callers.
    """
    result = get_collection().query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    # A single query embedding yields one nested list per field.
    return [
        {"id": chunk_id, "text": text, "metadata": metadata, "distance": distance}
        for chunk_id, text, metadata, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]
