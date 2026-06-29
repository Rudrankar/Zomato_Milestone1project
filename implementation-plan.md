# 📅 Phase-Wise Implementation Plan: Zomato AI Restaurant Recommender

This document outlines the step-by-step roadmap for building, testing, and deploying the AI-Powered Restaurant Recommendation System. It has been updated to support a clean separation of concerns with a backend REST API and a premium HTML/CSS/JS frontend.

---

## 🛠️ Tech Stack Recap
*   **Backend:** Python (FastAPI)
*   **Frontend:** Single-Page Application (HTML5, Vanilla CSS, Vanilla JavaScript)
*   **Data Processing & Storage:** Pandas, SQLite
*   **AI Inference:** Groq Python SDK (`llama-3.3-70b-versatile`)
*   **Environment Configuration:** `python-dotenv`

---

## 🚀 Phase-Wise Roadmap

### 📦 Phase 1: Workspace Initialization & Data Ingestion
**Goal:** Set up the developer environment and prepare the raw Zomato dataset for querying.

*   [x] **1.1 Project Structure Setup**
    *   Create directory layout: `/data`, `/src`, `requirements.txt`, `.env`.
*   [x] **1.2 Package Installation**
    *   Initialize virtual environment.
    *   Install core dependencies: `pandas`, `groq`, `python-dotenv`, `db-sqlite3`.
*   [x] **1.3 Data Download & Parsing**
    *   Write an ingestion script (`src/ingest.py`) to download the Zomato dataset.
    *   Filter out irrelevant columns and save clean structures into a local SQLite database (`data/zomato.db`).

---

### 💾 Phase 2: Database Queries & Filtering Engine
**Goal:** Implement the local search utility that extracts matching candidate restaurants from the database before LLM reasoning.

*   [x] **2.1 Database Utility Interface**
    *   Build `src/database.py` to handle connections and executing parameterized SQL queries.
*   [x] **2.2 Business Logic Mapping**
    *   Implement string cleaning for location matches (e.g. trimming whitespace, case-insensitivity).
    *   Code the budget classification logic:
        *   `Low` budget maps to standard cost $\le 400$ INR.
        *   `Medium` budget maps to cost between $401$ and $1000$ INR.
        *   `High` budget maps to cost $> 1000$ INR.
    *   Implement cuisine matchers parsing comma-separated strings.
*   [x] **2.3 Candidate Selection**
    *   Write a query function returning the **Top 5-10** matching restaurants sorted by rating descending (the candidate pool).

---

### 🤖 Phase 3: Groq LLM Integration & Prompt Construction
**Goal:** Configure client communication with Groq and establish prompt templates that guarantee structured outputs.

*   [x] **3.1 Groq Client Setup**
    *   Initialize the client using `groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))`.
    *   Create fallback/retry mechanisms in case of API latency or rate limits.
*   [x] **3.2 Prompt Template Design**
    *   Implement prompt assembly logic (`src/recommender.py`) feeding candidate listings, user constraints, and specific instructions into a pre-structured template.
*   [x] **3.3 Output Parser Implementation**
    *   Enable Groq's **Structured Output / JSON Mode** by setting the `response_format={"type": "json_object"}` parameter.
    *   Write validation code ensuring the returned JSON contains all client-facing details.

---

### 🔌 Phase 4: Backend API Development (FastAPI)
**Goal:** Build a robust, lightweight asynchronous API server to feed data and recommendations to the client.

*   [x] **4.1 API Initialization & Config**
    *   Install backend packages: `fastapi` and `uvicorn`.
    *   Write `src/main.py` configuring CORS, routing, and environment settings.
*   [x] **4.2 Core Information Endpoints**
    *   Implement `GET /api/locations` to dynamically fetch unique locations for dropdown lists.
    *   Implement `GET /api/cuisines` to compile unique or popular cuisines for filters.
    *   Implement `GET /api/health` checking database and key status.
*   [x] **4.3 Recommendation Query Endpoint**
    *   Implement `POST /api/recommend` receiving preferences and calling `src/database.py` and `src/recommender.py`.

---

### 🎨 Phase 5: Premium Web Frontend Development
**Goal:** Develop a stunning, glassmorphic Single Page Application featuring fluid transitions, clean inputs, and elegant UI feedback.

*   [ ] **5.1 Layout & Visual Theme (HTML/CSS)**
    *   Build a sleek dark-themed workspace with custom gradients, premium typography (`Outfit` / `Inter`), and interactive cards.
    *   Define layout structures in `frontend/index.html` and styles in `frontend/style.css`.
*   [ ] **5.2 Interactive Input Controls**
    *   Implement input autocomplete for location matches.
    *   Create an interactive multi-select tag engine for cuisines (adding and removing pills).
    *   Style sliders and budget selection toggles.
*   [ ] **5.3 Async API Communication & Loading States**
    *   Write Javascript in `frontend/app.js` using `fetch` to load suggestions and fetch recommendations.
    *   Build premium card skeleton structures and glowing spinners to handle API delays beautifully.
    *   Integrate a local mock recommendation fallback in the UI if Groq credentials are not set.

---

### 🧪 Phase 6: Verification, Testing & Edge Cases
**Goal:** Ensure resilience, profile response latency, and fix usability hiccups.

*   [ ] **6.1 API & SQL Validation**
    *   Write unit tests or validation scripts for all api routes.
*   [ ] **6.2 UI Responsiveness & Browser Testing**
    *   Validate layouts on mobile/desktop screen sizes.
    *   Ensure graceful error displays (no matches, connection timeouts).
