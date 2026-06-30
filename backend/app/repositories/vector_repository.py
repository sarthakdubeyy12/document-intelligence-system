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
