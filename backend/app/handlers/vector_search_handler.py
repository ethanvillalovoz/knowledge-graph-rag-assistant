import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
from backend.app.config import (
    CLEAN_WIKI_DATA_FILE,
    EMBEDDINGS_FILE,
    FAISS_INDEX_FILE,
)

class VectorSearchHandler:
    def __init__(self, embedding_path=EMBEDDINGS_FILE, index_path=FAISS_INDEX_FILE):
        self.embedding_path = embedding_path
        self.index_path = index_path
        self.index = None

        # Initialize model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def load_embeddings(self):
        """Load embeddings from the specified path."""
        if not os.path.exists(self.embedding_path):
            raise FileNotFoundError(f"Embedding file not found: {self.embedding_path}")
        return np.load(self.embedding_path)

    def build_index(self, embeddings):
        """Build a FAISS index with cosine similarity."""
        embeddings_normalized = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  
        self.index.add(embeddings_normalized)
        print(f"Index built with {self.index.ntotal} vectors.")

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

        query_vector_normalized = query_vector / np.linalg.norm(query_vector)
        query_vector_normalized = query_vector_normalized.reshape(1, -1)  # Reshape to 2D (1, d)

        similarities, indices = self.index.search(query_vector_normalized, top_k)

        # Filter results below threshold and remove invalid indices (-1)
        filtered_results = [
            (similarity, index)
            for similarity, index in zip(similarities[0], indices[0])
            if similarity >= similarity_threshold and index != -1
        ]

        if not filtered_results:
            return [], []  # No valid results

        filtered_similarities, filtered_indices = zip(*filtered_results)

        return list(filtered_similarities), list(filtered_indices)
    
    def get_search_results(self, indices, dataset_path=CLEAN_WIKI_DATA_FILE):
        """Get the corresponding texts of the top results."""
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

        original_data = pd.read_parquet(dataset_path)

        if original_data.empty:
            print("Warning: original_data is empty!")
            return []

        # Validate indices
        valid_indices = [i for i in indices if 0 <= i < len(original_data)]
        
        if not valid_indices:
            print(f"Warning: No valid indices found. Received: {indices}")
            print(f"Total rows in dataset: {len(original_data)}")
            print(f"Indices received: {indices}")

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
