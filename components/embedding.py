"""Step 4: Embedding - convert text chunks into vector embeddings."""
from sentence_transformers import SentenceTransformer


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """Load the sentence-transformers model (cached after first run)."""
    return SentenceTransformer(model_name)


def embed_chunks(chunks: list[dict], model_name: str = "all-MiniLM-L6-v2") -> list[dict]:
    """
    Compute embeddings for each chunk. Returns list of dicts with 'text', 'index', 'embedding'.
    """
    if not chunks:
        return []

    model = get_embedding_model(model_name)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False)

    return [
        {"index": c["index"], "text": c["text"], "embedding": emb.tolist()}
        for c, emb in zip(chunks, embeddings)
    ]
