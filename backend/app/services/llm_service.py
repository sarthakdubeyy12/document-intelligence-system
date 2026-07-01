"""Prompt construction and grounded answer generation for the LLM."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from groq import APIError, Groq

from app.core.config import get_settings
from app.services.retrieval_service import RetrievedChunk

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.txt"
QA_PROMPT_FILE = PROMPTS_DIR / "qa_prompt.txt"
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(ENV_FILE)

LLM_MAX_TOKENS = 2048


@dataclass
class Prompt:
    """A structured prompt with a system instruction and a user message."""

    system: str
    user: str


def build_prompt(query: str, chunks: list[RetrievedChunk]) -> Prompt:
    """Build the QA prompt from the retrieved context and the user's question."""
    context = _format_context(chunks)
    user_message = _load_template(QA_PROMPT_FILE).format(context=context, question=query)
    return Prompt(system=_load_template(SYSTEM_PROMPT_FILE), user=user_message)


def _format_context(chunks: list[RetrievedChunk]) -> str:
    """Render retrieved chunks into one context block, each labeled by its source."""
    blocks = [
        f"[Source: {chunk.filename}, page {chunk.page_number}]\n{chunk.text}"
        for chunk in chunks
    ]
    return "\n\n".join(blocks)


@lru_cache
def _load_template(path: Path) -> str:
    """Load and cache a prompt template from disk."""
    return path.read_text(encoding="utf-8").strip()


def generate_answer(prompt: Prompt) -> str:
    """Send the prepared prompt to the configured LLM and return only the answer text.

    The prompt instructs the model to answer solely from the provided context and to
    state when the information is unavailable, so insufficient context is handled by
    the model rather than special-cased here.
    """
    try:
        completion = _get_client().chat.completions.create(
            model=get_settings().llm_model,
            max_tokens=LLM_MAX_TOKENS,
            messages=[
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
        )
    except APIError as exc:
        raise RuntimeError(f"Language model request failed: {exc}") from exc
    return (completion.choices[0].message.content or "").strip()


@lru_cache
def _get_client() -> Groq:
    """Return a cached Groq client, reading the API key from the environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Groq API key is not configured. Set GROQ_API_KEY in backend/.env."
        )
    return Groq(api_key=api_key)
