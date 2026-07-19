# backend dockerfile is in the root directory to prevent import errors
FROM python:3.10-slim

WORKDIR /

LABEL org.opencontainers.image.source="https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant"

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /backend

ARG EMBEDDING_DATASET_REVISION=28777c9a144261672040710e0316ca5e40345172
ARG EMBEDDINGS_SHA256=98592d86c93dbf474decba8b79426cd3c57c73c607b650692ce2df0398fbad74
ARG FAISS_INDEX_SHA256=1e87e64080acfce1cbc3ecad2b3a8ae80900dde935135042dc2481675d340b1a

RUN mkdir -p /backend/app/data_processing/vector_search_data \
    /backend/app/data_processing/embeddings_data \
    && wget -O /backend/app/data_processing/vector_search_data/index.faiss \
    "https://huggingface.co/datasets/ethanvillalovoz/knowledge-graph-rag-retrieval-artifacts/resolve/${EMBEDDING_DATASET_REVISION}/index.faiss" \
    && echo "${FAISS_INDEX_SHA256}  /backend/app/data_processing/vector_search_data/index.faiss" | sha256sum -c - \
    && wget -O /backend/app/data_processing/embeddings_data/text_embeddings.npy \
    "https://huggingface.co/datasets/ethanvillalovoz/knowledge-graph-rag-retrieval-artifacts/resolve/${EMBEDDING_DATASET_REVISION}/text_embeddings.npy" \
    && echo "${EMBEDDINGS_SHA256}  /backend/app/data_processing/embeddings_data/text_embeddings.npy" | sha256sum -c -

ENV PYTHONPATH=/

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
