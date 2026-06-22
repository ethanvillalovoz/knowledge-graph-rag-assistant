import pytest
import numpy as np
from backend.app.handlers.vector_search_handler import VectorSearchHandler


@pytest.fixture
def dummy_embeddings():
    """Fixture to create dummy embeddings for testing."""
    return np.random.random((10, 128)).astype(np.float32)  # 10 vectors of 128 dimensions


@pytest.fixture
def vector_search_handler(dummy_embeddings, tmp_path):
    """Fixture to initialize a VectorSearchHandler with dummy embeddings."""
    embedding_path = tmp_path / "dummy_embeddings.npy"
    index_path = tmp_path / "dummy_index.faiss"
    np.save(embedding_path, dummy_embeddings)
    handler = VectorSearchHandler(
        embedding_path=str(embedding_path),
        index_path=str(index_path),
    )
    handler.build_index(dummy_embeddings)
    return handler


def test_load_embeddings(vector_search_handler, dummy_embeddings):
    loaded_embeddings = vector_search_handler.load_embeddings()
    assert np.array_equal(loaded_embeddings, dummy_embeddings)


def test_build_index(vector_search_handler, dummy_embeddings):
    assert vector_search_handler.index.ntotal == len(dummy_embeddings)


def test_search(vector_search_handler, dummy_embeddings):
    query = np.expand_dims(dummy_embeddings[0], axis=0)
    distances, indices = vector_search_handler.search(query, top_k=3)
    assert len(indices) == 3  # Ensure we get 3 results
    assert distances[0] == max(distances)  # Ensure closest match does have the max similarity score retrieved


def test_vector_search_large_embeddings(tmp_path):
    """Test vector search efficiency on large datasets."""
    large_embeddings = np.random.random((100000, 128)).astype(np.float32)  # 100K vectors
    embedding_path = tmp_path / "large_embeddings.npy"
    index_path = tmp_path / "large_index.faiss"
    handler = VectorSearchHandler(
        embedding_path=str(embedding_path),
        index_path=str(index_path),
    )
    handler.build_index(large_embeddings)

    query = np.expand_dims(large_embeddings[0], axis=0)
    distances, indices = handler.search(query, top_k=5)

    assert len(indices) == 5  # Ensure retrieval of 5 nearest neighbors
    assert max(distances) == distances[0]  # Closest match should have the highest similarity score
