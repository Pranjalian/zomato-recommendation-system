import json
import os
from typing import Dict, Optional, List

class UserDB:
    def __init__(self, db_path: str = "database/user_profiles.json"):
        """
        Initializes a mock NoSQL database using a local JSON file to store user profiles.
        This simulates a document-oriented database like MongoDB or Firestore.
        """
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else '.', exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Creates the JSON file if it doesn't exist."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)

    def _load_data(self) -> Dict[str, Dict]:
        """Loads all data from the JSON file."""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_data(self, data: Dict[str, Dict]):
        """Saves data back to the JSON file."""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Retrieves a user profile by ID."""
        data = self._load_data()
        return data.get(user_id)

    def update_user_profile(self, user_id: str, profile_data: Dict):
        """
        Updates or creates a user profile.
        Expects profile_data to contain fields like:
        - explicit_preferences: dict (e.g., allergies, diet)
        - implicit_behaviors: list (e.g., historical orders)
        """
        data = self._load_data()
        
        if user_id not in data:
            data[user_id] = {
                "user_id": user_id,
                "explicit_preferences": {
                    "allergies": [],
                    "diet": "none"
                },
                "implicit_behaviors": {
                    "historical_orders": [],
                    "frequent_cuisines": []
                }
            }
            
        # Update fields recursively or just overwrite for prototype
        # We will do a simple shallow update for prototype simplicity
        for key, value in profile_data.items():
            if isinstance(value, dict) and key in data[user_id]:
                data[user_id][key].update(value)
            else:
                data[user_id][key] = value
                
        self._save_data(data)

    def add_historical_order(self, user_id: str, order_details: Dict):
        """Appends a new order to the user's implicit behaviors."""
        data = self._load_data()
        if user_id in data:
            if "implicit_behaviors" not in data[user_id]:
                data[user_id]["implicit_behaviors"] = {}
            if "historical_orders" not in data[user_id]["implicit_behaviors"]:
                data[user_id]["implicit_behaviors"]["historical_orders"] = []
                
            data[user_id]["implicit_behaviors"]["historical_orders"].append(order_details)
            self._save_data(data)

if __name__ == "__main__":
    # Example Usage
    db = UserDB("user_profiles.json")
    db.update_user_profile("user_123", {
        "explicit_preferences": {
            "allergies": ["peanuts"],
            "diet": "vegan"
        }
    })
    print(db.get_user_profile("user_123"))
