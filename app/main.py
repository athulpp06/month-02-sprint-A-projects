from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions

# Initialize FastAPI
app = FastAPI(
    title="Semantic Search Engine API",
    description="A semantic search engine built with FastAPI, ChromaDB, and all-MiniLM-L6-v2",
    version="1.0.0"
)

# Initialize ChromaDB in-memory client for rapid prototyping
chroma_client = chromadb.Client()

# Set up the exact embedding model required for the sprint
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or connect to a collection
collection = chroma_client.get_or_create_collection(
    name="semantic_sprint_collection",
    embedding_function=embedding_function
)

# --- Pydantic Schemas ---
class Item(BaseModel):
    id: str
    content: str
    metadata: dict = {}

class SearchQuery(BaseModel):
    query_text: str
    limit: int = 5

# --- Endpoints ---
@app.post("/ingest", summary="Add a document to the vector database")
async def ingest_item(item: Item):
    try:
        collection.add(
            documents=[item.content],
            metadatas=[item.metadata],
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
        return {
            "status": "success", 
            "query": query.query_text,
            "matches": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))