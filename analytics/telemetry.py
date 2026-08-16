from typing import Dict, List
from database.user_db import UserDB
from database.catalog_db import CatalogDB

class TelemetryEngine:
    def __init__(self, user_db: UserDB, catalog_db: CatalogDB):
        self.user_db = user_db
        self.catalog_db = catalog_db

    def log_event(self, user_id: str, event_type: str, restaurant_id: int) -> bool:
        """
        Logs a user event. If the event is an 'order', updates user preferences.
        Returns True if successfully processed.
        """
        if event_type not in ["click", "order"]:
            print(f"Telemetry: Unknown event type: {event_type}")
            return False
            
        print(f"Telemetry: Logged '{event_type}' for user '{user_id}' on restaurant '{restaurant_id}'")
        
        # Optionally log to a file
        with open("data/telemetry_events.log", "a") as f:
            f.write(f"{user_id},{event_type},{restaurant_id}\n")
        
        if event_type == "order":
            return self._process_order(user_id, restaurant_id)
            
        return True
        
    def _process_order(self, user_id: str, restaurant_id: int) -> bool:
        restaurant = self.catalog_db.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            print(f"Telemetry: Restaurant {restaurant_id} not found in catalog.")
            return False
            
        # Ensure user exists, if not this will create them
        profile = self.user_db.get_user_profile(user_id)
        if not profile:
            self.user_db.update_user_profile(user_id, {})
            profile = self.user_db.get_user_profile(user_id)
            
        cuisines = restaurant.get("cuisines", [])
        if isinstance(cuisines, str):
            cuisines = [c.strip() for c in cuisines.split(",")]
        
        # Add to historical orders
        self.user_db.add_historical_order(user_id, {"restaurant_id": restaurant_id, "cuisines": cuisines})
        
        # Reload profile after historical order is added to update frequent cuisines
        profile = self.user_db.get_user_profile(user_id)
        implicit_behaviors = profile.get("implicit_behaviors", {})
        freq_cuisines = implicit_behaviors.get("frequent_cuisines", [])
        
        for cuisine in cuisines:
            if cuisine not in freq_cuisines:
                freq_cuisines.append(cuisine)
                
        # Update user profile with new frequent cuisines
        implicit_behaviors["frequent_cuisines"] = freq_cuisines
        self.user_db.update_user_profile(user_id, {"implicit_behaviors": implicit_behaviors})
        print(f"Telemetry: Updated frequent_cuisines for user '{user_id}': {freq_cuisines}")
        return True
