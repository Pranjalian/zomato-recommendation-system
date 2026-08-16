# Architecture Design: Zomato GenAI Recommendation System Prototype

This document outlines the proposed system architecture for the Zomato Recommendation System Prototype, addressing the "choice overload" problem by utilizing Generative AI and AscendAI capabilities to deliver highly <u>k</u>personalized and explainable restaurant suggestions.

## 1. High-Level Architecture Diagram

```
graph TD
    %% Client & Gateway
    Client[Zomato App / User] -->|Vague Query, Context, Location| Gateway[API Gateway]
    
    %% Processing & Context
    Gateway --> QU[GenAI Query Understanding]
    Gateway --> CE[Context Engine]
    
    %% Data Stores
    subgraph Data Layer
        DB_Catalog[(Restaurant Catalog DB)]
        DB_User[(User Profiles DB)]
        DB_Vector[(Vector DB - Embeddings)]
    end
    
    %% Core AI Engine
    subgraph Core AI System
        CE --> |Time, Weather, Location| RE[Retrieval Engine]
        QU --> |Parsed Intent & Embeddings| RE
        DB_Catalog --> RE
        DB_User --> RE
        DB_Vector --> RE
        
        RE --> |Candidate Generation| Ranker[Ranking & Scoring Model]
    end
    
    %% Explainability & Response
    Ranker --> |Top Recommendations| GenAI_Exp[GenAI Explainability Module]
    GenAI_Exp --> |Personalized Explanations| Gateway
    Gateway --> |Curated List & Reasons| Client
    
    %% Feedback Loop
    Client -.-> |Implicit/Explicit Feedback| Feedback[Telemetry & Feedback Loop]
    Feedback -.-> DB_User
    Feedback -.-> Ranker
```

## 2. Core Components

### 2.1. Client & API Gateway

- **Client App:** The frontend interface where users input vague prompts (e.g., "I'm hungry for something spicy"). It also captures real-time device context (GPS coordinates, local time).
- **API Gateway:** The entry point for all requests. It routes user queries, handles authentication, and orchestrates the flow between the microservices.

### 2.2. Query & Context Processing

- **Context Engine:** Enriches the user request with external real-time data. For example, it fetches current weather conditions (rainy, cold) and precise time-of-day categorization (late-night craving, quick lunch).
- **GenAI Query Understanding (AscendAI/LLM):** Parses vague natural language queries from the user. It extracts semantic intent, dietary preferences, and maps them to vector representations (embeddings) suitable for semantic search.

### 2.3. Data Layer

- **Restaurant Catalog DB (Relational/NoSQL):** Stores structured data such as menus, operating hours, pricing, aggregate ratings, and precise geolocations.
- **User Profiles DB (NoSQL):** Stores historical order data, explicit dietary preferences (e.g., vegan, allergies), and implicit behavioral patterns (e.g., typical order frequency, preferred cuisines).
- **Vector Database:** Stores high-dimensional embeddings of restaurant descriptions, menu items, and user reviews. This is crucial for semantic similarity matching.

### 2.4. Core AI System (Recommendation Engine)

- **Retrieval Engine (Candidate Generation):** Narrows down thousands of options to a subset (e.g., 50-100 candidates). It uses a hybrid approach:
  - *Semantic Search:* Querying the Vector DB based on the user's intent embedding.
  - *Hard Filtering:* Applying constraints like delivery radius, open status, and strict dietary restrictions.
- **Ranking & Scoring Model:** An ML model that scores and ranks the retrieved candidates. It weighs the semantic match score against real-time context (e.g., boosting hot soup places if it's raining) and user historical preferences.

### 2.5. GenAI Explainability Module

- **Explainable AI (XAI):** Instead of just returning a list of restaurants, this module uses Generative AI to craft a personalized "reason to order."
- *Example Output:* "Since it's raining and you wanted something spicy, we recommend the Sichuan Hot Pot from *Dragon Express*—highly rated for quick delivery to your location."
- **Benefit:** Directly reduces decision fatigue by justifying *why* the recommendation is relevant right now.

### 2.6. Telemetry & Feedback Loop

- Captures user interactions with the recommendations (clicks, time spent viewing, actual orders, or abandonment).
- This data is fed back into the User Profiles DB to refine future personalization and used to continuously retrain the Ranking Model.

## 3. Technology Stack Recommendations (Prototype Phase)

- **GenAI/LLM:** AscendAI / Gemini (for Query Understanding and Explainability).
- **Vector Database:** Pinecone, Milvus, or pgvector (for semantic search).
- **Backend & Orchestration:** Python (FastAPI/Flask) or Node.js.
- **Traditional DBs:** PostgreSQL (Catalog) and MongoDB/Firestore (User Profiles & Telemetry).