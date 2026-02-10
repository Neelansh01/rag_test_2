"""Step 3: Chunking - split cleaned text for retrieval (multiple methods)."""
from __future__ import annotations
import re
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """
    Fixed-size: character-based sliding window. Each chunk is a dict with 'text' and 'index'.
    """
    if not text or not text.strip():
        return []
    chunks = []
    start = 0
    index = 0
    while start < len(text):
        end = start + chunk_size
        slice_text = text[start:end]
        if slice_text.strip():
            chunks.append({"index": index, "text": slice_text.strip()})
            index += 1
        start = end - overlap
        if start >= len(text):
            break
    return chunks


def _split_sentences(text: str) -> list[str]:
    """Split on . ! ? and trim."""
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def chunk_by_sentences(
    text: str,
    max_chars: int = 500,
    overlap_sentences: int = 0,
) -> list[dict]:
    """
    Sentence-based: group sentences into chunks of ~max_chars. Overlap = number of
    sentences to repeat at the start of the next chunk.
    """
    if not text or not text.strip():
        return []
    sentences = _split_sentences(text)
    if not sentences:
        return chunk_text(text, chunk_size=max_chars, overlap=0)
    chunks = []
    index = 0
    i = 0
    while i < len(sentences):
        current = []
        current_len = 0
        while i < len(sentences) and current_len + len(sentences[i]) + 1 <= max_chars:
            current.append(sentences[i])
            current_len += len(sentences[i]) + 1
            i += 1
        if current:
            chunk_text_str = " ".join(current)
            chunks.append({"index": index, "text": chunk_text_str})
            index += 1
        if overlap_sentences > 0 and current:
            i = max(0, i - overlap_sentences)
    return chunks


def chunk_by_paragraphs(text: str, max_chars: int = 500) -> list[dict]:
    """
    Paragraph-based: split on double newline, then merge small paragraphs or split
    large ones so each chunk is around max_chars.
    """
    if not text or not text.strip():
        return []
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paras:
        return chunk_text(text, chunk_size=max_chars, overlap=0)
    chunks = []
    index = 0
    current = []
    current_len = 0
    for p in paras:
        if current_len + len(p) + 2 <= max_chars and current:
            current.append(p)
            current_len += len(p) + 2
        else:
            if current:
                chunks.append({"index": index, "text": "\n\n".join(current)})
                index += 1
            if len(p) > max_chars:
                for sub in chunk_text(p, chunk_size=max_chars, overlap=0):
                    sub["index"] = index
                    chunks.append(sub)
                    index += 1
                current = []
                current_len = 0
            else:
                current = [p]
                current_len = len(p)
    if current:
        chunks.append({"index": index, "text": "\n\n".join(current)})
    return chunks


# Method keys for UI
CHUNKING_METHODS = {
    "fixed": ("Fixed size (character)", chunk_text),
    "sentence": ("Sentence-based", chunk_by_sentences),
    "paragraph": ("Paragraph-based", chunk_by_paragraphs),
}


def chunk_text_with_method(
    text: str,
    method: str = "fixed",
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[dict]:
    """
    Run the selected chunking method. Returns list of {index, text}.
    method: "fixed" | "sentence" | "paragraph"
    """
    if method == "fixed":
        return chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    if method == "sentence":
        return chunk_by_sentences(text, max_chars=chunk_size, overlap_sentences=min(1, overlap // 50))
    if method == "paragraph":
        return chunk_by_paragraphs(text, max_chars=chunk_size)
    return chunk_text(text, chunk_size=chunk_size, overlap=overlap)
