import sys
import os
from typing import List, Dict, Any

# Ensure the root project directory is in the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embeddings.embedder import GeminiEmbedder
from embeddings.vector_store import VectorStore
from database.catalog_db import CatalogDB

class RetrievalEngine:
    def __init__(self, vector_store=None, catalog_db=None, embedder=None):
        self.vector_store = vector_store or VectorStore()
        # CatalogDB requires the path to be correct relative to where it's called
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'zomato_catalog.db')
        self.catalog_db = catalog_db or CatalogDB(db_path)
        self.embedder = embedder or GeminiEmbedder()

    def retrieve_candidates(self, parsed_query: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves candidate restaurants by combining semantic vector search and hard filtering.
        """
        # 1. Generate query embedding
        intent = parsed_query.get('semantic_intent', '')
        if not intent:
            return []
            
        query_emb = self.embedder.generate_query_embedding(intent)
        
        # 2. Semantic Retrieval (Fetch more than top_k to allow for filtering)
        # We fetch 20 to ensure we have enough after hard filters are applied
        search_results = self.vector_store.search(query_emb, n_results=20)
        
        if not search_results or not search_results.get('ids') or not search_results['ids'][0]:
            return []
            
        vector_ids = search_results['ids'][0]
        distances = search_results['distances'][0]
        
        candidates = []
        target_cuisines = [c.lower() for c in parsed_query.get('cuisines', [])]
        target_diet = parsed_query.get('diet', '').lower()
        
        for idx, rest_id_str in enumerate(vector_ids):
            rest_id = int(rest_id_str)
            # Fetch full details from Catalog
            rest_data = self.catalog_db.get_restaurant_by_id(rest_id)
            if not rest_data:
                continue
                
            # Store the semantic distance for ranking later
            rest_data['semantic_distance'] = distances[idx]
            
            # Apply Hard Filters
            if self._passes_filters(rest_data, target_cuisines, target_diet):
                candidates.append(rest_data)
                
            if len(candidates) >= top_k:
                break
                
        # 3. Zero Results Handling (Relax constraints if needed)
        if not candidates and target_cuisines:
            print("Zero results found with strict filters. Relaxing cuisine constraints...")
            # Relax cuisines, but keep diet
            for idx, rest_id_str in enumerate(vector_ids):
                rest_id = int(rest_id_str)
                rest_data = self.catalog_db.get_restaurant_by_id(rest_id)
                if not rest_data:
                    continue
                rest_data['semantic_distance'] = distances[idx]
                
                if self._passes_filters(rest_data, [], target_diet):
                    candidates.append(rest_data)
                if len(candidates) >= top_k:
                    break
                    
        return candidates

    def _passes_filters(self, rest_data: Dict[str, Any], target_cuisines: List[str], target_diet: str) -> bool:
        """
        Checks if a restaurant passes the hard constraints.
        """
        rest_cuisines = rest_data.get('cuisines', '').lower()
        
        # Check Cuisine
        if target_cuisines:
            cuisine_match = False
            for tc in target_cuisines:
                if tc in rest_cuisines:
                    cuisine_match = True
                    break
            if not cuisine_match:
                return False
                
        # Check Diet (Strict)
        # Note: In a real system, you'd check a 'diet' tag or menu items. 
        # For prototype, we check if 'vegan' or 'veg' is in the cuisine or name string
        if target_diet:
            rest_text = (rest_data.get('name', '') + " " + rest_cuisines).lower()
            if target_diet == 'vegan' and 'vegan' not in rest_text and 'veg' not in rest_text:
                return False
            elif target_diet == 'vegetarian' and 'veg' not in rest_text:
                return False
                
        return True
