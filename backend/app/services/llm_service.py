"""Construction of the prompt sent to the LLM (prompt building only, no inference)."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.services.retrieval_service import RetrievedChunk

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.txt"
QA_PROMPT_FILE = PROMPTS_DIR / "qa_prompt.txt"


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
