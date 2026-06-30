"""Schemas for the chat (document question answering) endpoint."""

from pydantic import BaseModel, Field

from app.schemas.citation import Citation


class ChatRequest(BaseModel):
    """A user question about the uploaded documents."""

    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    """A grounded answer with the citations it was based on."""

    answer: str
    citations: list[Citation]
