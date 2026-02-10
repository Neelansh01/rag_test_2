"""
RAG Demo App – Single PDF, step-by-step visibility on UI.
Run from project root: streamlit run app.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_DIR, UPLOAD_DIR

from components.data_collection import load_pdf
from components.cleaning import clean_text
from components.chunking import chunk_text
from components.embedding import embed_chunks
from components.storage import store_embeddings, get_stored_content
from components.retrieval import retrieve
from components.generation import generate_answer
from components.llm_azure import is_azure_configured, generate_with_azure

# Ensure dirs exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="RAG Demo", page_icon="📄", layout="wide")

# --- RAG explanation ---
st.title("📄 RAG Demo: Single PDF")
st.markdown("""
**RAG (Retrieval-Augmented Generation)** uses your own documents to answer questions.  
Instead of the model relying only on its training data, it **retrieves** relevant passages from your PDF,  
then **generates** an answer using that context. Below you can see each step.
""")

st.subheader("Pipeline overview")
st.markdown("""
| Step | What happens |
|------|----------------|
| **1. Data collection** | Load and extract text from your PDF. |
| **2. Cleaning** | Normalize whitespace and remove noise. |
| **3. Chunking** | Split text into overlapping chunks for retrieval. |
| **4. Embedding** | Turn each chunk into a vector (numbers). |
| **5. Storage** | Save vectors in a local vector DB (ChromaDB). |
| **6. Retrieval** | For a question, find the most similar chunks. |
| **7. Generation** | (Optional) Use an LLM to answer from those chunks. |
""")

st.divider()

# --- Upload & run pipeline ---
st.subheader("1️⃣ Data collection")
st.caption("Upload a single PDF. We extract raw text from every page.")
pdf_file = st.file_uploader("Choose a PDF", type=["pdf"], key="pdf_upload")

collected = None
cleaned = None
chunks = None
embeddings = None
stored_count = 0

if pdf_file:
    save_path = os.path.join(UPLOAD_DIR, pdf_file.name)
    with open(save_path, "wb") as f:
        f.write(pdf_file.getvalue())
    with st.spinner("Loading PDF..."):
        collected = load_pdf(save_path)
    st.success(f"Loaded **{collected['metadata']['num_pages']}** pages, **{collected['metadata']['total_chars']}** characters.")
    with st.expander("View raw extracted text (first 1500 chars)"):
        st.text(collected["text"][:1500] + ("..." if len(collected["text"]) > 1500 else ""))

    st.divider()
    st.subheader("2️⃣ Cleaning")
    st.caption("Normalize whitespace and remove excess newlines.")
    cleaned = clean_text(collected["text"])
    st.metric("Characters after cleaning", cleaned["stats"]["cleaned_len"])
    st.caption(f"Removed {cleaned['stats']['removed_chars']} characters.")
    with st.expander("View cleaned text (first 1500 chars)"):
        st.text((cleaned["text"] or "")[:1500] + ("..." if len(cleaned["text"] or "") > 1500 else ""))

    st.divider()
    st.subheader("3️⃣ Chunking")
    st.caption(f"Split into overlapping chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")
    chunks = chunk_text(cleaned["text"])
    st.metric("Number of chunks", len(chunks))
    for i, c in enumerate(chunks[:5]):
        with st.expander(f"Chunk {c['index']} (preview)"):
            st.text(c["text"][:400] + ("..." if len(c["text"]) > 400 else ""))
    if len(chunks) > 5:
        st.caption(f"... and {len(chunks) - 5} more chunks.")

    st.divider()
    st.subheader("4️⃣ Embedding")
    st.caption("Convert each chunk to a vector using a small local model (sentence-transformers).")
    with st.spinner("Computing embeddings..."):
        embeddings = embed_chunks(chunks)
    st.success(f"Embedded **{len(embeddings)}** chunks. Each vector has **{len(embeddings[0]['embedding'])}** dimensions.")
    with st.expander("View first chunk's vector (first 20 dimensions)"):
        st.code(str(embeddings[0]["embedding"][:20]) + "...")

    st.divider()
    st.subheader("5️⃣ Storage")
    st.caption("Store vectors in local ChromaDB (no server required).")
    if st.button("Store in ChromaDB"):
        with st.spinner("Storing..."):
            stored_count = store_embeddings(embeddings)
        st.success(f"Stored **{stored_count}** chunks in the vector database.")
        st.session_state["stored"] = True

# Show what's currently in ChromaDB (works on Cloud too – this is the only way to "see" stored content)
st.divider()
st.subheader("📂 What’s in the database?")
st.caption("On Cloud, data lives only in the running app’s memory; you can’t open the folder. Use this section to see what’s currently stored.")
if st.button("Refresh / View stored chunks", key="view_db"):
    st.session_state["show_db"] = True
if st.session_state.get("show_db"):
    info = get_stored_content()
    if info is None:
        st.warning("No collection yet, or database not available. Upload a PDF and click **Store in ChromaDB** first.")
    else:
        st.metric("Chunks in ChromaDB", info["count"])
        for c in info["chunks"]:
            with st.expander(f"**{c['id']}**"):
                st.text(c["text_preview"])

st.divider()
st.subheader("6️⃣ Retrieval & 7️⃣ Generation")
st.caption("Ask a question. We retrieve the most relevant chunks and show the context used for answering. (Upload a PDF and click **Store in ChromaDB** first if you haven’t.)")

from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
_use_azure = is_azure_configured(api_key=AZURE_OPENAI_API_KEY, endpoint=AZURE_OPENAI_ENDPOINT)

answer_mode = st.radio(
    "Answer with",
    options=["Context only (no LLM)", "GPT-4o (Azure) – direct answer"] if _use_azure else ["Context only (no LLM)"],
    key="answer_mode",
    horizontal=True,
)
use_gpt4o = _use_azure and "GPT-4o" in answer_mode

query = st.text_input("Your question", placeholder="e.g. What is the main topic?", key="query")
if query:
    try:
        with st.spinner("Retrieving..."):
            retrieved = retrieve(query)
        if not retrieved:
            st.warning("No chunks in the database. Upload a PDF and click **Store in ChromaDB** first.")
        else:
            st.metric("Chunks retrieved", len(retrieved))
            for i, r in enumerate(retrieved):
                with st.expander(f"Retrieved chunk {i+1} (distance: {r.get('distance', 'N/A')})"):
                    st.text(r["text"])
            with st.spinner("Building answer..."):
                out = generate_answer(query, retrieved)
            context = out["context_used"]

            if use_gpt4o:
                with st.spinner("Calling GPT-4o..."):
                    direct_answer, err = generate_with_azure(
                        query, context,
                        api_key=AZURE_OPENAI_API_KEY, endpoint=AZURE_OPENAI_ENDPOINT,
                    )
                if err:
                    st.error(f"Azure OpenAI error: {err}")
                else:
                    st.subheader("Answer (GPT-4o)")
                    st.success(direct_answer)
                st.markdown("**Most relevant passage from your document:**")
                st.info(out.get("key_passage", "") or "(none)")
                with st.expander("Full context sent to GPT-4o"):
                    st.text_area("", value=out["answer"], height=200, disabled=True, key=f"ctx_{abs(hash(query)) % 10**8}")
            else:
                st.subheader("Answer / Context sent to LLM")
                st.markdown("**Most relevant passage (answer is in here):**")
                st.info(out.get("key_passage", "") or "(none)")
                st.caption("Full context sent to an LLM would be:")
                st.text_area("", value=out["answer"], height=280, disabled=True, key=f"answer_{abs(hash(query)) % 10**8}")
                st.caption("In a full RAG app, an LLM would generate a short answer from the context above.")
    except Exception as e:
        st.error(f"Retrieval failed. Upload a PDF, run all steps, and click **Store in ChromaDB** first. Error: {e}")

st.divider()
st.caption("RAG Demo – components: data_collection, cleaning, chunking, embedding, storage, retrieval, generation.")
