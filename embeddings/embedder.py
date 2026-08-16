import os
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

class GeminiEmbedder:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        # Using the standard embedding model
        self.model_name = 'models/gemini-embedding-001'

    def generate_embedding(self, text: str) -> List[float]:
        """Generates an embedding vector for a single string."""
        if not text:
            # Return a zero vector of size 768 (Gemini standard)
            return [0.0] * 768
            
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding'][:768]
        except Exception as e:
            print(f"Error generating embedding, using mock: {e}")
            import hashlib
            import random
            # Generate a deterministic mock embedding based on text hash
            random.seed(hashlib.md5(text.encode()).hexdigest())
            return [random.uniform(-1, 1) for _ in range(768)]
            
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generates an embedding for a user query."""
        if not query:
            return [0.0] * 768
            
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding'][:768]
        except Exception as e:
            print(f"Error generating query embedding, using mock: {e}")
            import hashlib
            import random
            random.seed(hashlib.md5(query.encode()).hexdigest())
            return [random.uniform(-1, 1) for _ in range(768)]

if __name__ == "__main__":
    # embedder = GeminiEmbedder()
    # print(embedder.generate_embedding("Delicious spicy food"))
    pass
