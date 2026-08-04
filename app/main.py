import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from dotenv import load_dotenv
from app.schema import Item, SearchQuery

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Initialize Gemini Client (automatically reads GEMINI_API_KEY from environment)
try:
    genai_client = genai.Client()
except Exception as e:
    genai_client = None
    print("Warning: Gemini API Key not found. The /ask endpoint will fail.")

# 3. Sample dataset to populate automatically on startup
SEED_DATA = [
    {
        "id": "movie_01",
        "content": "A high-stakes sci-fi thriller where thieves enter people's dreams to steal confidential secrets.",
        "metadata": {"category": "Movies", "genre": "Sci-Fi"}
    },
    {
        "id": "movie_02",
        "content": "A dark detective mystery investigating a husband after his wife mysteriously vanishes on their anniversary.",
        "metadata": {"category": "Movies", "genre": "Mystery"}
    },
    {
        "id": "job_01",
        "content": "Backend Developer position looking for experience with Python, FastAPI, asynchronous APIs, and relational databases.",
        "metadata": {"category": "Jobs", "role": "Backend"}
    },
    {
        "id": "job_02",
        "content": "Machine Learning Engineer role focused on building RAG pipelines, vector search with ChromaDB, and LLM integration.",
        "metadata": {"category": "Jobs", "role": "AI/ML"}
    },
    {
        "id": "lost_01",
        "content": "Black leather wallet with a student ID card and bus pass found inside the main library cafeteria.",
        "metadata": {"category": "Lost & Found", "location": "Library"}
    }
]

# 4. Initialize ChromaDB client and Embedding Model
chroma_client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = chroma_client.get_or_create_collection(
    name="semantic_sprint_collection",
    embedding_function=embedding_function
)

# 5. Define startup behavior (Auto-seeding)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-seed initial data on startup if collection is empty
    if collection.count() == 0:
        ids = [item["id"] for item in SEED_DATA]
        documents = [item["content"] for item in SEED_DATA]
        metadatas = [item["metadata"] for item in SEED_DATA]
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"✅ Auto-seeded {len(SEED_DATA)} sample documents into ChromaDB.")
    yield

# 6. Initialize FastAPI App
app = FastAPI(
    title="AI RAG Search Engine API",
    description="A semantic search engine and RAG pipeline with FastAPI, ChromaDB, and Gemini.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Endpoints ---

@app.post("/ingest", summary="Add a document to the vector database")
async def ingest_item(item: Item):
    try:
        collection.add(
            documents=[item.content],
            metadatas=[item.metadata] if item.metadata else [{}],
            ids=[item.id]
        )
        return {"status": "success", "message": f"Added item {item.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", summary="Perform a semantic search")
async def semantic_search(query: SearchQuery):
    try:
        results = collection.query(
            query_texts=[query.query_text],
            n_results=query.limit
        )
        
        formatted_results = []
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results.get("distances") else 0.0
                })

        return {
            "status": "success", 
            "query": query.query_text,
            "matches": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", summary="Perform Semantic Search + LLM Answer (RAG)")
async def ask_rag(query: SearchQuery):
    if not genai_client:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured on server.")
        
    try:
        # Step A: Retrieve relevant context from ChromaDB
        search_results = collection.query(
            query_texts=[query.query_text],
            n_results=3
        )
        
        retrieved_docs = search_results["documents"][0] if search_results["documents"] else []
        if not retrieved_docs:
            return {"query": query.query_text, "answer": "No relevant documents found in the database."}

        # Step B: Combine documents into a context block
        context_str = "\n---\n".join(retrieved_docs)
        prompt = f"""
You are a helpful AI search assistant. Answer the user's question accurately using ONLY the context provided below. 
If the answer cannot be determined from the context, say so clearly.

Context:
{context_str}

User Question: {query.query_text}
Answer:
"""
        # Step C: Call the Gemini API
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return {
            "status": "success",
            "query": query.query_text,
            "retrieved_sources": retrieved_docs,
            "ai_answer": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "healthy", "database_items": collection.count()}