# Changelog

## Unreleased

- Migrated the pinned retrieval-artifact dependency to a documented,
  project-owned Hugging Face dataset while preserving the original teammate
  repository and revision as provenance.
- Refined public documentation for the maintained fork of the WSU capstone project.
- Added contribution, security, environment, Docker ignore, and repository hygiene files.
- Improved Docker Compose and GitHub Actions configuration for fork-based builds.
- Added the publication-style technical report, system-overview figure, citation metadata, and an explicit paper-to-code reproducibility boundary.
- Pinned and checksum-verified the embedding matrix and FAISS index used by the maintained setup.
- Removed historical third-party PDF inputs and their derived parquet from the maintained public tree while preserving local PDF ingestion.
- Added data and media provenance documentation plus monthly dependency-update configuration.
- Published commit-addressable container tags and made the publishing workflow build the exact commit that passed CI.
