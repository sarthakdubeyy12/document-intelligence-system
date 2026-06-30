"""Orchestration of the document question answering flow.

Coordinates the existing services: retrieve relevant chunks, generate a grounded
answer, and build citations. Each step's logic stays in its own service.
"""

from app.schemas.chat import ChatResponse
from app.services.citation_service import build_citations
from app.services.llm_service import build_prompt, generate_answer
from app.services.retrieval_service import retrieve

NO_CONTEXT_MESSAGE = (
    "I couldn't find any relevant information in the uploaded documents "
    "to answer that question."
)


def answer_question(question: str) -> ChatResponse:
    """Answer a question from the stored documents, with grounding citations.

    When no relevant chunks are retrieved, returns a clear message and no
    citations without calling the LLM.
    """
    chunks = retrieve(question)
    if not chunks:
        return ChatResponse(answer=NO_CONTEXT_MESSAGE, citations=[])

    answer = generate_answer(build_prompt(question, chunks))
    return ChatResponse(answer=answer, citations=build_citations(chunks))
