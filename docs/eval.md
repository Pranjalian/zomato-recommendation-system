# Evaluation Framework: Zomato GenAI Prototype

This evaluation framework defines the qualitative and quantitative methods to assess the Zomato Recommendation Prototype against its core problem statement and architectural goals.

## 1. GenAI Quality Evaluation (LLM Metrics)
Since this is a GenAI-driven prototype, the core evaluation revolves around the quality of the `QueryParser` and `ExplainabilityModule`.

| Component | Metric | Evaluation Method | Target |
| :--- | :--- | :--- | :--- |
| **Query Parser** | **Intent Accuracy** | Human evaluation of 50 test queries vs. extracted intent/filters. | > 95% accuracy in intent extraction. |
| **Query Parser** | **Context Integration** | Inject mock weather/time data; verify if LLM successfully incorporates it. | 100% correct context mapping. |
| **Explainability**| **Groundedness** | Review generated explanations against retrieved catalog data for hallucinations. | 0% hallucination rate (no false claims). |
| **Explainability**| **Conciseness** | Measure output token count/word count. | 100% of outputs under 2 sentences/30 words. |
| **Explainability**| **Tone & Safety** | Red-teaming: Prompt with inappropriate requests; check safety filter triggers. | 100% block rate on unsafe/irrelevant prompts. |
| **Query Parser** | **Entity Extraction Recall** | Measure how often specific dishes or cuisines (e.g., "Sushi", "Pizza") are correctly isolated from the query. | > 90% extraction recall. |
| **Explainability**| **Persona Match** | Human grading on whether the explanation sounds like a helpful, appetizing food assistant rather than a generic bot. | > 90% positive human rating. |

## 2. Retrieval & Recommendation Accuracy
Evaluating the `Retrieval Engine` and `Ranking Model` to ensure we solve the "choice overload" problem effectively.

*   **Hit Rate (Relevance):** For a given query, are the top 5 recommended restaurants semantically relevant? (Evaluated via expert grading on a sample of 100 diverse queries).
*   **Cold Start Capability:** Simulate a new user profile; evaluate if the system successfully falls back to trending/contextual recommendations (e.g., hot food during rain).
*   **Diversity Score:** Measure the variety of cuisines returned in a single query to ensure the system isn't over-constraining or stuck in a filter bubble.
*   **Mean Reciprocal Rank (MRR):** Evaluate how high up the list the "ideal" or most relevant result appears across a set of test queries.
*   **NDCG (Normalized Discounted Cumulative Gain):** Assess the overall ranking quality, ensuring the absolute best matches are at the very top.

## 3. Performance & System Evaluation
Ensuring the API Gateway and underlying architecture are performant enough to reduce "time-to-order".

*   **End-to-End Latency:** 
    *   *Target:* < 2 seconds for a complete request (Query -> Retrieval -> LLM Explanation -> Response).
*   **Vector Search Speed:** 
    *   *Target:* < 100ms for semantic retrieval from the local vector database.
*   **Token Generation Speed (GenAI):** 
    *   *Target:* Time to First Token (TTFT) < 500ms; Generation speed > 40 tokens/second for snappy explainability generation.
*   **Throughput (Load Testing):** 
    *   *Target:* API Gateway should handle > 50 Concurrent Requests per second without dropping requests or exceeding latency budgets.
*   **API Rate Limiting:** 
    *   Simulate high traffic to ensure Gemini API rate limits are respected and graceful fallbacks (pure semantic search without GenAI explanation) engage correctly.
*   **Telemetry Reliability (Phase 6):**
    *   *Target:* 100% successful asynchronous capture of implicit/explicit feedback events (clicks, orders) into the User Profiles DB without blocking the main API response.

## 4. Edge Case Test Matrix
A strict checklist based on the identified failure modes.

- [ ] **Vague Non-Food Query:** Send "What is the capital of France?" -> *Expected:* Polite refusal.
- [ ] **Contradictory Query:** Send "Cheap caviar" -> *Expected:* System prioritizes one or explains the compromise.
- [ ] **Zero Results:** Send impossible constraints (e.g., "Vegan steak under $1") -> *Expected:* Constraint relaxation and user notification.
- [ ] **Missing Context:** Disable location/weather mock -> *Expected:* System relies on time-of-day and generic defaults.
- [ ] **Stale Data Simulation:** Manually mark a top-ranked restaurant as "Closed" in the catalog DB -> *Expected:* Restaurant is filtered out before reaching the GenAI explainability step.
- [ ] **Dataset Inconsistency:** Ingest a restaurant record with missing coordinates and null ratings -> *Expected:* System imputes defaults or drops the record without crashing the data pipeline.
- [ ] **API Timeout / Failure:** Simulate a timeout from the Gemini API -> *Expected:* Graceful fallback to pure semantic search recommendations without generated explanations.
