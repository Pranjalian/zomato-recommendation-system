# Zomato GenAI Recommendation System Prototype Implementation Plan

## Overview
This implementation plan provides a detailed, phase-by-phase approach to building the Zomato Recommendation System Prototype. It directly addresses the "choice overload" and "vague intent" challenges outlined in the problem statement by leveraging Generative AI (AscendAI/Gemini) and a hybrid retrieval architecture to deliver personalized, explainable recommendations.

## Proposed Changes

---

### Phase 1: Foundation & Data Layer Setup (Catalog & User Profiles)
**Goal:** Establish the fundamental data structures and databases required to store restaurant information and user profiles.

*   **[NEW] `data/dataset_loader.py`**: Script to load, clean, and preprocess the provided Zomato dataset. We will use the Hugging Face dataset (`hf://datasets/ManikaSaini/zomato-restaurant-recommendation/zomato.csv`) instead of the local dummy CSV. Must handle dataset inconsistencies (e.g., null ratings, missing coordinates) gracefully by imputing values or dropping unusable records.
*   **[NEW] `database/catalog_db.py`**: Setup for a relational database (e.g., PostgreSQL or SQLite for prototype) to act as the Restaurant Catalog storing structured data (menus, pricing, hours).
*   **[NEW] `database/user_db.py`**: Setup for a NoSQL database (e.g., MongoDB/Firestore) to store User Profiles, capturing explicit preferences (allergies, diet) and implicit behaviors (historical orders).

---

### Phase 2: Vector Database & Embeddings (Retrieval Layer)
**Goal:** Implement the embedding generation and vector storage to enable semantic search capabilities.

*   **[NEW] `embeddings/embedder.py`**: Script to convert restaurant descriptions, menus, and user reviews into high-dimensional vector embeddings using a pre-trained embedding model (e.g., Gemini embeddings or SentenceTransformers).
*   **[NEW] `embeddings/vector_store.py`**: Integration with a vector database (e.g., Pinecone, Milvus, ChromaDB) to store and index the generated embeddings for fast semantic nearest-neighbor search.

---

### Phase 3: GenAI Integration (Query Understanding & Context)
**Goal:** Integrate the LLM to understand vague natural language queries and enrich them with real-time context.

*   **[NEW] `api/context_engine.py`**: Module to fetch or mock external real-time context (weather conditions, exact time of day, precise location). Handles missing or inaccurate context by providing generic defaults or time-based fallbacks.
*   **[NEW] `genai/query_parser.py`**: Module using AscendAI/Gemini to parse vague user queries (e.g., "spicy food for a rainy day") into structured context, semantic intent, and hard constraints. Includes fallback mechanisms for non-food queries, handles contradictory intents, and extracts precise entities (diet, cuisine).

---

### Phase 4: Core AI System (Recommendation Engine)
**Goal:** Build the retrieval and ranking mechanisms to select and order the best candidates.

*   **[NEW] `engine/retrieval.py`**: The retrieval logic combining semantic search (from Vector DB based on intent embedding) and hard filtering (from Catalog DB based on radius, open status, dietary restrictions). Includes logic to handle "Zero Results" by gradually relaxing constraints, mitigate "Filter Bubbles" by injecting exploration recommendations, and pre-filter stale/closed restaurants before LLM handoff.
*   **[NEW] `engine/ranking.py`**: ML ranking model to score and order the retrieved candidates, weighing semantic match scores against real-time context (e.g., boosting hot soup on rainy days) and user historical preferences.

---

### Phase 5: Explainability & API Gateway
**Goal:** Provide personalized, GenAI-driven reasons to order and expose the system via a REST API.

*   **[NEW] `genai/explainability.py`**: Explainable AI (XAI) Module that takes the top-ranked restaurants and the user's context to generate personalized, natural language reasons to order (e.g., "Since it's raining and you want spicy food..."). Enforces strict length limits (conciseness), strict grounding on catalog data (prevents hallucinations), and implements safety guardrails.
*   **[NEW] `api/main.py`**: A FastAPI (or Node.js) application serving as the API Gateway. Orchestrates the flow: Query -> Context -> Parser -> Retrieval -> Ranking -> Explainability. Implements caching, API rate limit handling, and graceful fallbacks (e.g., basic semantic search without LLM) if the GenAI API fails.
*   **[NEW] `requirements.txt`**: Project dependencies (FastAPI, uvicorn, chromadb, google-generativeai, etc.).

---

### Phase 6: Telemetry & Feedback Loop (Post-MVP)
**Goal:** Capture user interactions to continuously improve recommendations.

*   **[NEW] `analytics/telemetry.py`**: Module to capture implicit/explicit feedback (clicks, actual orders, abandonment) and feed it back into the User Profiles DB to refine future personalization and continuously retrain the Ranking Model.

---

## Verification Plan

### Evaluation Metrics & Performance
- **GenAI Quality:** Assess Intent Accuracy (>95%), Groundedness (0% hallucinations), Conciseness (<30 words), Tone/Safety, and Entity Extraction Recall.
- **Retrieval Accuracy:** Measure Hit Rate, Diversity Score, MRR, NDCG, and Cold Start capabilities.
- **System Performance:** Ensure End-to-End Latency < 2s, Vector Search < 100ms, TTFT < 500ms, and API Throughput > 50 RPS.

### Automated Tests
- We will write basic unit tests for the `query_parser`, `context_engine`, `retrieval`, and `ranking` logic.
- We will execute script runs to ensure the vector database and relational DBs can be queried successfully.

### Manual & Edge Case Verification
- We will start the API server locally and use tools like `curl` or Postman to send test queries (e.g., "I'm hungry for something spicy") with different mock contexts (e.g., weather: rainy).
- We will manually verify that the returned recommendations are semantically relevant and that the GenAI explanation accurately reflects both the user's intent and the current context.
- **Edge Case Test Matrix:** Execute the following scenarios:
  - Vague Non-Food Query -> Expect polite refusal.
  - Contradictory Query -> Expect system to prioritize or explain compromise.
  - Zero Results (impossible constraints) -> Expect constraint relaxation notification.
  - Missing Context -> Expect system to rely on generic defaults/time.
  - Stale Data Simulation (mark restaurant closed) -> Expect restaurant is filtered out before GenAI generation.
