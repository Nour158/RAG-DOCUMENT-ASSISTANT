from pydantic import BaseModel, Field
class QueryRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
