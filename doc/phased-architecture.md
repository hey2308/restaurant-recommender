# Phase-wise Architecture: AI-Powered Restaurant Recommendation System

This document describes the phase-wise architecture for the Zomato-inspired AI recommendation system.

## Phase 1: Data Foundation Layer

**Goal:** Build a clean and query-ready restaurant dataset.

**Core Components:**
- `Dataset Loader` (Hugging Face fetch utility)
- `Data Preprocessor` (cleaning, null handling, normalization)
- `Feature Extractor` (name, location, cuisine, cost, rating, tags)
- `Data Store` (CSV/SQLite/PostgreSQL)

**Input:** Raw Zomato dataset  
**Output:** Cleaned and structured restaurant repository

---

## Phase 2: User Preference Capture Layer

**Goal:** Collect and validate user requirements for recommendations.

**Core Components:**
- `Input Interface` — **basic web UI** as the primary source of user input; same preference payload may also be submitted via a small **REST API** (JSON) for testing and integration
- `Validation Module` (required fields, value ranges)
- `Preference Normalizer` (maps text to standard labels)

**Input:** User-provided preferences  
**Output:** Validated preference profile (`location`, `budget`, `cuisine`, `min_rating`, `optional_tags`)

---

## Phase 3: Candidate Retrieval and Filtering Layer

**Goal:** Narrow down the dataset to relevant restaurant candidates.

**Core Components:**
- `Filter Engine` (hard filters for location, budget, cuisine, rating)
- `Scoring Helper` (optional weighted ranking before LLM)
- `Top-N Selector` (shortlists best candidates for prompt context)

**Input:** Structured restaurant data + validated user profile  
**Output:** Candidate restaurant list (prompt-ready context)

---

## Phase 4: LLM Recommendation Intelligence Layer

**Goal:** Generate ranked and explainable recommendations.

**Core Components:**
- `Prompt Builder` (system + user + candidate context template)
- `LLM Client` (API integration with model provider)
- `Response Parser` (extract ranking, reasons, summary)
- `Guardrails` (token limits, safe fallback if LLM fails)

**Input:** Candidate list + user profile  
**Output:** Ranked recommendations with natural-language explanations

---

## Phase 5: Presentation and Delivery Layer

**Goal:** Show recommendations in a user-friendly format.

**Core Components:**
- `Response Formatter` (card/table/JSON structure)
- `UI Renderer` (web page, mobile view, or CLI output)
- `Explanation View` (why this was recommended)

**Input:** Parsed LLM recommendations  
**Output:** Final user-facing recommendation list

---

## Phase 6: Backend API and Orchestration Layer

**Goal:** Provide a production-ready backend service that orchestrates recommendation phases and exposes stable APIs.

**Core Components:**
- `Backend API` (FastAPI/Flask service exposing recommendation endpoints)
- `Orchestration Service` (invokes Phase 2 -> Phase 3 -> Phase 4 pipeline)
- `Data Access Layer` (repository access for cleaned restaurant data and optional feedback store)
- `Auth + Rate Limiting` (basic API protection and abuse control)
- `Observability` (structured logs, request tracing, error monitoring)

**Primary Contract:**
- `POST /api/v1/recommendations` -> accepts normalized preference payload and returns ranked explainable recommendations
- `GET /api/v1/health` -> service readiness/liveness check
- Optional: `POST /api/v1/feedback` -> capture like/dislike/selected restaurant

**Input:** Validated user preference requests + pipeline phase outputs  
**Output:** Versioned API responses for frontend/clients

---

## Phase 7: Frontend Experience Layer

**Goal:** Deliver a complete user-facing application that consumes backend APIs and presents recommendations clearly.

**Core Components:**
- `Frontend App` (React/Next.js or equivalent SPA)
- `Preference Form UI` (collects location, budget, cuisine, rating, optional tags)
- `Recommendation Views` (cards, ranking, rationale, loading/error states)
- `API Client Layer` (typed request/response integration with backend)
- `Session State` (persist user inputs and latest recommendation runs)

**Input:** User interactions + backend API responses  
**Output:** Interactive recommendation experience across web/mobile clients

---

## Phase 8: Feedback and Continuous Improvement Layer (Optional but Recommended)

**Goal:** Improve recommendation quality over time.

**Core Components:**
- `Feedback Collector` (likes/dislikes, selected restaurant)
- `Analytics Module` (conversion rate, relevance quality)
- `Prompt/Data Tuning` (adjust filtering logic and prompt design)

**Input:** User interaction and feedback signals  
**Output:** Better retrieval strategy and recommendation relevance

---

## Phase 9: Backend Deployment Layer (Render)

**Goal:** Deploy the Flask backend API to Render for production hosting.

**Core Components:**
- `Render Web Service` (Flask app hosted on render.com)
- `Environment Configuration` (GROQ_API_KEY and other secrets via Render dashboard)
- `Build Configuration` (pip install from requirements.txt, start command)
- `Custom Domain` (optional: api.bitewise-ai.com)

**Deployment Steps:**
1. Create `render.yaml` or use Render Dashboard
2. Configure build command: `pip install -r requirements.txt`
3. Configure start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Add environment variable `GROQ_API_KEY` in Render dashboard
5. Deploy from GitHub repository (main branch)

**Input:** GitHub repository with Phase 6 backend code  
**Output:** Live API at `https://<service-name>.onrender.com/api/v1/recommendations`

---

## Phase 10: Frontend Deployment Layer (Vercel)

**Goal:** Deploy the Next.js frontend to Vercel for production hosting.

**Core Components:**
- `Vercel Project` (Next.js 14 app with static/dynamic export)
- `Environment Variables` (API_BASE_URL pointing to Render backend)
- `Build Settings` (Next.js preset, output directory `.next`)
- `Custom Domain` (optional: www.bitewise-ai.com)

**Deployment Steps:**
1. Import GitHub repository in Vercel dashboard
2. Configure framework preset: Next.js
3. Add environment variable `NEXT_PUBLIC_API_URL` pointing to Render backend
4. Deploy with Git integration (auto-deploy on push to main)

**Input:** GitHub repository with Phase 7 frontend code + Phase 9 backend URL  
**Output:** Live frontend at `https://<project-name>.vercel.app`

---

## End-to-End Request Flow

1. User submits preferences.
2. Frontend sends request to backend recommendation API.
3. Backend validates and normalizes inputs.
4. Filter engine retrieves matching restaurant candidates.
5. Prompt builder sends candidates and user profile to LLM.
6. LLM returns ranked recommendations with explanations.
7. Backend returns formatted response to frontend.
8. Frontend displays top choices and optional summary.
9. Feedback loop stores user actions for future optimization.
