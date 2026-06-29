import os
import sys
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import get_candidate_restaurants
from src.recommender import generate_recommendations

def main():
    print("Fetching candidate restaurants from database...")
    # Location: Bellandur
    # Rating: >= 4.2
    # Budget: 1500 (this falls into "High" category since it is > 1000 INR for two people, 
    # but we can also fetch candidates and check them)
    
    candidates = get_candidate_restaurants(
        location="Bellandur",
        cuisine=None,
        budget_level="High",
        min_rating=4.2,
        limit=10
    )
    
    print(f"Found {len(candidates)} candidates matching Bellandur, Rating >= 4.2, High Budget:")
    for idx, c in enumerate(candidates, 1):
        print(f"{idx}. {c['name']} | Rating: {c['rating']} | Cost: {c['cost']} | Cuisines: {c['cuisines']}")
        
    print("\nCalling Groq LLM to predict top 5 recommendations...")
    user_pref = {
        "location": "Bellandur",
        "cuisine": "Any",
        "budget_level": "High (approx 1500 INR)",
        "min_rating": 4.2,
        "additional": "Find the best options up to 1500 INR."
    }
    
    # We pass limit=5 for top 5 recommendations
    result = generate_recommendations(candidates, user_pref, model="llama-3.3-70b-versatile", top_n=5)
    
    print("\n=== AI RECOMMENDATION RESULTS ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
