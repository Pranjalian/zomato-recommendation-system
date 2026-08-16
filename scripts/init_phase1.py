import sys
import os

# Add root directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.dataset_loader import DatasetLoader
from database.catalog_db import CatalogDB
from database.user_db import UserDB

def main():
    print("=== Initializing Phase 1 ===")
    
    # 1. Load Data
    print("Loading dataset...")
    loader = DatasetLoader()
    restaurants = loader.get_restaurants_dict()
    
    if not restaurants:
        print("Failed to load restaurants or empty dataset.")
        return
        
    print(f"Loaded {len(restaurants)} restaurants successfully.")
    
    # 2. Populate Catalog DB
    print("Populating Catalog DB...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'zomato_catalog.db')
    catalog = CatalogDB(db_path)
    catalog.insert_restaurants(restaurants)
    
    # Verify Catalog DB
    all_rests = catalog.get_all_restaurants()
    print(f"Catalog DB now contains {len(all_rests)} records.")
    
    # 3. Initialize User DB
    print("Initializing User DB...")
    user_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'user_profiles.json')
    user_db = UserDB(user_db_path)
    
    # Create a mock user for testing
    user_db.update_user_profile("test_user_1", {
        "explicit_preferences": {
            "allergies": ["peanuts"],
            "diet": "vegetarian"
        }
    })
    
    profile = user_db.get_user_profile("test_user_1")
    if profile:
        print("User DB initialized and mock user created.")
        
    print("=== Phase 1 Completed Successfully ===")

if __name__ == "__main__":
    main()
