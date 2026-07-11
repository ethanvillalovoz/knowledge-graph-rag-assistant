from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_allowed_origins
from .routers.dbpedia_query_router import router as dbpedia_router
from .routers.nlp_router import router as nlp_router
from .routers.vector_search_router import router as vector_search_router

app = FastAPI(
    title="Knowledge Graph RAG API",
    description="Retrieval API combining DBpedia context, FAISS search, and LLM synthesis.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(nlp_router, prefix="/nlp")
app.include_router(dbpedia_router, prefix="/dbpedia")
app.include_router(vector_search_router, prefix="/vector_search")


@app.get("/")
def read_root():
    return {"service": "knowledge-graph-rag", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
