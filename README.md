# rag_test – RAG Demo (Single PDF, Step-by-Step UI)

A minimal **RAG (Retrieval-Augmented Generation)** app that loads one PDF and shows each pipeline step in the UI. Built for learning and testing.

## Quick start

1. **Setup** (one-time): see [SETUP.md](SETUP.md) for virtual environment, dependencies, and database.
2. **Run**: from project root run `streamlit run app.py`.
3. **Use**: upload a PDF, follow the steps on the page, then ask a question.

## What you see on the UI

- **Step 1 – Data collection**: raw text extracted from the PDF.
- **Step 2 – Cleaning**: normalized text and simple stats.
- **Step 3 – Chunking**: text split into overlapping chunks.
- **Step 4 – Embedding**: chunks turned into vectors (with a small preview).
- **Step 5 – Storage**: button to store vectors in local ChromaDB.
- **Step 6 & 7 – Retrieval & generation**: type a question, see retrieved chunks and the context used for the “answer” (template-style; no external LLM).

All logic is split into separate modules under `components/` for clarity.
