"""File upload endpoints."""

from fastapi import APIRouter, File, UploadFile

from app.schemas.upload import UploadResponse
from app.services import pdf_service
from app.utils.validators import validate_upload

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    """Validate the uploaded PDF files and delegate persistence to the service layer."""
    validate_upload(files)
    filenames = await pdf_service.save_uploads(files)
    return UploadResponse(filenames=filenames)
