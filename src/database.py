import os
import sqlite3

DB_PATH = os.path.join("data", "zomato.db")

def get_candidate_restaurants(location=None, cuisine=None, budget_level=None, min_rating=0.0, limit=10):
    """
    Queries the SQLite database to filter and fetch the top candidate restaurants based on user criteria.
    
    Parameters:
    - location (str): Name of the location or area.
    - cuisine (str): Cuisine type (e.g. Italian, Chinese).
    - budget_level (str): 'Low', 'Medium', or 'High'.
    - min_rating (float): Minimum clean rating threshold (0.0 to 5.0).
    - limit (int): Max candidates to fetch.
    
    Returns:
    - List[Dict]: List of matching restaurant dict objects.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found at {DB_PATH}. Please run the data ingestion script first.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns results as dictionary-like objects
    cursor = conn.cursor()

    # Base SQL query
    query = "SELECT name, address, location, cuisines, rating_clean, cost_clean FROM restaurants WHERE rating_clean >= ?"
    params = [float(min_rating)]

    # Dynamic filters
    # Match location against BOTH the location column and the full address column for robustness
    if location and location.strip():
        loc_val = f"%{location.strip()}%"
        query += " AND (location LIKE ? OR address LIKE ?)"
        params.append(loc_val)
        params.append(loc_val)

    if cuisine and cuisine.strip():
        cuisine_list = [c.strip() for c in cuisine.split(",") if c.strip()]
        if cuisine_list:
            cuisine_queries = []
            for c in cuisine_list:
                cuisine_queries.append("cuisines LIKE ?")
                params.append(f"%{c}%")
            query += " AND (" + " OR ".join(cuisine_queries) + ")"

    if budget_level:
        budget_lower = budget_level.lower().strip()
        if budget_lower == "low":
            query += " AND cost_clean <= 400"
        elif budget_lower == "medium":
            query += " AND cost_clean BETWEEN 401 AND 1000"
        elif budget_lower == "high":
            query += " AND cost_clean > 1000"

    # Order by rating and apply limit
    query += " ORDER BY rating_clean DESC, cost_clean ASC LIMIT ?"
    params.append(int(limit))

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert sqlite3.Row results to python dicts
        candidates = []
        for row in rows:
            candidates.append({
                "name": row["name"],
                "address": row["address"],
                "location": row["location"],
                "cuisines": row["cuisines"],
                "rating": row["rating_clean"],
                "cost": row["cost_clean"]
            })
        return candidates
    except Exception as e:
        print(f"Error querying database: {e}")
        return []
    finally:
        conn.close()

def get_unique_locations():
    """
    Fetches the sorted list of all unique locations from the SQLite database.
    """
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT location FROM restaurants WHERE location IS NOT NULL AND location != '' ORDER BY location ASC")
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching locations: {e}")
        return []
    finally:
        conn.close()

def get_popular_cuisines():
    """
    Fetches the list of all unique cuisine types present in the database, sorted by popularity (frequency) descending.
    """
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cuisines FROM restaurants WHERE cuisines IS NOT NULL AND cuisines != ''")
        cuisine_counts = {}
        for row in cursor.fetchall():
            for c in row[0].split(','):
                cleaned = c.strip()
                if cleaned:
                    cuisine_counts[cleaned] = cuisine_counts.get(cleaned, 0) + 1
        
        # Sort by frequency descending
        sorted_cuisines = sorted(cuisine_counts.keys(), key=lambda x: cuisine_counts[x], reverse=True)
        return sorted_cuisines
    except Exception as e:
        print(f"Error fetching cuisines: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    # Small self-test execution
    print("Running quick database query test...")
    try:
        sample_results = get_candidate_restaurants(
            location="Koramangala",
            cuisine="Italian",
            budget_level="Medium",
            min_rating=4.0,
            limit=5
        )
        print(f"Found {len(sample_results)} candidate(s):")
        for i, res in enumerate(sample_results, 1):
            print(f"{i}. {res['name']} | Rating: {res['rating']} | Cost for two: {res['cost']} | Cuisines: {res['cuisines']}")
    except Exception as err:
        print(f"Self-test failed: {err}")
