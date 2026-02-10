"""Step 6: Retrieval - find the most relevant chunks (semantic or keyword)."""
from sentence_transformers import SentenceTransformer
import chromadb
import re
from config import CHROMA_DIR, COLLECTION_NAME, TOP_K_RETRIEVAL, EMBEDDING_MODEL


def retrieve(
    query: str,
    top_k: int = TOP_K_RETRIEVAL,
    collection_name: str = COLLECTION_NAME,
    persist_dir: str = CHROMA_DIR,
    model_name: str = EMBEDDING_MODEL,
) -> list[dict]:
    """
    Semantic: embed the query, search ChromaDB by similarity. Return list of dicts with 'text', 'metadata', 'distance'.
    """
    client = chromadb.PersistentClient(path=persist_dir)
    col = client.get_collection(collection_name)
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query], show_progress_bar=False)[0].tolist()

    results = col.query(query_embeddings=[query_embedding], n_results=top_k, include=["documents", "metadatas", "distances"])

    out = []
    if results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            out.append({
                "id": doc_id,
                "text": results["documents"][0][i],
                "metadata": (results["metadatas"][0] or [{}])[i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results.get("distances") else None,
            })
    return out


def _tokenize(s: str) -> set:
    """Lowercase words, strip punctuation."""
    return set(re.findall(r"\b\w+\b", (s or "").lower()))


def retrieve_keyword(
    query: str,
    top_k: int = TOP_K_RETRIEVAL,
    collection_name: str = COLLECTION_NAME,
    persist_dir: str = CHROMA_DIR,
) -> list[dict]:
    """
    Keyword: fetch all chunks, score by query-word overlap (count of query words in chunk), return top_k.
    Returns same shape as retrieve() with 'score' instead of 'distance' (higher = better).
    """
    client = chromadb.PersistentClient(path=persist_dir)
    col = client.get_collection(collection_name)
    data = col.get(include=["documents", "metadatas"])
    if not data["ids"]:
        return []
    query_words = _tokenize(query)
    scored = []
    for i, doc_id in enumerate(data["ids"]):
        doc = (data["documents"] or [""])[i] or ""
        words = _tokenize(doc)
        overlap = len(query_words & words)
        scored.append({
            "id": doc_id,
            "text": doc,
            "metadata": (data["metadatas"][i] or {}) if data.get("metadatas") else {},
            "distance": -overlap,
        })
    scored.sort(key=lambda x: x["distance"])
    return scored[:top_k]


RETRIEVER_METHODS = {
    "semantic": ("Semantic (SBERT)", retrieve),
    "keyword": ("Keyword overlap", retrieve_keyword),
}


def retrieve_with_method(
    query: str,
    method: str = "semantic",
    top_k: int = TOP_K_RETRIEVAL,
    **kwargs,
) -> list[dict]:
    """Run the selected retriever. method: 'semantic' | 'keyword'."""
    if method == "keyword":
        return retrieve_keyword(query, top_k=top_k, **kwargs)
    return retrieve(query, top_k=top_k, **kwargs)
