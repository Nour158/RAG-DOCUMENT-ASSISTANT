from fastapi import APIRouter, Request
from app.schemas.query import QueryRequest, QueryResponse
from app.services.generation import generate
router=APIRouter()
@router.get("/health")
def health(request:Request): return {"status":"ok","chunks":request.app.state.retriever.collection.count()}
@router.post("/query",response_model=QueryResponse)
def query(body:QueryRequest,request:Request):
    chunks=request.app.state.retriever.search(body.question); answer,sources=generate(body.question,chunks); return QueryResponse(answer=answer,sources=sources)
