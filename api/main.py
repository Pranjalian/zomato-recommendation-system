import sys
import os

# Set Gemini API Key (ensure this is provided in your environment variables)
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from api.context_engine import ContextEngine
from genai.query_parser import QueryParser
from genai.explainability import ExplainabilityEngine
from engine.retrieval import RetrievalEngine
from engine.ranking import RankingEngine
from database.user_db import UserDB
from database.catalog_db import CatalogDB
from analytics.telemetry import TelemetryEngine

app = FastAPI(title="Zomato GenAI Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
context_engine = ContextEngine()
query_parser = QueryParser()
retrieval_engine = RetrievalEngine()
ranking_engine = RankingEngine()
explainability_engine = ExplainabilityEngine()

# Use DATA_DIR from environment if available (useful for Railway volumes)
data_dir = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database'))

catalog_db_path = os.path.join(data_dir, 'zomato_catalog.db')
catalog_db = CatalogDB(catalog_db_path)

user_db_path = os.path.join(data_dir, 'user_profiles.json')
user_db = UserDB(user_db_path)

telemetry_engine = TelemetryEngine(user_db, catalog_db)

class RecommendRequest(BaseModel):
    user_id: str
    query: str
    context_overrides: Optional[Dict[str, Any]] = None
    top_k: Optional[int] = 3

class RecommendResponse(BaseModel):
    restaurant_id: int
    name: str
    cuisines: str
    score: float
    explanation: str

class FeedbackRequest(BaseModel):
    user_id: str
    event_type: str
    restaurant_id: int

class ProfileRequest(BaseModel):
    user_id: str
    explicit_preferences: Dict[str, Any]

@app.post("/recommend", response_model=List[RecommendResponse])
def recommend(request: RecommendRequest):
    # 1. User Profile
    user_profile = user_db.get_user_profile(request.user_id)
    if not user_profile:
        user_profile = {} # Fallback to empty profile
        
    # 2. Context
    context = context_engine.get_current_context(
        user_id=request.user_id, 
        overrides=request.context_overrides
    )
    
    # 3. Query Parsing
    parsed_query = query_parser.parse_query(request.query, context=context)
    
    # Check if out of domain
    if not parsed_query.get('is_food_related', True):
        raise HTTPException(status_code=400, detail="Query is not related to food or restaurants.")
        
    # 4. Retrieval
    # We retrieve a few extra candidates to rank
    candidates = retrieval_engine.retrieve_candidates(parsed_query, top_k=10)
    if not candidates:
        return []
        
    # 5. Ranking
    ranked_candidates = ranking_engine.rank_candidates(
        candidates, parsed_query, context, user_profile
    )
    
    # Take top K
    top_candidates = ranked_candidates[:request.top_k]
    
    # 6. Explainability
    results = []
    for candidate in top_candidates:
        explanation = explainability_engine.generate_explanation(
            candidate, parsed_query, context, user_profile
        )
        
        results.append(RecommendResponse(
            restaurant_id=candidate.get('id', 0),
            name=candidate.get('name', ''),
            cuisines=candidate.get('cuisines', ''),
            score=candidate.get('final_score', 0.0),
            explanation=explanation
        ))
        
    return results

@app.post("/feedback")
def feedback(request: FeedbackRequest):
    success = telemetry_engine.log_event(
        user_id=request.user_id,
        event_type=request.event_type,
        restaurant_id=request.restaurant_id
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to process feedback event.")
    return {"status": "success", "message": "Feedback logged successfully."}

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    profile = user_db.get_user_profile(user_id)
    if not profile:
        return {
            "user_id": user_id,
            "explicit_preferences": {"diet": "none", "allergies": []},
            "implicit_behaviors": {"historical_orders": [], "frequent_cuisines": []}
        }
    return profile

@app.post("/profile")
def update_profile(request: ProfileRequest):
    user_db.update_user_profile(request.user_id, {
        "explicit_preferences": request.explicit_preferences
    })
    return {"status": "success", "message": "Profile updated successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
