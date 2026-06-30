"""Schema for answer citations."""

from pydantic import BaseModel


class Citation(BaseModel):
    """A reference to the document chunk an answer was grounded in."""

    chunk_id: str
    filename: str
    page_number: int
    snippet: str
