# Data Notice

The `data-v1` release assets are derived from Simple English Wikipedia content prepared during the original Washington State University capstone. They are distributed separately from the source code for research reproducibility and are not covered by this repository's MIT license.

Wikipedia text is available under the [Creative Commons Attribution-ShareAlike License](https://creativecommons.org/licenses/by-sa/4.0/) and, where applicable, the [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html). Reuse of the corpus must preserve the attribution and share-alike obligations that apply to the source material.

The exact Wikipedia snapshot date was not preserved in the original project record. Treat that missing provenance as a limitation when using these artifacts for evaluation or comparison. The files are provided as-is and should not be interpreted as a maintained or comprehensive encyclopedia dataset.

The separately hosted `text_embeddings.npy` and `index.faiss` files are pinned
to project-owned Hugging Face dataset revision
[`550aca04b1a6f7d2f64e57ec304b62f8c9ea1d62`](https://huggingface.co/datasets/ethanvillalovoz/knowledge-graph-rag-retrieval-artifacts/tree/550aca04b1a6f7d2f64e57ec304b62f8c9ea1d62)
in the maintained setup. This documented mirror preserves the original
`miverson9/acme10-he-ragapp-embeddings` repository and revision as provenance.
Pinning and checksumming the mirrored binaries detects later mutation; it does
not recover the missing source-snapshot date, passage-construction environment,
or all model runtime controls from the original capstone.

Historical Requirements Engineering book chapters and their derived local PDF
parquet are not part of the maintained public runtime inputs. The application
continues to support user-supplied PDF collections, but users must provide
documents they are authorized to process and redistribute. See
[ASSET_SOURCES.md](ASSET_SOURCES.md) for the boundary between the software
license and other project material.
