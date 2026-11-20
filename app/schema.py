from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Item(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="The text content to be vectorized and stored")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Optional metadata tags")

class SearchQuery(BaseModel):
    query_text: Optional[str] = Field(default=None, description="The semantic search query text")
    query: Optional[str] = Field(default=None, description="Alternative alias for query text")
    limit: int = Field(default=5, ge=1, le=50, description="Number of results to return (1-50)")

    def get_query_text(self) -> str:
        return self.query_text or self.query or ""