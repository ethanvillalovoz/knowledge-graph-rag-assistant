# Reproducibility

This repository exposes three distinct reproducibility surfaces. They should
not be treated as interchangeable.

## 1. Interface review without external services

The React interface includes a deterministic fixture that demonstrates source
selection and retrieval-trace interactions without presenting fixture content
as a live model response.

```bash
cd frontend/rag-app
npm ci
npm run dev
```

This verifies the interface workflow only. It does not evaluate retrieval or
answer quality.

## 2. Maintained code checks

The public CI workflow runs the backend and frontend suites independently:

```bash
CI=true PYTHONPATH=. pytest -q tests/
cd frontend/rag-app && npm run check
```

The DBpedia boundary is mocked in ordinary CI. Live DBpedia availability,
OpenAI responses, network latency, and generated wording are therefore outside
the deterministic test surface.

## 3. Full retrieval prototype

The full prototype requires three artifact groups:

| Artifact | Location | Integrity record |
| --- | --- | --- |
| Simple English Wikipedia corpus | GitHub release `data-v1` | SHA-256 values in `scripts/download_corpus.py` |
| `text_embeddings.npy` | Hugging Face revision `b88b9c93be2943f05485874914af00c47b82fc18` | `98592d86c93dbf474decba8b79426cd3c57c73c607b650692ce2df0398fbad74` |
| `index.faiss` | Hugging Face revision `b88b9c93be2943f05485874914af00c47b82fc18` | `1e87e64080acfce1cbc3ecad2b3a8ae80900dde935135042dc2481675d340b1a` |

Download the corpus using the repository script, then place the embedding
matrix and FAISS index in the paths documented in the root README. The Docker
build uses the same immutable Hugging Face revision and refuses artifacts that
do not match these checksums.

The original project record does not preserve the exact Wikipedia snapshot
date, passage-to-embedding construction environment, or all hardware/runtime
controls. These omissions prevent the archived artifacts from serving as a
fully reconstructible benchmark. See [Data Notice](../DATA_NOTICE.md).

## Paper-to-code boundary

The technical report records the April 2025 capstone implementation at commit
[`1ad5cc0`](https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant/tree/1ad5cc08cbebdeae655cad626393364b2f476556).
The report documents engineering tests and historical timing records; it does
not establish that hybrid retrieval improves factuality, retrieval recall, or
answer quality over graph-only or vector-only baselines.

The current `main` branch is a maintained fork. Reproductions intended to
match the report should begin from the archived commit, while evaluations of
the current software should record the exact Git commit and external artifact
revisions they use.
