"""File upload endpoints."""

from fastapi import APIRouter, File, UploadFile

from app.services.document_pipeline import IngestionResult, ingest_documents
from app.utils.validators import validate_upload

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=IngestionResult)
async def upload_files(files: list[UploadFile] = File(...)) -> IngestionResult:
    """Validate the uploaded PDFs and run them through the ingestion pipeline."""
    validate_upload(files)
    return await ingest_documents(files)
