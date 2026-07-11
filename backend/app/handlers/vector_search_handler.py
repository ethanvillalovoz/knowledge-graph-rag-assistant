import os

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from backend.app.config import (
    CLEAN_WIKI_DATA_FILE,
    EMBEDDINGS_FILE,
    FAISS_INDEX_FILE,
)


class VectorSearchHandler:
    def __init__(
        self,
        embedding_path=EMBEDDINGS_FILE,
        index_path=FAISS_INDEX_FILE,
        model=None,
    ):
        self.embedding_path = embedding_path
        self.index_path = index_path
        self.index = None
        self._model = model

    @property
    def model(self):
        """Load the embedding model only when a query needs encoding."""
        if self._model is None:
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._model

    def load_embeddings(self):
        """Load embeddings from the specified path."""
        if not os.path.exists(self.embedding_path):
            raise FileNotFoundError(f"Embedding file not found: {self.embedding_path}")
        return np.load(self.embedding_path)

    def build_index(self, embeddings):
        """Build a FAISS index with cosine similarity."""
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        if np.any(norms == 0):
            raise ValueError("Embeddings must not contain zero-length vectors.")

        embeddings_normalized = embeddings / norms
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings_normalized)

        index_dir = os.path.dirname(self.index_path)
        if index_dir:
            os.makedirs(index_dir, exist_ok=True)
        faiss.write_index(self.index, self.index_path)

    def load_index(self):
        """Load an existing FAISS index."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Index file not found: {self.index_path}")
        self.index = faiss.read_index(self.index_path)

    def embed_query(self, query):
        """Generate an embedding for the query."""
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        
        return query_embedding
   
    def search(self, query_vector, top_k=10, similarity_threshold=0.5):
        """Search the FAISS index with normalized query vector."""
        if self.index is None:
            raise ValueError("Index is not loaded. Build or load an index first.")

        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            raise ValueError("Query vector must not be zero length.")

        query_vector_normalized = query_vector / query_norm
        query_vector_normalized = query_vector_normalized.reshape(1, -1)

        similarities, indices = self.index.search(query_vector_normalized, top_k)

        filtered_results = [
            (similarity, index)
            for similarity, index in zip(similarities[0], indices[0])
            if similarity >= similarity_threshold and index != -1
        ]

        if not filtered_results:
            return [], []

        filtered_similarities, filtered_indices = zip(*filtered_results)

        return list(filtered_similarities), list(filtered_indices)
    
    def get_search_results(self, indices, dataset_path=CLEAN_WIKI_DATA_FILE):
        """Get the corresponding texts of the top results."""
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

        original_data = pd.read_parquet(dataset_path)

        if original_data.empty:
            return []

        valid_indices = [i for i in indices if 0 <= i < len(original_data)]
        
        if not valid_indices:
            return []

        return original_data.iloc[valid_indices]["text"].tolist()

# Example Usage
if __name__ == "__main__":
    handler = VectorSearchHandler()

    embeddings = handler.load_embeddings()
    handler.build_index(embeddings)

    example_query_text = "How many people in Guatemala are Native American?"
    example_query_vector = handler.embed_query(example_query_text)
    similarities, indices = handler.search(example_query_vector)

    vector_search_texts = handler.get_search_results(indices)
    for result_num, result in enumerate(vector_search_texts):
        print(f"Result {result_num + 1}: {result}\n\n")
