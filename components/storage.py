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
