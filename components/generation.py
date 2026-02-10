"""Step 7: Generation - produce an answer from retrieved context + query (simple template)."""
# No external LLM for minimal setup: we format context + query for visibility.
# You can plug in OpenAI/Ollama later.


def generate_answer(query: str, retrieved_chunks: list[dict]) -> dict:
    """
    Build a simple 'answer' from retrieved context. For demo we concatenate
    context and echo the query; no API key or model required.
    """
    context = "\n\n---\n\n".join(c["text"] for c in retrieved_chunks)
    # First chunk is usually the most relevant (lowest distance) — show it as "key passage"
    key_passage = (retrieved_chunks[0]["text"].strip() if retrieved_chunks else "")
    # Simple template response so the UI can show "what would be sent to an LLM"
    answer = (
        f"[Retrieved context used for answering]\n\n{context}\n\n"
        f"[Your question]\n{query}\n\n"
        "[In a full RAG app, an LLM would generate an answer from the context above.]"
    )
    return {
        "answer": answer,
        "context_used": context,
        "num_chunks": len(retrieved_chunks),
        "key_passage": key_passage,
    }
