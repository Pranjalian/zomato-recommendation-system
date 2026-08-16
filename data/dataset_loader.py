import pandas as pd
import numpy as np
from typing import List, Dict
import os
import ast

class DatasetLoader:
    def __init__(self, dataset_path: str = "data/zomato.csv"):
        self.dataset_path = dataset_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Loads the Zomato dataset from the provided path."""
        try:
            if not self.dataset_path.startswith("hf://") and not os.path.exists(self.dataset_path):
                print(f"Dataset not found at {self.dataset_path}. Returning empty DataFrame.")
                return pd.DataFrame()
                
            print(f"Loading dataset from {self.dataset_path}...")
            self.df = pd.read_csv(self.dataset_path)
            print(f"Successfully loaded dataset with {len(self.df)} records.")
            return self.df
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return pd.DataFrame()

    def preprocess_data(self) -> pd.DataFrame:
        """Cleans and formats the dataset for our system."""
        if self.df is None:
            self.load_data()
            
        if self.df is None or self.df.empty:
            return pd.DataFrame()

        df_clean = self.df.copy()
        
        # Standardize column names if it's the typical Kaggle Zomato dataset
        if 'approx_cost(for two people)' in df_clean.columns:
            df_clean.rename(columns={'approx_cost(for two people)': 'cost_for_two'}, inplace=True)
            
        # Clean 'rate' column (e.g., '4.1/5', 'NEW', '-')
        if 'rate' in df_clean.columns:
            df_clean['rate'] = df_clean['rate'].astype(str)
            df_clean['rate'] = df_clean['rate'].apply(lambda x: str(x).split('/')[0].strip())
            df_clean['rate'] = df_clean['rate'].replace(['NEW', '-', 'nan'], np.nan)
            df_clean['rate'] = pd.to_numeric(df_clean['rate'], errors='coerce')
            
            # Impute missing ratings with median rating of the location or overall median
            overall_median = df_clean['rate'].median()
            df_clean['rate'] = df_clean['rate'].fillna(overall_median)

        # Clean cost column (remove commas and convert to float)
        if 'cost_for_two' in df_clean.columns:
            df_clean['cost_for_two'] = df_clean['cost_for_two'].astype(str).str.replace(',', '')
            df_clean['cost_for_two'] = pd.to_numeric(df_clean['cost_for_two'], errors='coerce')
            # Drop rows where cost is missing as it's a critical feature
            df_clean = df_clean.dropna(subset=['cost_for_two'])

        # Handle missing coordinates (Mocking them based on location string or generating random within a city if not present)
        # Real dataset might not have lat/lon, we will add dummy ones if they don't exist
        if 'latitude' not in df_clean.columns or 'longitude' not in df_clean.columns:
            # Mocking coordinates for Bengaluru (approx bounding box)
            np.random.seed(42)
            df_clean['latitude'] = np.random.uniform(12.8, 13.1, size=len(df_clean))
            df_clean['longitude'] = np.random.uniform(77.5, 77.8, size=len(df_clean))

        # Fill NaNs in text columns with empty strings
        text_cols = ['name', 'location', 'rest_type', 'cuisines', 'dish_liked']
        for col in text_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna('')

        # Clean menus (if available as strings of lists)
        if 'menu_item' in df_clean.columns:
            def parse_menu(x):
                try:
                    return ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else x
                except:
                    return []
            df_clean['menu_item'] = df_clean['menu_item'].apply(parse_menu)

        # Drop unusable records (e.g., missing name or location)
        if 'name' in df_clean.columns and 'location' in df_clean.columns:
            df_clean = df_clean[(df_clean['name'] != '') & (df_clean['location'] != '')]

        return df_clean
        
    def get_restaurants_dict(self) -> List[Dict]:
        """Returns the preprocessed dataset as a list of dictionaries."""
        df_clean = self.preprocess_data()
        if df_clean.empty:
            return []
        return df_clean.to_dict('records')

if __name__ == "__main__":
    loader = DatasetLoader()
    data = loader.get_restaurants_dict()
    if data:
        print(f"Successfully preprocessed {len(data)} restaurants.")
        print(f"Sample: {data[0]['name'] if 'name' in data[0] else 'Unknown'}")
