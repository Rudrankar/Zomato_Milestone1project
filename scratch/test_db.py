import unittest
import sys
import os

# Add src to python path so we can import database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import get_candidate_restaurants

class TestDatabaseFiltering(unittest.TestCase):
    def test_low_budget(self):
        """Verify that Low budget filters return cost <= 400."""
        results = get_candidate_restaurants(budget_level="Low", limit=20)
        self.assertGreater(len(results), 0, "Should find at least some Low budget restaurants.")
        for r in results:
            self.assertLessEqual(r["cost"], 400, f"Restaurant {r['name']} exceeds low budget limit of 400: cost={r['cost']}")

    def test_medium_budget(self):
        """Verify that Medium budget filters return cost between 401 and 1000."""
        results = get_candidate_restaurants(budget_level="Medium", limit=20)
        self.assertGreater(len(results), 0, "Should find at least some Medium budget restaurants.")
        for r in results:
            self.assertTrue(401 <= r["cost"] <= 1000, f"Restaurant {r['name']} cost {r['cost']} not in medium budget range (401-1000)")

    def test_high_budget(self):
        """Verify that High budget filters return cost > 1000."""
        results = get_candidate_restaurants(budget_level="High", limit=20)
        self.assertGreater(len(results), 0, "Should find at least some High budget restaurants.")
        for r in results:
            self.assertGreater(r["cost"], 1000, f"Restaurant {r['name']} cost {r['cost']} not in high budget range (>1000)")

    def test_rating_filter(self):
        """Verify that min_rating threshold is respected."""
        min_rating = 4.2
        results = get_candidate_restaurants(min_rating=min_rating, limit=20)
        self.assertGreater(len(results), 0, "Should find at least some high-rated restaurants.")
        for r in results:
            self.assertGreaterEqual(r["rating"], min_rating, f"Restaurant {r['name']} rating {r['rating']} is below threshold {min_rating}")

    def test_no_matches(self):
        """Verify that searching for non-existent combinations returns an empty list."""
        results = get_candidate_restaurants(location="NonExistentCityXYZ", cuisine="MartianFood")
        self.assertEqual(len(results), 0, "Query for invalid combinations should return 0 results.")

if __name__ == "__main__":
    unittest.main()
