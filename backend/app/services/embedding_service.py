"""Embedding model setup and batched embedding generation."""

from dataclasses import dataclass
from functools import lru_cache

import torch
from transformers import (
    AutoModel,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from app.core.config import get_settings
from app.services.chunking_service import Chunk

DEFAULT_BATCH_SIZE = 32


@dataclass
class EmbeddingModel:
    """A loaded embedding model with its tokenizer, ready to produce embeddings."""

    name: str
    tokenizer: PreTrainedTokenizerBase
    model: PreTrainedModel


@lru_cache
def get_embedding_model() -> EmbeddingModel:
    """Return the shared embedding model, loading it once on first use.

    Caching keeps the (potentially heavy) model in memory for the process
    lifetime, so callers can request it without managing initialization.
    """
    model_name = get_settings().embedding_model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()
    return EmbeddingModel(name=model_name, tokenizer=tokenizer, model=model)


@dataclass
class EmbeddedChunk:
    """A chunk paired with its embedding vector, ready for vector storage."""

    chunk: Chunk
    embedding: list[float]


def embed_chunks(
    chunks: list[Chunk], batch_size: int = DEFAULT_BATCH_SIZE
) -> list[EmbeddedChunk]:
    """Generate embeddings for chunks in batches, keeping each chunk's metadata.

    Returns an empty list when given no chunks.
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    if not chunks:
        return []

    model = get_embedding_model()
    embedded: list[EmbeddedChunk] = []
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        vectors = _embed_texts([chunk.text for chunk in batch], model)
        embedded.extend(
            EmbeddedChunk(chunk=chunk, embedding=vector)
            for chunk, vector in zip(batch, vectors)
        )
    return embedded


def embed_query(text: str) -> list[float]:
    """Generate an embedding for a single query string."""
    return _embed_texts([text], get_embedding_model())[0]


def _embed_texts(texts: list[str], model: EmbeddingModel) -> list[list[float]]:
    """Embed a batch of texts into normalized, mean-pooled sentence vectors."""
    tokens = model.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        output = model.model(**tokens)
    embeddings = _mean_pool(output.last_hidden_state, tokens["attention_mask"])
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings.tolist()


def _mean_pool(
    last_hidden_state: torch.Tensor, attention_mask: torch.Tensor
) -> torch.Tensor:
    """Average token embeddings, using the attention mask to ignore padding."""
    mask = attention_mask.unsqueeze(-1).float()
    summed = (last_hidden_state * mask).sum(dim=1)
    token_counts = mask.sum(dim=1).clamp(min=1e-9)
    return summed / token_counts
