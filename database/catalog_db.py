import sqlite3
import json
from typing import List, Dict, Optional
import os

class CatalogDB:
    def __init__(self, db_path: str = "database/zomato_catalog.db"):
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else '.', exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database with necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Restaurants table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT,
                cuisines TEXT,
                rating REAL,
                cost_for_two REAL,
                latitude REAL,
                longitude REAL,
                raw_data TEXT
            )
        ''')
        
        # Create indexes for faster filtering
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON restaurants(location)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rating ON restaurants(rating)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cost ON restaurants(cost_for_two)')
        
        conn.commit()
        conn.close()

    def insert_restaurants(self, restaurants_data: List[Dict]):
        """Inserts a batch of restaurants into the database."""
        if not restaurants_data:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for rest in restaurants_data:
            # We store the raw JSON string as a fallback for all extra fields like menu, reviews, etc.
            cursor.execute('''
                INSERT INTO restaurants (name, location, cuisines, rating, cost_for_two, latitude, longitude, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                rest.get('name', 'Unknown'),
                rest.get('location', ''),
                rest.get('cuisines', ''),
                rest.get('rate', None),
                rest.get('cost_for_two', None),
                rest.get('latitude', None),
                rest.get('longitude', None),
                json.dumps(rest)
            ))
            
        conn.commit()
        conn.close()

    def get_all_restaurants(self) -> List[Dict]:
        """Retrieves all restaurants."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT raw_data FROM restaurants")
        rows = cursor.fetchall()
        conn.close()
        
        return [json.loads(row[0]) for row in rows]
        
    def get_restaurant_by_id(self, rest_id: int) -> Optional[Dict]:
        """Retrieves a single restaurant by its internal ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT raw_data FROM restaurants WHERE id = ?", (rest_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            rest = json.loads(row[0])
            rest['internal_id'] = rest_id
            return rest
        return None
        
    def filter_restaurants(self, min_rating: float = None, max_cost: float = None) -> List[Dict]:
        """Example method to filter restaurants using SQL directly."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT raw_data, id FROM restaurants WHERE 1=1"
        params = []
        
        if min_rating is not None:
            query += " AND rating >= ?"
            params.append(min_rating)
            
        if max_cost is not None:
            query += " AND cost_for_two <= ?"
            params.append(max_cost)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            data = json.loads(row[0])
            data['internal_id'] = row[1]
            results.append(data)
            
        return results

if __name__ == "__main__":
    db = CatalogDB("zomato_catalog.db")
    print("Catalog DB Initialized.")
