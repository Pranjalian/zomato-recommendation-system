import sys
import os
import json

# Add root directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.context_engine import ContextEngine
from genai.query_parser import QueryParser

def main():
    print("=== Testing Phase 3: GenAI Integration ===")
    
    # 1. Test Context Engine
    print("\n--- Testing Context Engine ---")
    context_engine = ContextEngine()
    current_context = context_engine.get_current_context()
    print("Current Context:", json.dumps(current_context, indent=2))
    
    mocked_context = context_engine.get_current_context(mock=True)
    # Let's force a weather override using the code we know exists
    # Wait, the code in context_engine.py had a slightly different signature than my plan
    # It has `get_current_context(user_id=None, mock=True)`
    
    print("\n--- Testing Query Parser ---")
    parser = QueryParser()
    
    test_queries = [
        "I want a really spicy vegan pizza for dinner",
        "Just a cheap chinese takeout",
        "What is the weather like?"
    ]
    
    for q in test_queries:
        print(f"\nQuery: '{q}'")
        result = parser.parse_query(q, context=current_context)
        print("Parsed Output:", json.dumps(result, indent=2))
        
    print("\n=== Phase 3 Testing Completed ===")

if __name__ == "__main__":
    main()
