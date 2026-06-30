"""Reusable validation helpers for file uploads."""

from fastapi import HTTPException, UploadFile, status

MIN_FILES = 1
MAX_FILES = 50
PDF_MIME_TYPE = "application/pdf"
PDF_EXTENSION = ".pdf"


def validate_upload(files: list[UploadFile]) -> None:
    """Validate a batch of uploaded files, raising HTTPException on the first problem.

    Runs all checks before any file is persisted, so an invalid request fails fast.
    """
    _validate_file_count(files)
    _validate_no_duplicate_filenames(files)
    for file in files:
        _validate_pdf_file(file)


def _validate_file_count(files: list[UploadFile]) -> None:
    """Ensure the request carries between MIN_FILES and MAX_FILES files."""
    if not MIN_FILES <= len(files) <= MAX_FILES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Number of uploaded files must be between {MIN_FILES} and {MAX_FILES}.",
        )


def _validate_no_duplicate_filenames(files: list[UploadFile]) -> None:
    """Reject the request if two files share the same filename."""
    filenames = [file.filename or "" for file in files]
    duplicates = sorted({name for name in filenames if filenames.count(name) > 1})
    if duplicates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Duplicate filenames in request: {', '.join(duplicates)}.",
        )


def _validate_pdf_file(file: UploadFile) -> None:
    """Validate a single file's extension, MIME type, and that it is not empty."""
    filename = file.filename or ""
    if not filename.lower().endswith(PDF_EXTENSION):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File '{filename}' must have a {PDF_EXTENSION} extension.",
        )
    if file.content_type != PDF_MIME_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File '{filename}' must be of type {PDF_MIME_TYPE}.",
        )
    if file.size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File '{filename}' is empty.",
        )
