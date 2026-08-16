from typing import List, Dict, Any

class RankingEngine:
    def rank_candidates(
        self, 
        candidates: List[Dict[str, Any]], 
        parsed_query: Dict[str, Any], 
        context: Dict[str, Any], 
        user_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Scores and sorts the retrieved candidates based on semantic distance,
        contextual factors, and user preferences.
        """
        ranked_candidates = []
        
        # User implicit behaviors
        implicit_behaviors = user_profile.get("implicit_behaviors", {}) if user_profile else {}
        historical_orders = implicit_behaviors.get("historical_orders", [])
        
        # Extract historically ordered restaurant names or cuisines to boost them
        favorite_cuisines = implicit_behaviors.get("frequent_cuisines", [])
        
        weather = context.get('weather', '').lower()
        time_of_day = context.get('time_of_day', '').lower()

        for candidate in candidates:
            # 1. Base Score
            # ChromaDB cosine distance: lower is better (0 is exact match)
            # We invert it for scoring: 1 / (1 + distance)
            distance = candidate.get('semantic_distance', 1.0)
            base_score = 1.0 / (1.0 + distance)
            
            score = base_score
            
            rest_cuisines = candidate.get('cuisines', '').lower()
            rest_name = candidate.get('name', '').lower()
            
            # 2. Contextual Boosts
            # If it's cold/rainy, boost comforting/hot cuisines
            if weather in ['rainy', 'cold']:
                if 'soup' in rest_cuisines or 'chinese' in rest_cuisines or 'thai' in rest_cuisines:
                    score += 0.15
                    candidate['explain_boost'] = "Perfect for this weather."
                    
            # If it's morning, boost cafes/bakeries
            if time_of_day == 'morning':
                if 'cafe' in rest_cuisines or 'bakery' in rest_cuisines or 'breakfast' in rest_cuisines:
                    score += 0.15
                    candidate['explain_boost'] = "Great for breakfast."
            
            # 3. User Preference Boosts
            for fav_cuisine in favorite_cuisines:
                if fav_cuisine.lower() in rest_cuisines:
                    score += 0.1
                    candidate['explain_boost'] = "Matches your favorite cuisines."
                    break
                    
            candidate['final_score'] = score
            ranked_candidates.append(candidate)
            
        # Sort descending by final score
        ranked_candidates.sort(key=lambda x: x.get('final_score', 0.0), reverse=True)
        
        return ranked_candidates
