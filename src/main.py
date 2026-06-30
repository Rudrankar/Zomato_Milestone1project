import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add workspace directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import get_candidate_restaurants, get_unique_locations, get_popular_cuisines
from src.recommender import generate_recommendations
from src.ingest import download_dataset, process_and_store

app = FastAPI(
    title="Zomato AI Restaurant Recommender API",
    description="Backend service for Zomato-inspired AI recommendations",
    version="1.0.0"
)

# Enable CORS for local testing if running frontend separately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db_path = os.path.join("data", "zomato.db")
    if not os.path.exists(db_path):
        print("SQLite database not found. Initializing auto-ingestion on startup...")
        try:
            download_dataset()
            process_and_store()
            print("Database ingestion completed successfully.")
        except Exception as e:
            print(f"Database ingestion failed: {e}")
            # Do not re-raise to allow the server to start, but subsequent API queries will report health check failures.

# Pydantic schema for recommendation request body
class RecommendationRequest(BaseModel):
    location: str = "Any"
    cuisine: str = "Any"
    budget_level: str = "Any"
    min_rating: float = 0.0
    additional: str = ""
    top_n: int = 3

@app.get("/api/health")
def health_check():
    """
    Returns system status, ensuring database availability and environment credentials configuration.
    """
    db_path = os.path.join("data", "zomato.db")
    db_exists = os.path.exists(db_path)
    
    # Check if Groq API key is present
    groq_api_key = os.environ.get("GROQ_API_KEY")
    groq_configured = bool(groq_api_key and len(groq_api_key.strip()) > 0)
    
    return {
        "status": "healthy" if db_exists else "unhealthy",
        "database_exists": db_exists,
        "groq_configured": groq_configured,
        "message": "API server is running. Mock mode enabled if GROQ_API_KEY is missing." if not groq_configured else "API server running with Groq LLM integration."
    }

@app.get("/api/locations")
def fetch_locations():
    """
    Returns a list of distinct geographic locations available in the dataset.
    """
    locations = get_unique_locations()
    return {"locations": locations}

@app.get("/api/cuisines")
def fetch_cuisines():
    """
    Returns a list of unique cuisines available in the dataset.
    """
    cuisines = get_popular_cuisines()
    return {"cuisines": cuisines}

@app.post("/api/recommend")
def recommend_restaurants(request: RecommendationRequest):
    """
    Queries local candidates matching filters and runs them through Groq Recommender.
    """
    # Standardize inputs
    loc = None if request.location.lower() == "any" else request.location
    cui = None if request.cuisine.lower() == "any" else request.cuisine
    budget = None if request.budget_level.lower() == "any" else request.budget_level
    min_rat = float(request.min_rating)
    
    # Fetch up to 15 candidates sorted by rating descending
    candidates = get_candidate_restaurants(
        location=loc,
        cuisine=cui,
        budget_level=budget,
        min_rating=min_rat,
        limit=15
    )
    
    if not candidates:
        return {
            "recommendations": [],
            "message": "No restaurants match your filters in the local database. Try adjusting your constraints!"
        }
    
    # Map request back to user preferences for the prompt constructor
    user_pref = {
        "location": request.location,
        "cuisine": request.cuisine,
        "budget_level": request.budget_level,
        "min_rating": request.min_rating,
        "additional": request.additional
    }
    
    # Use recommendation engine to score, select and explain top N candidates
    try:
        results = generate_recommendations(candidates, user_pref, top_n=request.top_n)
        return results
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"LLM Recommendation failed: {err}")

# Serve frontend directory dynamically
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend folder not found at {frontend_path}. Please create it to serve client assets.")

if __name__ == "__main__":
    import uvicorn
    # Start web server on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
