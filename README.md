# Knowledge Graph RAG Assistant

Knowledge Graph RAG Assistant is a Washington State University senior design capstone project built for [HackerEarth](https://www.hackerearth.com/). The system explores retrieval-augmented generation over a large Wikipedia knowledge base using a React frontend, FastAPI backend, DBpedia knowledge graph queries, FAISS vector search, and OpenAI-powered response generation.

This repository is Ethan Villalovoz's maintained fork of the original team project, originally developed under the ACME10-HE-RAGApp capstone name. The capstone team was Molly Iverson, Ethan Villalovoz, Chandler Juego, and Adam Shtrikman.

## Demo

- [Project demo video](https://www.youtube.com/watch?v=YWdR3FAdq1o)
- [Final project report](docs/project-report/RAGApp-FinalReport.pdf)
- [Project abstract](docs/project-report/Project-Abstract.pdf)

## What It Does

The application lets a user ask natural-language questions and receive responses grounded in retrieved context. The backend combines:

- **Vector search:** FAISS index over Wikipedia embeddings.
- **Embedding model:** SentenceTransformers for semantic retrieval.
- **Knowledge graph:** DBpedia SPARQL queries for structured context.
- **LLM layer:** OpenAI chat completion with retrieved evidence.
- **Frontend:** React chat interface for user queries and generated responses.

## Architecture

```text
frontend/rag-app         React + TypeScript user interface
backend/app/main.py      FastAPI application entrypoint
backend/app/routers      API routes for NLP, DBpedia, and vector search
backend/app/handlers     LLM, embedding, and vector search logic
backend/app/data_processing
                         dataset extraction and embedding assets
tests                    backend unit and integration tests
docs                     meeting notes, sprint reports, code guides, and reports
```

## Quick Start With Docker

Docker is the easiest way to run the full app because the backend depends on large embedding and FAISS index files.

1. Create a local environment file:

   ```bash
   cp .env.example .env
   ```

2. Add your OpenAI API key to `.env`:

   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Build and start the app:

   ```bash
   docker compose up --build
   ```

4. Open the app:

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

To stop the app:

```bash
docker compose down
```

## Local Development

### Prerequisites

- Python 3.10
- Node.js 20.19+ or 22+
- OpenAI API key

### Backend

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
export OPENAI_API_KEY=sk-your-key-here
export PYTHONPATH=$(pwd)
uvicorn backend.app.main:app --reload
```

The vector search runtime also needs the large embedding files from the project dataset:

- Download `text_embeddings.npy` from the [Hugging Face dataset](https://huggingface.co/datasets/miverson9/acme10-he-ragapp-embeddings/tree/main) into `backend/app/data_processing/embeddings_data/`.
- Download `index.faiss` into `backend/app/data_processing/vector_search_data/`.

### Frontend

In a second terminal:

```bash
cd frontend/rag-app
npm ci
npm start
```

The frontend runs at [http://localhost:3000](http://localhost:3000) and expects the backend at [http://localhost:8000](http://localhost:8000).

## Testing

Backend:

```bash
CI=true PYTHONPATH=. pytest tests/
```

Frontend:

```bash
cd frontend/rag-app
npm test
npm run build
```

`CI=true` lets the backend tests avoid requiring a real OpenAI API key.

## Documentation

- [Sprint reports](docs/sprint-reports/)
- [Meeting notes](docs/meeting-notes/)
- [Code guides](docs/code-guides/)
- [Performance notes](docs/performance-stats.md)
- [Final project report](docs/project-report/RAGApp-FinalReport.pdf)
- [Final client presentation](docs/project-report/final_client_presentation_ragapp.pdf)

## Known Limitations

- Vector search quality depends heavily on embedding coverage, chunking strategy, and threshold tuning.
- DBpedia SPARQL queries can fail or return sparse context for ambiguous entities.
- The project prototype uses large local embedding artifacts that are not committed to the repository.
- Some generated responses may still be limited by retrieval quality or missing source coverage.

## Credits

This project was developed as a WSU senior design capstone project for HackerEarth by Molly Iverson, Ethan Villalovoz, Chandler Juego, and Adam Shtrikman.

## License

This project is licensed under the terms in [LICENSE](LICENSE).
