# Azure OpenAI (GPT-4o) – Setup

To get **direct answers** from the RAG app using your Azure-deployed GPT-4o, configure the app with your Azure credentials. **Never commit API keys to the repo.**

---

## Option 1: Environment variables (local)

Create a `.env` file in the project root (and add `.env` to `.gitignore` – it’s already ignored). Example:

```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://openclawsss.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

Or set the same variables in your shell before running `streamlit run app.py`.  
The app reads these via `python-dotenv` if you load `.env` (e.g. in `app.py` add `load_dotenv()` at the top).

---

## Option 2: Streamlit secrets (Streamlit Cloud)

On [share.streamlit.io](https://share.streamlit.io), open your app → **Settings** → **Secrets**, and add:

```toml
[azure_openai]
api_key = "your_azure_api_key_here"
endpoint = "https://YOUR_RESOURCE.openai.azure.com"
```

Optional (defaults are already set in code):

```toml
# Optional – these have defaults
# deployment = "gpt-4o"
# api_version = "2025-01-01-preview"
```

The app will use these when running on Streamlit Cloud so you don’t need to set env vars there.

---

## What you need from Azure

- **Endpoint**: Your Azure OpenAI resource URL, e.g. `https://openclawsss.openai.azure.com` (no trailing slash).
- **API key**: From Azure Portal → your OpenAI resource → **Keys and Endpoint**.
- **Deployment name**: The name of your GPT-4o deployment (e.g. `gpt-4o`). Default in the app is `gpt-4o`.
- **API version**: e.g. `2025-01-01-preview`. Default in the app is `2025-01-01-preview`.

---

## In the app

1. Upload a PDF and run the pipeline (collection → cleaning → chunking → embedding).
2. Click **Store in ChromaDB**.
3. In **"Answer with"**, choose **"GPT-4o (Azure) – direct answer"** (only visible when Azure is configured).
4. Ask a question; the app will show a **direct answer** from GPT-4o plus the **most relevant passage** and the **full context** in an expander.

If Azure isn’t configured, you’ll only see **"Context only (no LLM)"** and a short note on how to enable GPT-4o.
