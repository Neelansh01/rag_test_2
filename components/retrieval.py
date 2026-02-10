"""Step 6: Retrieval - find the most relevant chunks for a query."""
from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_DIR, COLLECTION_NAME, TOP_K_RETRIEVAL, EMBEDDING_MODEL


def retrieve(
    query: str,
    top_k: int = TOP_K_RETRIEVAL,
    collection_name: str = COLLECTION_NAME,
    persist_dir: str = CHROMA_DIR,
    model_name: str = EMBEDDING_MODEL,
) -> list[dict]:
    """
    Embed the query, search ChromaDB, return list of dicts with 'text', 'metadata', 'distance'.
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
