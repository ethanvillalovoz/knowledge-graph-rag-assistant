from pydantic import BaseModel, Field


class Query(BaseModel):
    query: str = Field(min_length=1, max_length=2_000)
    vector_search_results: list[str] | None = Field(default=None, max_length=20)
    kg_results: str | None = Field(default=None, max_length=20_000)
