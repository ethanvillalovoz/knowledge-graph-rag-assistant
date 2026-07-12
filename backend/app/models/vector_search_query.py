from pydantic import BaseModel, Field


class VectorSearchQuery(BaseModel):
    query_text: str = Field(min_length=1, max_length=2_000)
