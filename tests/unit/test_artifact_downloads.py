from scripts import download_retrieval_artifacts


def test_retrieval_artifacts_use_an_immutable_revision():
    revision = download_retrieval_artifacts.DATASET_REVISION

    assert len(revision) == 40
    assert all(character in "0123456789abcdef" for character in revision)
    assert f"/resolve/{revision}" in download_retrieval_artifacts.DATASET_BASE_URL

    artifacts = {
        artifact.filename: artifact
        for artifact in download_retrieval_artifacts.ARTIFACTS
    }
    assert set(artifacts) == {"text_embeddings.npy", "index.faiss"}
    assert all(len(artifact.sha256) == 64 for artifact in artifacts.values())
    assert artifacts["text_embeddings.npy"].destination.parent.name == (
        "embeddings_data"
    )
    assert artifacts["index.faiss"].destination.parent.name == "vector_search_data"


def test_retrieval_artifact_hashing(tmp_path):
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"knowledge-graph-rag")

    assert download_retrieval_artifacts.sha256(artifact) == (
        "771fed8e248bfe293cf6e8e9f13a5ade2bb4a2d25faa217fab3d91dd0d927da8"
    )
