"""Business logic for handling uploaded PDF files."""

from pathlib import Path

from fastapi import UploadFile

# storage/ lives at the project root, alongside the backend/ package.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PROJECT_ROOT / "storage" / "uploads"


async def save_uploads(files: list[UploadFile]) -> list[str]:
    """Persist uploaded files to the uploads directory and return their filenames."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    for file in files:
        # Reduce the client-supplied name to its final component so it cannot
        # escape the uploads directory via path traversal or absolute paths.
        filename = Path(file.filename or "").name
        if not filename:
            continue
        content = await file.read()
        (UPLOAD_DIR / filename).write_bytes(content)
        saved.append(filename)
    return saved
