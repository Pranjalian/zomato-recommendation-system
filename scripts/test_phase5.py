import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

client = TestClient(app)

def run_tests():
    print("=== Testing Phase 5: Explainability & API Gateway ===\n")
    
    payload = {
        "user_id": "test_user_1",
        "query": "I am feeling cold and want a spicy chinese dish",
        "context_overrides": {
            "weather": "cold",
            "time_of_day": "evening"
        },
        "top_k": 2
    }
    
    print("Sending POST request to /recommend with payload:")
    import json
    print(json.dumps(payload, indent=2))
    
    response = client.post("/recommend", json=payload)
    
    if response.status_code == 200:
        print("\nResponse Status: 200 OK")
        print("\nRecommendations Received:")
        results = response.json()
        for idx, rec in enumerate(results):
            print(f"\n{idx+1}. {rec['name']} (Score: {rec['score']:.4f})")
            print(f"   Cuisines: {rec['cuisines']}")
            print(f"   Explanation: {rec['explanation']}")
    else:
        print(f"\nError! Status Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    run_tests()
