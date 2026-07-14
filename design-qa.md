# Knowledge Graph RAG design QA

## Direction

- Preserve the research-workbench format: query on the left, inspectable topology and evidence on the right.
- Keep the project visibly different from a generic chat product by making retrieval state the primary interface.
- Reference capture: `/Users/ethanvillalovoz/Documents/Codex/2026-07-09/files-mentioned-by-the-user-agents/outputs/rag-design-qa/rag-current.png`.

## Visual review

- The completed retrieval state keeps the question, grounded answer, source nodes, trace, and excerpts simultaneously inspectable.
- Node colors identify retrieval roles without turning the page into a decorative palette.
- The deterministic demo disclosure is explicit and the interface does not present fixture output as a live evaluation.
- The original-size completed-state capture confirms the graph nodes and connectors are fully visible.

## Functional review

- Suggested questions run the full deterministic retrieval flow.
- A completed query renders an answer, three evidence records, and four retrieval stages.
- Desktop and 390 x 844 mobile layouts have no horizontal overflow.
- Browser console contains no warnings or errors.
- `npm run check` passes two Vitest tests, TypeScript, and the Vite production build.

final result: passed
