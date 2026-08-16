import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.context_engine import ContextEngine
from genai.query_parser import QueryParser
from engine.retrieval import RetrievalEngine
from engine.ranking import RankingEngine
from database.user_db import UserDB

def main():
    print("=== Testing Phase 4: Recommendation Engine ===")
    
    # 1. Initialize all modules
    print("\n1. Initializing modules...")
    context_engine = ContextEngine()
    query_parser = QueryParser()
    retrieval_engine = RetrievalEngine()
    ranking_engine = RankingEngine()
    
    user_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'user_profiles.json')
    user_db = UserDB(user_db_path)
    
    user_profile = user_db.get_user_profile("test_user_1")
    if user_profile:
        # Add a frequent cuisine for testing ranking boost
        user_profile['implicit_behaviors']['frequent_cuisines'] = ["Chinese"]
    else:
        user_profile = {}

    # 2. Set up test scenario
    # A user wants spicy food on a rainy day.
    test_query = "I want a spicy chinese dish"
    mock_context_override = {"weather": "rainy", "time_of_day": "dinner"}
    
    print(f"\n2. Scenario:")
    print(f"   Query: '{test_query}'")
    print(f"   Context: {mock_context_override}")
    print(f"   User Profile (frequent cuisines): {user_profile.get('implicit_behaviors', {}).get('frequent_cuisines', [])}")
    
    # 3. Execution Pipeline
    context = context_engine.get_current_context(overrides=mock_context_override)
    parsed_query = query_parser.parse_query(test_query, context=context)
    
    print(f"\n3. Parsed Query from Phase 3:\n{json.dumps(parsed_query, indent=2)}")
    
    print("\n4. Phase 4 Retrieval Engine executing...")
    candidates = retrieval_engine.retrieve_candidates(parsed_query, top_k=5)
    print(f"   Retrieved {len(candidates)} candidates.")
    for c in candidates:
        print(f"   - {c.get('name')} (Semantic Dist: {c.get('semantic_distance', 0):.4f})")
        
    print("\n5. Phase 4 Ranking Engine executing...")
    ranked_candidates = ranking_engine.rank_candidates(candidates, parsed_query, context, user_profile)
    
    print("\n=== Final Ranked Recommendations ===")
    for idx, c in enumerate(ranked_candidates):
        boost_reason = c.get('explain_boost', 'Good match.')
        print(f"{idx+1}. {c.get('name')} | Score: {c.get('final_score'):.4f} | Cuisines: {c.get('cuisines')}")
        print(f"   Reason: {boost_reason}")

if __name__ == "__main__":
    main()
