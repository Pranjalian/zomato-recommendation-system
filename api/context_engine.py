import datetime
import random

class ContextEngine:
    def __init__(self):
        # In a real app, this would connect to weather APIs, location services, etc.
        pass

    def get_current_context(self, user_id: str = None, mock: bool = True, overrides: dict = None) -> dict:
        """
        Retrieves current context for the user (time, weather, location).
        If mock is True, it returns randomized or simulated data.
        """
        now = datetime.datetime.now()
        time_of_day = self._categorize_time(now.hour)
        
        if mock:
            weathers = ["sunny", "raining", "cloudy", "cold", "hot"]
            weather = random.choice(weathers)
        else:
            weather = "unknown" # Would call a weather API here
            
        context = {
            "time_of_day": time_of_day,
            "weather": weather,
            "timestamp": now.isoformat()
        }
        
        if overrides:
            context.update(overrides)
            
        return context
        
    def _categorize_time(self, hour: int) -> str:
        if 5 <= hour < 11:
            return "morning"
        elif 11 <= hour < 15:
            return "lunch"
        elif 15 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "dinner"
        else:
            return "late night"

if __name__ == "__main__":
    # ce = ContextEngine()
    # print(ce.get_current_context())
    pass
