# AI Semantic Search & RAG Engine

A semantic search engine and RAG pipeline built for Month 02 Sprint A. It allows users to ingest text documents, search through them by meaning, and generate intelligent answers using a Retrieval-Augmented Generation (RAG) pipeline powered by Gemini.

## Live Demo

- **App (Streamlit):** https://month-02-sprint-a-projects-g72yqio6szjgmnu8uemdlf.streamlit.app
- **API docs (Swagger):** https://month-02-sprint-a-projects-7xcw.onrender.com/docs

## Tech Stack

* **Backend:** FastAPI
* **Vector Database:** ChromaDB
* **Embeddings:** all-MiniLM-L6-v2 (ChromaDB ONNX DefaultEmbeddingFunction)
* **LLM Engine:** Gemini (`gemini-2.5-flash` via `google-genai`)
* **Frontend:** Streamlit

---

## Local Setup & Run Instructions

### 1. Create and Activate Virtual Environment

```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory (refer to `.env.example`):

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> **Note:** The `GEMINI_API_KEY` is required for the RAG `/ask` endpoint powered by Gemini. The semantic `/search` and `/ingest` endpoints work locally without an API key using the built-in ChromaDB ONNX model.

### 4. Run the Backend API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and opening `http://127.0.0.1:8000/` automatically redirects to Swagger UI at `http://127.0.0.1:8000/docs`.

### 5. Run the Streamlit Frontend

In a separate terminal window (with virtual environment activated):

```bash
streamlit run streamlit_app.py
```

The Streamlit dashboard will open at `http://localhost:8501`. By default, it connects to `http://127.0.0.1:8000`.

---

## Deployment Settings

### 1. Render (Backend Web Service)

- **Branch:** `athul-pp`
- **Root Directory:** *(leave blank)*
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/health`
- **Environment Variables:**
  - `GEMINI_API_KEY`: Your Google Gemini API Key

### 2. Streamlit Community Cloud (Frontend)

- **Repository:** `athulpp06/month-02-sprint-A-projects`
- **Branch:** `athul-pp`
- **Main file path:** `streamlit_app.py`
- **App Secrets / Environment Variables:**
  - `BACKEND_URL`: `https://month-02-sprint-a-projects-7xcw.onrender.com`
