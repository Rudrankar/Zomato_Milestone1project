import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add src to python path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Verify GET /api/health returns valid system checks."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("database_exists", data)
        self.assertTrue(data["database_exists"], "Database should exist at data/zomato.db")

    def test_locations_endpoint(self):
        """Verify GET /api/locations returns locations list."""
        response = self.client.get("/api/locations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("locations", data)
        self.assertIsInstance(data["locations"], list)
        self.assertGreater(len(data["locations"]), 0, "Location list should not be empty")

    def test_cuisines_endpoint(self):
        """Verify GET /api/cuisines returns cuisines list."""
        response = self.client.get("/api/cuisines")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cuisines", data)
        self.assertIsInstance(data["cuisines"], list)
        self.assertGreater(len(data["cuisines"]), 0, "Cuisine list should not be empty")

    def test_recommendation_flow(self):
        """Verify POST /api/recommend returns structured list of suggestions."""
        payload = {
            "location": "Koramangala",
            "cuisine": "Italian",
            "budget_level": "Medium",
            "min_rating": 4.0,
            "additional": "Nice romantic outdoor tables",
            "top_n": 3
        }
        response = self.client.post("/api/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommendations", data)
        recs = data["recommendations"]
        self.assertIsInstance(recs, list)
        
        # If matching candidates exist in database, check recommendations details
        if len(recs) > 0:
            first = recs[0]
            self.assertIn("name", first)
            self.assertIn("cuisine", first)
            self.assertIn("rating", first)
            self.assertIn("cost", first)
            self.assertIn("explanation", first)

if __name__ == "__main__":
    unittest.main()
