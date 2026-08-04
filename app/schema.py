from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Item(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="The text content to be vectorized and stored")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Optional metadata tags")

class SearchQuery(BaseModel):
    query_text: str = Field(..., description="The semantic search query text")
    limit: int = Field(default=5, ge=1, le=50, description="Number of results to return (1-50)")