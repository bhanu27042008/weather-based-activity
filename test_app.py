"""
Unit & Integration Tests for Web Application (Flask Routes & API)
-----------------------------------------------------------------
Verifies web UI endpoints, JSON API, validation errors, and fallback form handling.
"""

import unittest
import json
from app import app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_index(self):
        """Web UI home page should render with 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Weather-Based Activity Agent", response.data)
        self.assertIn(b"Sensory Inputs", response.data)

    def test_get_health(self):
        """Health check endpoint should return 200 OK."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")

    def test_api_recommend_success(self):
        """API should return structured recommendation for valid weather percepts."""
        payload = {
            "temperature": 25.0,
            "condition": "Sunny",
            "humidity": 50,
            "wind_speed": 10
        }
        response = self.client.post(
            "/api/recommend",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("Outdoor", data["data"]["classification"])
        self.assertGreater(len(data["data"]["primary_activities"]), 0)

    def test_api_recommend_storm_hazard(self):
        """API should return hazardous indoor alert for storms."""
        payload = {
            "temperature": 26.0,
            "condition": "Stormy",
            "humidity": 90,
            "wind_speed": 35
        }
        response = self.client.post(
            "/api/recommend",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("Hazardous", data["data"]["classification"])
        self.assertEqual(data["data"]["verdict_color"], "danger")

    def test_api_validation_error(self):
        """API should return 422 if percept inputs are out of bounds."""
        payload = {
            "temperature": 150.0,
            "condition": "Tornado",
            "humidity": 200,
            "wind_speed": -5
        }
        response = self.client.post(
            "/api/recommend",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 422)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertGreater(len(data["errors"]), 0)

    def test_api_missing_fields(self):
        """API should return 400 if required fields are missing."""
        payload = {"temperature": 25.0}
        response = self.client.post(
            "/api/recommend",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_form_fallback_post(self):
        """Standard HTML form POST should render the page with results."""
        form_payload = {
            "temperature": "20.0",
            "condition": "Cloudy",
            "humidity": "55",
            "wind_speed": "12"
        }
        response = self.client.post("/recommend", data=form_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Outdoor Recommended", response.data)


if __name__ == "__main__":
    unittest.main()
