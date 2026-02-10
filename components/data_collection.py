"""Step 1: Data collection - load raw text from a single PDF."""
from pathlib import Path
from pypdf import PdfReader


def load_pdf(path: str) -> dict:
    """
    Load a single PDF and extract text from all pages.
    Returns dict with 'text' (full raw text) and 'metadata' (page count, path).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError("File must be a PDF")

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})

    full_text = "\n\n".join(p["text"] for p in pages)
    return {
        "text": full_text,
        "pages": pages,
        "metadata": {
            "path": str(path),
            "num_pages": len(pages),
            "total_chars": len(full_text),
        },
    }
