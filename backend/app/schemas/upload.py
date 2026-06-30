"""Schemas for the upload endpoint."""

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Response returned after files are uploaded."""

    filenames: list[str]
