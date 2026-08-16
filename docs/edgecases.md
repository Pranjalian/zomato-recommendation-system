# Edge Cases: Zomato GenAI Recommendation System Prototype

This document outlines potential edge cases, risks, and failure modes for the Zomato GenAI Recommendation System, based on the architecture and problem statement. Identifying these early ensures a more robust implementation.

## 1. GenAI & Query Understanding Edge Cases
*   **Vague or Unrelated Queries:** The user inputs a query unrelated to food (e.g., "What's the weather today?", "Tell me a joke").
    *   *Mitigation:* The `QueryParser` needs a fallback mechanism to identify non-food intents and return a polite error message ("I can only help you find food!").
*   **Contradictory Intents:** The user inputs conflicting constraints (e.g., "I want a cheap, high-end fine dining experience" or "Vegan steakhouse").
    *   *Mitigation:* The parser must identify the contradiction or prioritize one aspect over the other based on historical data.
*   **LLM Hallucinations:** The explainability module generates a reason for recommendation that is factually incorrect (e.g., claiming a restaurant has vegan options when it doesn't).
    *   *Mitigation:* Ground the prompt strictly in the structured data retrieved from the catalog DB.
*   **API Latency & Rate Limits:** The Gemini API might experience high latency or hit rate limits, slowing down the recommendation process.
    *   *Mitigation:* Implement caching for common queries and fallback to basic semantic search without GenAI parsing if the API fails.

## 2. Recommendation & Retrieval Edge Cases
*   **The "Cold Start" Problem:** A new user with no historical data, or a brand new restaurant with no reviews.
    *   *Mitigation:* Rely heavily on the real-time context (weather, time) and generic popular items until sufficient user interaction data is collected.
*   **Zero Results Found (Over-constraining):** The user applies too many strict filters (e.g., "Vegan, open at 4 AM, within 1km, under ₹100"), resulting in an empty vector search result.
    *   *Mitigation:* Gradually relax constraints (e.g., expand the radius to 3km, remove the price cap) and inform the user in the explanation.
*   **Filter Bubbles (Over-personalization):** The system continuously recommends the exact same type of food, never letting the user discover new cuisines, reinforcing the "habitual ordering" problem.
    *   *Mitigation:* Inject a small percentage of "exploration" or "wildcard" recommendations (e.g., 1 out of 5 recommendations is slightly outside the user's usual profile).

## 3. Data & Context Engine Edge Cases
*   **Missing or Inaccurate Context:** The user denies location permissions, or the weather API is down.
    *   *Mitigation:* Provide recommendations based on time-of-day and generic popularity. Ask the user for manual location input.
*   **Stale Data:** The vector database suggests a restaurant that has recently closed permanently or is currently out of stock of the requested item.
    *   *Mitigation:* Ensure a pre-filtering step checks real-time operational status from the `catalog_db` *before* passing candidates to the LLM for explanation.
*   **Dataset Inconsistencies:** The Zomato CSV dataset might contain missing fields (e.g., null ratings, missing coordinates).
    *   *Mitigation:* The `dataset_loader.py` must handle nulls gracefully, imputing average values or dropping unusable records.

## 4. UI & Explainability Edge Cases
*   **Overwhelming Explanations:** The GenAI generates a paragraph of text, which is too long for a mobile app interface.
    *   *Mitigation:* Enforce strict length limits in the `ExplainabilityModule` prompt (e.g., "Maximum 2 sentences. Max 20 words.").
*   **Inappropriate Explanations:** The LLM generates a culturally insensitive or tone-deaf explanation.
    *   *Mitigation:* Add safety guardrails and content moderation settings to the Gemini API configuration.

## 5. Telemetry & Feedback Edge Cases (Phase 6)
*   **Feedback Loop Stagnation (Echo Chamber):** The ranking model overly weights past behavior, making it impossible for the user to break out of historical preferences.
    *   *Mitigation:* Apply a time-decay factor to older user interactions and ensure the exploration wildcard injection rate remains active.
*   **Telemetry Data Loss or Blocking:** High concurrency causes the telemetry module to drop events or slow down the main API response.
    *   *Mitigation:* Implement telemetry capture asynchronously (e.g., via background tasks in FastAPI) so it does not block the user response.
