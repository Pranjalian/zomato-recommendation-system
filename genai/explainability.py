import os
from typing import Dict, Any

# We use the old google.generativeai for now to avoid large refactoring across the prototype,
# but acknowledging the FutureWarning logged during testing.
import google.generativeai as genai

from dotenv import load_dotenv

class ExplainabilityEngine:
    def __init__(self):
        # Configure Gemini if API key is present
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-3.6-flash')
        else:
            self.model = None

    def generate_explanation(
        self, 
        candidate: Dict[str, Any], 
        parsed_query: Dict[str, Any], 
        context: Dict[str, Any], 
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Generates a natural language explanation for why a candidate was recommended.
        """
        if not self.model:
            return self._mock_fallback(candidate, parsed_query, context, user_profile)

        # Construct prompt
        intent = parsed_query.get('semantic_intent', '')
        name = candidate.get('name', '')
        cuisines = candidate.get('cuisines', '')
        boost_reason = candidate.get('explain_boost', '')
        
        weather = context.get('weather', '')
        time_of_day = context.get('time_of_day', '')
        
        prompt = f"""
        You are a friendly and concise AI food recommendation assistant for Zomato.
        A user asked for: "{intent}"
        Current Context: Time: {time_of_day}, Weather: {weather}.
        
        We are recommending the restaurant "{name}" which serves "{cuisines}".
        Our internal engine gave this reason for boosting its score: "{boost_reason}"
        
        Write a 1-2 sentence friendly explanation of why we are recommending "{name}" to the user.
        Make it sound natural and use the context and boost reason. Do not mention the word "engine" or "boost".
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating explanation with Gemini: {e}")
            return self._mock_fallback(candidate, parsed_query, context, user_profile)

    def _mock_fallback(
        self, 
        candidate: Dict[str, Any], 
        parsed_query: Dict[str, Any], 
        context: Dict[str, Any], 
        user_profile: Dict[str, Any]
    ) -> str:
        """
        Deterministic template-based fallback if GenAI fails.
        """
        name = candidate.get('name', 'This restaurant')
        boost_reason = candidate.get('explain_boost', 'It is a great match for your query.')
        weather = context.get('weather', '')
        
        explanation = f"We recommend {name}. {boost_reason}"
        if weather in ['rainy', 'cold'] and "weather" not in boost_reason:
             explanation += f" Perfect for a {weather} day."
             
        return explanation
