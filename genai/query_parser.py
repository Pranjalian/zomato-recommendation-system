import os
from groq import Groq
import json
from dotenv import load_dotenv

class QueryParser:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=api_key)
        # Using a fast and capable model on Groq
        self.model = "llama-3.1-8b-instant"

    def parse_query(self, query: str, context: dict = None) -> dict:
        """
        Takes a natural language query and context, and extracts structured intent.
        """
        prompt = f"""
        You are an AI assistant for a food delivery app. Parse the following user query and extract the key intents, considering the real-time context.
        Return the result as a JSON object with the following keys exactly:
        - "semantic_intent": The core food or craving semantic meaning (e.g., "comforting hot food", "spicy meal").
        - "cuisines": A list of specific cuisines mentioned (e.g., ["Italian", "Chinese"]). Empty list if none.
        - "diet": Any mentioned dietary restrictions (e.g., "vegan", "vegetarian", "gluten-free"). Empty string if none.
        - "is_food_related": Boolean indicating if the query is actually about ordering food.
        
        Context: {json.dumps(context or {})}
        User Query: "{query}"
        
        Output JSON only:
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content
            return json.loads(text.strip())
        except Exception as e:
            print(f"Error parsing query with Groq, using mock fallback: {e}")
            return self._mock_fallback(query)
            
    def _mock_fallback(self, query: str) -> dict:
        """A simple rule-based fallback if the API fails or is missing an API key."""
        query_lower = query.lower()
        
        # Simple extraction rules
        is_food_related = True
        cuisines = []
        if "pizza" in query_lower or "italian" in query_lower:
            cuisines.append("Italian")
        if "chinese" in query_lower or "noodles" in query_lower:
            cuisines.append("Chinese")
            
        diet = ""
        if "vegan" in query_lower:
            diet = "vegan"
        elif "veg" in query_lower:
            diet = "vegetarian"
            
        if "weather" in query_lower or "how are you" in query_lower:
            is_food_related = False
            
        semantic_intent = query  # The best we can do without LLM is use the raw query
        
        return {
            "semantic_intent": semantic_intent,
            "cuisines": cuisines,
            "diet": diet,
            "is_food_related": is_food_related
        }

if __name__ == "__main__":
    # parser = QueryParser()
    # print(parser.parse_query("I'm craving a really spicy vegan curry tonight"))
    pass
