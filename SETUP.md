# RAG Demo – Setup Guide

This guide walks you through setting up the RAG application locally, including the vector database and environment.

---

## Prerequisites

- **Python 3.10+** (recommended 3.10 or 3.11)
- **pip** (Python package manager)
- A **single PDF file** for testing (e.g. a short article or report)

---

## Step 1: Create a virtual environment (recommended)

Open a terminal in the project folder (`c:\dev\RAG_TEST`) and run:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your prompt.

---

## Step 2: Install dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:

- **streamlit** – web UI
- **pypdf** – PDF text extraction
- **chromadb** – local vector database (no separate server)
- **sentence-transformers** – local embedding model (downloads on first run)

The first time you run the app, `sentence-transformers` will download the model `all-MiniLM-L6-v2` (~80MB). This is one-time.

---

## Step 3: Database setup (ChromaDB)

**No manual database setup is required.**

- ChromaDB runs **embedded** in your app and stores data in a folder on disk.
- The app uses the folder: **`chroma_db`** (created automatically in the project root when you first run the pipeline).
- No separate database server, no credentials, no connection string.

If you want to **reset** the stored PDF index, delete the `chroma_db` folder and run the pipeline again (upload PDF → Store in ChromaDB).

---

## Step 4: Run the application

From the project root (`c:\dev\RAG_TEST`):

```bash
streamlit run app.py
```

Your browser should open to `http://localhost:8501`. If it doesn’t, open that URL manually.

---

## Step 5: Use the app (single PDF)

1. **Upload a PDF** in the "Data collection" step.
2. Watch the UI as each step runs:
   - **Collection** – raw text from the PDF
   - **Cleaning** – normalized text
   - **Chunking** – list of chunks
   - **Embedding** – vectors for each chunk
3. Click **"Store in ChromaDB"** to save the vectors to the local DB.
4. Type a **question** in the retrieval section and see:
   - Retrieved chunks
   - The context that would be sent to an LLM (answer area)

---

## Project structure

```
RAG_TEST/
├── app.py                 # Streamlit UI and pipeline orchestration
├── config.py              # Chunk size, paths, model name, etc.
├── requirements.txt
├── SETUP.md               # This file
├── data/                  # (optional) place sample PDFs here
├── uploads/               # PDFs uploaded via the UI
├── chroma_db/             # ChromaDB data (created on first store)
└── components/
    ├── data_collection.py # Load PDF
    ├── cleaning.py       # Clean text
    ├── chunking.py       # Split into chunks
    ├── embedding.py      # Compute embeddings
    ├── storage.py        # Save to ChromaDB
    ├── retrieval.py      # Query ChromaDB
    └── generation.py     # Build answer from context (template for demo)
```

---

## Optional: change chunk size or overlap

Edit `config.py`:

- `CHUNK_SIZE` – characters per chunk (default 500)
- `CHUNK_OVERLAP` – overlap between chunks (default 50)

Restart the app after changing config.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `FileNotFoundError: PDF not found` | Upload a PDF via the UI; don’t rely on a path outside the app. |
| `ModuleNotFoundError: config` | Run `streamlit run app.py` from the project root `RAG_TEST`. |
| ChromaDB errors after deleting `chroma_db` | Restart the app, upload the PDF again, and click "Store in ChromaDB". |
| First run is slow | The embedding model is downloaded on first use; later runs are faster. |

---

## Summary

1. **Python 3.10+** → create venv → `pip install -r requirements.txt`
2. **No extra DB setup** – ChromaDB is local and auto-created.
3. Run with **`streamlit run app.py`** from the project root.
4. Upload **one PDF**, follow the steps on the UI, then ask a question.

That’s all you need to run the RAG demo locally.
