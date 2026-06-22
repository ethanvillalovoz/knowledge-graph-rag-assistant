# Contributing

Thanks for helping improve ACME10-HE-RAGApp. This repository preserves and maintains a WSU senior design capstone project, so contributions should keep the project history, team attribution, and HackerEarth client context intact.

## Development Setup

Use the root `README.md` for Docker, backend, and frontend setup.

Common verification commands:

```bash
CI=true PYTHONPATH=. pytest tests/
cd frontend/rag-app && npm test
cd frontend/rag-app && npm run build
```

## Contribution Guidelines

- Do not commit API keys, `.env` files, generated build output, local virtual environments, or large embedding/index files.
- Keep core RAG behavior changes small and well explained.
- Add or update tests when changing backend handlers, routers, or frontend behavior.
- Update documentation when setup, commands, dependencies, or runtime assumptions change.
- Preserve attribution to the original capstone team: Molly Iverson, Ethan Villalovoz, Chandler Juego, and Adam Shtrikman.

## Pull Requests

Please include:

- A short summary of the change.
- The affected area: backend, frontend, retrieval, DBpedia, Docker, CI, or docs.
- Commands used to verify the change.
- Notes about any remaining limitations or follow-up work.
