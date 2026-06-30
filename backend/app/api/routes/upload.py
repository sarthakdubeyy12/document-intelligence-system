"""File upload endpoints."""

from fastapi import APIRouter, File, UploadFile

from app.schemas.upload import UploadResponse
from app.services import pdf_service

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    """Accept one or more uploaded files and delegate persistence to the service layer."""
    filenames = await pdf_service.save_uploads(files)
    return UploadResponse(filenames=filenames)
