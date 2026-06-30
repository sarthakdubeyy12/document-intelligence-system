"""Embedding model setup: load the configured model once and share it."""

from dataclasses import dataclass
from functools import lru_cache

from transformers import (
    AutoModel,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

from app.core.config import get_settings


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
