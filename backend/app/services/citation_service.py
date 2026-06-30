"""Building answer citations from the retrieved chunks used to answer a question."""

from app.schemas.citation import Citation
from app.services.retrieval_service import RetrievedChunk

DEFAULT_SNIPPET_LENGTH = 200


def build_citations(chunks: list[RetrievedChunk]) -> list[Citation]:
    """Build one citation per retrieved chunk, reusing its source metadata."""
    return [_to_citation(chunk) for chunk in chunks]


def _to_citation(chunk: RetrievedChunk) -> Citation:
    """Map a retrieved chunk to a citation with a quoted snippet of its text."""
    return Citation(
        chunk_id=chunk.chunk_id,
        filename=chunk.filename,
        page_number=chunk.page_number,
        snippet=_snippet(chunk.text),
    )


def _snippet(text: str, max_length: int = DEFAULT_SNIPPET_LENGTH) -> str:
    """Return a short quoted snippet, truncated with an ellipsis when too long."""
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"
