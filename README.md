# Knowledge Graph RAG Assistant

An evidence-aware research workspace that combines dense retrieval, DBpedia knowledge-graph context, and generated answers.

[![CI](https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant/actions/workflows/test.yml/badge.svg)](https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE)

![Knowledge Graph RAG answering a technical question while exposing its retrieval trace](docs/media/rag-workspace.gif)

## Why This Exists

Most chat interfaces hide the retrieval pipeline. This project keeps it visible. A question moves through entity extraction, knowledge-graph lookup, semantic retrieval, and answer synthesis while the interface shows the evidence used at each stage.

The repository is Ethan Villalovoz's maintained fork of a Washington State University senior design capstone built for [HackerEarth](https://www.hackerearth.com/). The original team was Molly Iverson, Ethan Villalovoz, Chandler Juego, and Adam Shtrikman.

## System

```mermaid
flowchart LR
    Q[Question] --> N[spaCy entity extraction]
    N --> K[DBpedia SPARQL]
    Q --> E[SentenceTransformer embedding]
    E --> V[FAISS vector search]
    K --> G[Grounded prompt]
    V --> G
    G --> O[OpenAI response]
```

| Layer | Responsibility |
| --- | --- |
| React + TypeScript | Conversation, source context, and retrieval trace |
| FastAPI | Validated API boundary and orchestration |
| SentenceTransformers + FAISS | Dense semantic retrieval over Wikipedia passages |
| DBpedia | Explicit entity and relationship context through SPARQL |
| OpenAI | Concise synthesis over retrieved evidence |

## Run The Interface

The frontend includes a deterministic demo dataset, so the product can be evaluated without credentials or multi-gigabyte retrieval artifacts.

```bash
cd frontend/rag-app
npm ci
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Demo mode is labeled in the interface and never pretends to be a live model response.

## Run The Full Pipeline

1. Copy the environment template and set an OpenAI API key.

   ```bash
   cp .env.example .env
   ```

2. Download and checksum the versioned Wikipedia corpus files.

   ```bash
   python3 scripts/download_corpus.py
   ```

3. Download `text_embeddings.npy` and `index.faiss` from the [project dataset](https://huggingface.co/datasets/miverson9/acme10-he-ragapp-embeddings/tree/main) into `backend/app/data_processing/embeddings_data/`.

4. Start both services.

   ```bash
   docker compose up --build
   ```

The frontend runs at [http://localhost:3000](http://localhost:3000), the API at [http://localhost:8000](http://localhost:8000), and interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

For direct backend development:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
uvicorn backend.app.main:app --reload
```

## Repository Map

```text
backend/app/handlers       LLM, embedding, and vector-search services
backend/app/routers        FastAPI route boundaries
backend/app/data_processing
                           dataset preparation utilities and local artifacts
frontend/rag-app/src       typed product interface and deterministic demo
tests                      backend unit and integration coverage
docs                       reports, code guides, and project history
```

## Verification

```bash
CI=true PYTHONPATH=. pytest -q tests/
cd frontend/rag-app && npm run check
```

CI runs both suites on every pull request. Service initialization is lazy, so unit tests do not download an embedding or generation model unless a test explicitly exercises it.

## Design Decisions

- **Inspectable by default:** sources and retrieval stages stay adjacent to the answer.
- **Honest offline mode:** contributors can review the product without an API key; live and fixture data are visibly distinct.
- **Constrained boundaries:** query lengths, source counts, CORS origins, and public error messages are validated at the API edge.
- **Large artifacts out of Git:** corpus parquet files are checksum-verified release assets; the FAISS index and embedding matrix remain in the project dataset.

## Limitations

- Retrieval quality depends on corpus coverage, chunking, and similarity thresholds.
- DBpedia can return sparse results for ambiguous or uncommon entities.
- Exposing evidence improves inspectability but does not guarantee factual correctness.
- The included demo is a product fixture, not an evaluation of the full retrieval pipeline.

## Project Record

- [Demo video](https://www.youtube.com/watch?v=YWdR3FAdq1o)
- [Final report](docs/project-report/RAGApp-FinalReport.pdf)
- [Project abstract](docs/project-report/Project-Abstract.pdf)
- [Performance notes](docs/performance-stats.md)
- [Sprint reports](docs/sprint-reports/)

## License

Licensed under the terms in [LICENSE](LICENSE). Original team attribution is preserved above and in the project reports.
