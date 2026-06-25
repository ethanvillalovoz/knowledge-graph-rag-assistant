# Knowledge Graph RAG Assistant Demo Strategy

Knowledge Graph RAG Assistant is best presented through the existing project demo video plus a reproducible Docker/local setup. It should not advertise a public live app unless the backend, frontend, OpenAI access, DBpedia dependency, and large embedding artifacts are hosted and monitored together.

## Current Public Demo

- Primary demo: [Project demo video](https://www.youtube.com/watch?v=YWdR3FAdq1o)
- Supporting artifacts:
  - `docs/project-report/RAGApp-FinalReport.pdf`
  - `docs/project-report/final_client_presentation_ragapp.pdf`
  - `docs/performance-stats.md`
- Local reproduction through Docker or the README development steps.

## Why Not GitHub Pages

GitHub Pages only hosts static files. It cannot run:

- The React frontend as a connected full-stack application.
- The FastAPI backend.
- DBpedia SPARQL queries.
- FAISS vector search over local index files.
- OpenAI-powered answer generation.
- Large embedding artifacts that are intentionally not committed to the repository.

For that reason, a GitHub Pages link would only be a static walkthrough unless the backend, vector artifacts, and model/API dependencies were hosted elsewhere.

## Recommended Public Demo Format

The existing demo video is the right public artifact. If refreshed later, a strong walkthrough should show:

1. Starting the app with Docker.
2. Asking a natural-language question.
3. Retrieving vector-search context from Wikipedia embeddings.
4. Adding structured context from DBpedia.
5. Returning a grounded answer in the React chat interface.

Keep the video focused on the system behavior and mention that the repository is a maintained fork of a team capstone project.

## Local Reproduction Checklist

Before recording a new walkthrough:

- Configure `.env` with an OpenAI API key.
- Download the FAISS index and embedding array from the linked Hugging Face dataset.
- Start the app with `docker compose up --build` or run the backend/frontend manually.
- Verify the frontend reaches the backend at the expected local URL.
- Use representative questions that exercise both vector search and knowledge graph retrieval.

## If A Hosted Demo Is Added Later

A real public live demo should only be linked after:

- The backend and frontend deployments are stable.
- FAISS and embedding artifacts are available in the hosted runtime.
- OpenAI keys are stored as server-side secrets.
- DBpedia availability, rate limits, and failure behavior are handled.
- The README clearly labels the hosted demo as maintained.
