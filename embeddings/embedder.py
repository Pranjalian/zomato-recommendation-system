from typing import List
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

class Embedder:
    def __init__(self):
        # Using DefaultEmbeddingFunction (all-MiniLM-L6-v2) for fast, free local embeddings
        self.embed_func = DefaultEmbeddingFunction()

    def generate_embedding(self, text: str) -> List[float]:
        """Generates an embedding vector for a single string."""
        if not text:
            return [0.0] * 384
            
        try:
            return self.embed_func([text])[0]
        except Exception as e:
            print(f"Error generating embedding, using mock: {e}")
            return [0.0] * 384
            
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generates an embedding for a user query."""
        if not query:
            return [0.0] * 384
            
        try:
            return self.embed_func([query])[0]
        except Exception as e:
            print(f"Error generating query embedding, using mock: {e}")
            return [0.0] * 384
