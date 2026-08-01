# The Waste Land — RAG Literary Assistant

A Retrieval-Augmented Generation app over T. S. Eliot's *The Waste Land* (1922).

Answers are grounded in poem text only, with cited sources.

---

## Project Structure

```
01_documents.py            Raw poem corpus (5 sections, 54 stanzas)
02_preprocessing.py        Clean and normalise stanza text
03_chunking.py             Stanza-level chunks with annotation metadata
04_vector_representation.py  Encode chunks with multilingual-MiniLM-L12-v2
05_create_chroma_store.py  Build and persist ChromaDB vector store
06_retrieve_context.py     Semantic retrieval from ChromaDB
07_prompting.py            Prompt builder + OpenRouter LLM call
streamlit_app.py           Streamlit chat UI
requirements.txt
.gitignore
.streamlit/secrets.toml    Local secrets template (never commit)
```

---

## Local Setup (VS Code)

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/YOUR_USERNAME/wasteland-rag.git
cd wasteland-rag
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key (local only)

Create `.streamlit/secrets.toml` (already in `.gitignore`):

```toml
OPENROUTER_API_KEY = "your_real_key_here"
OPENROUTER_MODEL   = "openai/gpt-4o-mini"
```

Get a free key at [openrouter.ai](https://openrouter.ai).

### 4. Build the vector store (first run only)

```bash
python 05_create_chroma_store.py
```

This encodes all 54 stanzas and saves to `./chroma_store/`.
Takes ~30 seconds on first run; subsequent runs load from disk instantly.

### 5. Run the app

```bash
streamlit run streamlit_app.py
```

---

## Streamlit Cloud Deployment

1. Push this repo to GitHub (**do NOT include `.streamlit/secrets.toml`**)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main file to `streamlit_app.py`
4. Open **Manage App > Secrets** and add:

```toml
OPENROUTER_API_KEY = "your_real_key_here"
OPENROUTER_MODEL   = "openai/gpt-4o-mini"
```

5. Deploy. The vector store is built automatically on first load.

---

## Pipeline

```
Query
 → embed_query()             (multilingual-MiniLM-L12-v2)
 → ChromaDB cosine search    (top-k stanzas)
 → build_context_string()    (numbered [Source N] blocks)
 → SYSTEM_PROMPT + sources   (prompt builder)
 → OpenRouter API call       (gpt-4o-mini)
 → cited answer              (Streamlit chat UI)
```

---

## API Key Rules (Submission Checklist)

- [ ] Real API key is NOT in any `.py` file
- [ ] Real API key is NOT in the ZIP file
- [ ] Real API key is NOT committed to GitHub
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Streamlit Cloud secrets are configured in valid TOML format
- [ ] `chroma_store/` is in `.gitignore` (built at runtime)
- [ ] All 8 required Python files exist
- [ ] `requirements.txt` exists
- [ ] App runs and answers cite `[Source N]`
