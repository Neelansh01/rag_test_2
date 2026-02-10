"""Step 3: Chunking - split cleaned text into overlapping chunks for retrieval."""
from __future__ import annotations
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """
    Split text into overlapping chunks. Each chunk is a dict with 'text' and 'index'.
    Simple character-based sliding window (no sentence boundary logic for simplicity).
    """
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    index = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text_slice = text[start:end]
        if chunk_text_slice.strip():
            chunks.append({"index": index, "text": chunk_text_slice.strip()})
            index += 1
        start = end - overlap
        if start >= len(text):
            break

    return chunks
