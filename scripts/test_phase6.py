import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from api.main import app, user_db, catalog_db
import json

client = TestClient(app)

def test_telemetry():
    print("=== Testing Phase 6: Telemetry & Feedback Loop ===")
    
    test_user_id = "test_telemetry_user"
    
    # 1. Reset user profile
    user_db.update_user_profile(test_user_id, {
        "explicit_preferences": {"allergies": [], "diet": "none"},
        "implicit_behaviors": {"historical_orders": [], "frequent_cuisines": []}
    })
    
    # Verify initial state
    initial_profile = user_db.get_user_profile(test_user_id)
    print(f"\nInitial frequent_cuisines: {initial_profile['implicit_behaviors']['frequent_cuisines']}")
    
    # We will log an order for restaurant ID 1
    restaurant = catalog_db.get_restaurant_by_id(1)
    if not restaurant:
        print("\nError: Restaurant ID 1 not found in CatalogDB. Cannot proceed with telemetry test.")
        return
        
    print(f"\nTarget Restaurant ID 1 Cuisines: {restaurant.get('cuisines', [])}")
    
    # 2. Send Feedback Request
    payload = {
        "user_id": test_user_id,
        "event_type": "order",
        "restaurant_id": 1
    }
    
    print(f"\nSending POST request to /feedback with payload:\n{json.dumps(payload, indent=2)}")
    response = client.post("/feedback", json=payload)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    # 3. Verify user profile was updated
    updated_profile = user_db.get_user_profile(test_user_id)
    final_cuisines = updated_profile['implicit_behaviors'].get('frequent_cuisines', [])
    print(f"\nUpdated frequent_cuisines: {final_cuisines}")
    
    # Assert
    assert response.status_code == 200, "Expected status code 200"
    assert len(final_cuisines) > 0, "frequent_cuisines should not be empty after an order"
    
    # Expected cuisines (restaurant 1 is Jalsa which is North Indian, Mughlai, Chinese)
    # Check if any of them were added
    cuisines_from_db = restaurant.get("cuisines", [])
    if isinstance(cuisines_from_db, str):
        cuisines_from_db = [c.strip() for c in cuisines_from_db.split(",")]
        
    for c in cuisines_from_db:
        assert c in final_cuisines, f"Expected {c} to be in user's frequent_cuisines"
        
    print("\nSUCCESS! Telemetry successfully captured feedback and updated the UserDB.")

if __name__ == "__main__":
    test_telemetry()
