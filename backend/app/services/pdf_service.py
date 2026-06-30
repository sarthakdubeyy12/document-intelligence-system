"""Business logic for handling uploaded PDF files."""

from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader
from pypdf.errors import FileNotDecryptedError, PyPdfError

# storage/ lives at the project root, alongside the backend/ package.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PROJECT_ROOT / "storage" / "uploads"


@dataclass
class PageContent:
    """Text extracted from a single PDF page."""

    page_number: int
    text: str


@dataclass
class ExtractedDocument:
    """Structured text content extracted from a PDF, ordered by page."""

    pages: list[PageContent]


class PdfExtractionError(Exception):
    """Base error raised when a PDF's text cannot be extracted."""


class EncryptedPdfError(PdfExtractionError):
    """Raised when a PDF is encrypted and cannot be read."""


class CorruptedPdfError(PdfExtractionError):
    """Raised when a PDF is corrupted or otherwise unreadable."""


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


def extract_text(file_path: Path) -> ExtractedDocument:
    """Extract text from a PDF file page by page, preserving page order.

    Pages without extractable text yield empty strings, so an empty PDF returns
    an ExtractedDocument with blank page text rather than raising.

    Raises:
        EncryptedPdfError: the PDF is encrypted and cannot be read.
        CorruptedPdfError: the PDF is corrupted or otherwise unreadable.
    """
    try:
        reader = PdfReader(str(file_path))
        pages = [
            PageContent(page_number=number, text=(page.extract_text() or "").strip())
            for number, page in enumerate(reader.pages, start=1)
        ]
    except FileNotDecryptedError as exc:
        raise EncryptedPdfError(
            f"Cannot extract text from encrypted PDF '{file_path.name}'."
        ) from exc
    except PyPdfError as exc:
        raise CorruptedPdfError(
            f"Could not read PDF '{file_path.name}'; it may be corrupted."
        ) from exc

    return ExtractedDocument(pages=pages)
