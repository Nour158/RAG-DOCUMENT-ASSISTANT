from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router
from app.core.config import get_settings
from app.services.retrieval import Retriever
@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.retriever=Retriever(); yield
app=FastAPI(title="RAG Document Assistant API",version="1.0.0",lifespan=lifespan)
s=get_settings(); app.add_middleware(CORSMiddleware,allow_origins=[s.frontend_origin],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
