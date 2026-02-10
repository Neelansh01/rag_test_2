"""Step 2: Data cleaning - normalize and clean raw text."""
import re


def clean_text(raw: str) -> dict:
    """
    Clean raw text: normalize whitespace, remove excess newlines, trim.
    Returns dict with 'text' (cleaned) and 'stats' for UI.
    """
    if not raw or not raw.strip():
        return {"text": "", "stats": {"original_len": 0, "cleaned_len": 0}}

    original_len = len(raw)
    text = raw

    # Collapse multiple newlines to at most 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple spaces to single
    text = re.sub(r"[ \t]+", " ", text)
    # Strip per line and then overall
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(line for line in lines if line)
    text = text.strip()

    return {
        "text": text,
        "stats": {
            "original_len": original_len,
            "cleaned_len": len(text),
            "removed_chars": original_len - len(text),
        },
    }
