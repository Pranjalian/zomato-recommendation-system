import sys
import os

# Add root directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.catalog_db import CatalogDB
from embeddings.embedder import GeminiEmbedder
from embeddings.vector_store import VectorStore

def main():
    print("=== Initializing Phase 2 ===")
    
    # 1. Load restaurants from Catalog DB
    print("Fetching restaurants from Catalog DB...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'zomato_catalog.db')
    catalog = CatalogDB(db_path)
    restaurants = catalog.get_all_restaurants()
    
    if not restaurants:
        print("No restaurants found in Catalog DB. Please run Phase 1 first.")
        return
        
    print(f"Fetched {len(restaurants)} restaurants.")
    
    # 2. Generate Embeddings
    print("Generating embeddings (this may take a moment)...")
    embedder = GeminiEmbedder()
    embeddings = []
    
    for rest in restaurants:
        name = rest.get('name', '')
        cuisines = rest.get('cuisines', '')
        location = rest.get('location', '')
        dish_liked = rest.get('dish_liked', '')
        # A rich string for embedding to capture semantics
        doc_str = f"Restaurant {name} located in {location}. Serves {cuisines}. Popular for {dish_liked}."
        emb = embedder.generate_embedding(doc_str)
        embeddings.append(emb)
        
    # 3. Store in Vector DB
    print("Storing embeddings in Vector DB...")
    chroma_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chroma_db')
    vector_store = VectorStore(db_path=chroma_path)
    
    vector_store.add_restaurants(restaurants, embeddings)
    
    # 4. Test semantic search
    print("\nTesting Semantic Search...")
    test_query = "I want some spicy pizza in Koramangala"
    query_emb = embedder.generate_query_embedding(test_query)
    results = vector_store.search(query_emb, n_results=2)
    
    print(f"Top results for '{test_query}':")
    for meta in results.get('metadatas', [[]])[0]:
        print(f"- {meta.get('name')} in {meta.get('location')} ({meta.get('cuisines')})")
        
    print("\n=== Phase 2 Completed Successfully ===")

if __name__ == "__main__":
    main()
