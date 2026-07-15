# Knowledge Graph RAG design direction

The interface should make retrieval inspectable. A question, its graph and vector evidence, the retrieval trace, and the answer should read as one chain of custody rather than four unrelated dashboard panels.

## Principles

- Keep the conversation, topology, trace, and source excerpts visible in the same workspace.
- Selecting an evidence node selects the same source row and vice versa.
- Use a real graph renderer for topology and interaction; do not approximate graph edges with decorative drawings.
- Keep demo mode explicit and deterministic. Never imply that sample evidence came from a live corpus.
- Favor source excerpts, retrieval scores, and trace details over generic performance charts.
- Preserve the project-record visual language used by the public project page without turning the app into a marketing site.

## Avoid

- Chatbot gradients, floating assistant avatars, glass panels, or empty hero copy.
- Unsupported claims about grounding, factuality, latency, or benchmark quality.
- Graph decoration that cannot be selected, traced, or tied back to source context.
