# Knowledge Graph RAG Assistant Frontend

React + TypeScript workspace for inspecting generated answers, retrieval stages, and source context.

## Development

```bash
npm ci
npm run dev
```

The app opens at [http://localhost:3000](http://localhost:3000). It uses an explicitly labeled deterministic demo when `VITE_API_BASE_URL` is not set.

To connect the FastAPI service:

```bash
cp .env.example .env.local
```

## Verification

```bash
npm run check
```

See the repository root [README](../../README.md) for full project setup, Docker instructions, and backend details.
