# Deploy to Streamlit Community Cloud

Streamlit Community Cloud deploys your app from a **GitHub repository**. You need Git and a GitHub account.

---

## Step 1: Install Git (if needed)

- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win) and install.
- Or use **GitHub Desktop** if you prefer a GUI.

Check that Git is installed:

```powershell
git --version
```

---

## Step 2: Create a GitHub repository

1. Go to [github.com](https://github.com) and sign in.
2. Click **"New repository"** (or **"+"** → **New repository**).
3. Choose a name (e.g. `rag-demo`), set visibility to **Public** (required for free Streamlit Cloud).
4. Do **not** initialize with a README, .gitignore, or license (you already have files locally).
5. Click **Create repository**.

---

## Step 3: Push your code to GitHub

In a terminal, from your project folder:

```powershell
cd c:\dev\RAG_TEST

# Initialize Git (if not already)
git init

# Add all files (respects .gitignore)
git add .

# First commit
git commit -m "Initial commit: RAG demo app"

# Add your GitHub repo as remote (replace YOUR_USERNAME and YOUR_REPO with your values)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

If GitHub asks for authentication, use a **Personal Access Token** (Settings → Developer settings → Personal access tokens) as the password, or use **GitHub CLI** (`gh auth login`).

---

## Step 4: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **"New app"**.
3. **Repository**: select your repo (e.g. `YOUR_USERNAME/rag-demo`).
4. **Branch**: `main` (or the branch you use).
5. **Main file path**: `app.py`.
6. (Optional) Click **"Advanced settings"** and set **Python version** to 3.11 if available (works well with sentence-transformers and ChromaDB).
7. Click **"Deploy!"**.

The first deploy can take a few minutes (it installs dependencies and downloads the embedding model).

---

## Step 5: After deployment

- Your app URL will be like: `https://YOUR_APP_NAME.streamlit.app`.
- **Important**: On Streamlit Community Cloud the filesystem is **ephemeral**. The `chroma_db` folder and any uploaded PDFs are **not** kept when the app restarts or redeploys. So each time someone (or you) opens the app, they need to:
  1. Upload a PDF  
  2. Go through the pipeline (collection → cleaning → chunking → embedding)  
  3. Click **"Store in ChromaDB"**  
  4. Then they can ask questions until the app goes to sleep or is redeployed.

This is normal for the free tier and is fine for demos and testing.

---

## Summary checklist

| Step | Action |
|------|--------|
| 1 | Install Git, create GitHub account |
| 2 | Create a new **public** repo on GitHub (no README/gitignore) |
| 3 | `git init` → `git add .` → `git commit` → `git remote add origin` → `git push` |
| 4 | Go to share.streamlit.io → New app → pick repo, branch `main`, file `app.py` → Deploy |
| 5 | Use the app URL; re-upload and re-store PDF after each app restart if needed |

If you hit any error during **Step 4** (e.g. missing dependency or Python version), check the build logs on Streamlit Cloud and adjust `requirements.txt` or add a `runtime.txt` (e.g. `python-3.11.0`) if needed.
