# AI Semantic Search & RAG Engine

A semantic search engine built for Month 02 Sprint A. It allows users to ingest text documents, search through them by meaning, and generate intelligent answers using a Retrieval-Augmented Generation (RAG) pipeline powered by Gemini.

## Tech Stack

* **Backend:** FastAPI
* **Vector Database:** ChromaDB
* **Embeddings:** all-MiniLM-L6-v2 (via sentence-transformers)
* **LLM Engine:** Gemini (google-genai)
* **Frontend:** Streamlit

## Setup Instructions

1. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set your Gemini API Key:**
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

```


4. **Run the backend server:**
```bash
uvicorn app.main:app --reload

```


5. **Run the Frontend UI:**
Open a new terminal window, activate the virtual environment, and run:
```bash
streamlit run streamlit_app.py

```