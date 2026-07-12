# Retrieval Benchmarking

The automated suite checks vector-search correctness with a deterministic 10,000-vector fixture. It intentionally does not claim production latency or memory numbers.

For performance work, benchmark the real embedding dimension and corpus on the target deployment hardware. Record:

- corpus size and embedding dimension;
- index type and FAISS build;
- index construction time;
- p50, p95, and p99 query latency;
- peak resident memory;
- recall against a labeled query set.

Keep benchmark results in `docs/performance-stats.md` with the hardware, dataset revision, and exact command used. This prevents a machine-specific stress test from making the portable unit suite flaky.
