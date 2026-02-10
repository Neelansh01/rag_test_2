"""Step 5: Storage - persist embeddings in local ChromaDB."""
import chromadb
from config import CHROMA_DIR, COLLECTION_NAME


def get_client(persist_dir: str = CHROMA_DIR):
    """Get or create ChromaDB client with persistent storage."""
    return chromadb.PersistentClient(path=persist_dir)


def create_or_reset_collection(client, collection_name: str = COLLECTION_NAME):
    """Create a new collection (or get existing and clear for demo)."""
    try:
        col = client.get_collection(collection_name)
        client.delete_collection(collection_name)
    except Exception:
        pass
    return client.create_collection(name=collection_name, metadata={"description": "RAG demo"})


def store_embeddings(
    embeddings: list[dict],
    collection_name: str = COLLECTION_NAME,
    persist_dir: str = CHROMA_DIR,
) -> int:
    """
    Store chunk embeddings in ChromaDB. IDs are chunk_0, chunk_1, ...
    Returns number of documents stored.
    """
    if not embeddings:
        return 0

    client = get_client(persist_dir)
    col = create_or_reset_collection(client, collection_name)

    ids = [f"chunk_{e['index']}" for e in embeddings]
    documents = [e["text"] for e in embeddings]
    vectors = [e["embedding"] for e in embeddings]

    col.add(ids=ids, documents=documents, embeddings=vectors)
    return len(ids)


def get_stored_content(
    collection_name: str = COLLECTION_NAME,
    persist_dir: str = CHROMA_DIR,
    limit: int = 20,
) -> dict | None:
    """
    Read what's currently in the collection (for UI). Returns None if collection
    doesn't exist or is empty; otherwise dict with count and list of {id, text_preview}.
    """
    try:
        client = get_client(persist_dir)
        col = client.get_collection(collection_name)
    except Exception:
        return None
    n = col.count()
    if n == 0:
        return {"count": 0, "chunks": []}
    data = col.get(include=["documents"], limit=min(limit, n))
    chunks = [
        {"id": id_, "text_preview": (doc or "")[:300] + ("..." if len(doc or "") > 300 else "")}
        for id_, doc in zip(data["ids"], data["documents"])
    ]
    return {"count": n, "chunks": chunks}
