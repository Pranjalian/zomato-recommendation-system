import chromadb
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="zomato_restaurants",
            metadata={"hnsw:space": "cosine"}
        )

    def add_restaurants(self, restaurants: List[Dict], embeddings: List[List[float]]):
        """Adds restaurant metadata and their embeddings to the vector store."""
        ids = []
        metadatas = []
        documents = []
        
        for i, rest in enumerate(restaurants):
            rest_id = str(rest.get('id', i))
            ids.append(rest_id)
            
            # Create a string representation for semantic search
            name = rest.get('name', '')
            cuisines = rest.get('cuisines', '')
            location = rest.get('location', '')
            doc_str = f"Restaurant: {name}. Cuisines: {cuisines}. Location: {location}."
            documents.append(doc_str)
            
            # Store metadata for filtering
            # Chroma requires metadata values to be str, int, float, or bool
            meta = {
                "name": str(name),
                "location": str(location),
                "cuisines": str(cuisines)
            }
            metadatas.append(meta)
            
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        print(f"Added {len(ids)} restaurants to Vector Store.")

    def search(self, query_embedding: List[float], n_results: int = 10) -> Dict[str, Any]:
        """Searches the vector store using a query embedding."""
        if not query_embedding:
            return {"ids": [], "metadatas": [], "distances": []}
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    pass
