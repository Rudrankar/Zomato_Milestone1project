import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add src to python path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.recommender as recommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.candidates = [
            {"name": "Dyu Art Cafe", "cuisines": "Cafe, Italian", "location": "Koramangala", "rating": 4.5, "cost": 800, "address": "Block 5"},
            {"name": "Onesta", "cuisines": "Pizza, Italian", "location": "Koramangala", "rating": 4.4, "cost": 600, "address": "Block 3"}
        ]
        self.user_pref = {
            "location": "Koramangala",
            "cuisine": "Italian",
            "budget_level": "Medium",
            "min_rating": 4.0,
            "additional": "Cozy workspace."
        }

    def test_mock_fallback_mode_empty_key(self):
        """Verify that when client is None (no API Key), mock recommendations are returned."""
        with patch('src.recommender.client', None):
            res = recommender.generate_recommendations(self.candidates, self.user_pref)
            self.assertIn("recommendations", res)
            self.assertEqual(len(res["recommendations"]), 2)
            self.assertEqual(res["recommendations"][0]["name"], "Dyu Art Cafe")
            self.assertTrue(res["recommendations"][0]["explanation"].startswith("[Offline Mock Mode]"))

    def test_empty_candidates_returns_empty_recommendations(self):
        """Verify that passing empty candidates list immediately returns empty JSON list."""
        res = recommender.generate_recommendations([], self.user_pref)
        self.assertIn("recommendations", res)
        self.assertEqual(len(res["recommendations"]), 0)

    @patch('src.recommender.client')
    def test_groq_client_successful_response(self, mock_groq_client):
        """Mock the Groq client API response and check prompt integration and JSON parsing."""
        # Setup mock completion objects
        mock_choice = MagicMock()
        mock_choice.message.content = json.dumps({
            "recommendations": [
                {
                    "name": "Dyu Art Cafe",
                    "cuisine": "Cafe, Italian",
                    "rating": 4.5,
                    "cost": 800,
                    "explanation": "This restaurant is a cozy art cafe with excellent Italian options, fitting your vibe."
                }
            ]
        })
        
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_groq_client.chat.completions.create.return_value = mock_completion

        # Execute recommendations with mocked client active
        res = recommender.generate_recommendations(self.candidates, self.user_pref)
        
        # Verify the mock API was called
        mock_groq_client.chat.completions.create.assert_called_once()
        
        # Verify result parsing
        self.assertIn("recommendations", res)
        self.assertEqual(len(res["recommendations"]), 1)
        self.assertEqual(res["recommendations"][0]["name"], "Dyu Art Cafe")
        self.assertEqual(res["recommendations"][0]["cost"], 800)

if __name__ == "__main__":
    unittest.main()
