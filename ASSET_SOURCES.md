# Asset Sources and Reuse Notes

The root MIT license applies to the repository's source code. It does not
automatically license datasets, papers, reports, photographs, videos, logos,
model artifacts, or other third-party material.

## Project-authored material

- `docs/media/rag-demo.gif`, `rag-demo.mp4`, and `rag-poster.webp` were captured
  from the repository's deterministic interface fixture for this project.
- `docs/media/retrieval-flow.*` and `system-overview-paper.svg` are
  project-authored diagrams.
- `docs/paper/knowledge-graph-rag-technical-report.pdf` and the files under
  `docs/project-report/` and `docs/sprint-reports/` are scholarly or capstone
  records authored by project participants. They are distributed for project
  history, reading, and citation; no broader media license is asserted here.

## Data and model artifacts

- Simple English Wikipedia-derived artifacts are subject to the provenance and
  reuse conditions in [DATA_NOTICE.md](DATA_NOTICE.md).
- The FAISS index and embedding matrix are hosted in a project-owned,
  [documented Hugging Face repository](https://huggingface.co/datasets/ethanvillalovoz/knowledge-graph-rag-retrieval-artifacts).
  Its dataset card preserves the original teammate-hosted repository and
  revision as provenance. Source-corpus limitations and missing historical
  provenance remain applicable even though the mirrored binary files are
  byte-identical and checksum-pinned.
- SentenceTransformers, spaCy, NLTK, DBpedia, OpenAI, and other dependencies or
  services retain their respective licenses and terms.

## Names, logos, and marks

Washington State University, HackerEarth, MECA, GitHub, Hugging Face, and other
names or logos remain the property of their respective owners. Their presence
documents project context and does not imply endorsement or transfer of rights.

## Local PDF collections

The application can ingest user-supplied PDFs. No third-party book chapters or
class materials are distributed as runtime inputs in the maintained source
tree. Users are responsible for ensuring they have permission to process and
redistribute any documents they add locally.
