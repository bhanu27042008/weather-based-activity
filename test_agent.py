"""
Unit Tests for Weather-Based Activity Agent
-------------------------------------------
Tests the rational agent's decisions across multiple weather environments:
1. Pleasant sunny day (Outdoor favored)
2. Overcast cloudy day (Outdoor favored with mild activities)
3. Heavy rain (Indoor favored)
4. Severe thunderstorm (Hazardous - Stay indoors)
5. Gale force wind (Hazardous - High wind speed)
6. Extreme heat wave (Indoor cooling favored)
7. Freezing winter temperature (Indoor heating favored)
8. Input validation bounds check
"""

import unittest
from agent import WeatherPercept, ActivityAgent


class TestActivityAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ActivityAgent()

    def test_ideal_sunny_weather(self):
        """Sunny, 24°C, 45% humidity, 10 km/h wind -> Outdoor Favored"""
        percept = WeatherPercept(temperature=24, condition="Sunny", humidity=45, wind_speed=10)
        self.assertEqual(percept.validate(), [])
        
        result = self.agent.evaluate(percept)
        self.assertIn("Outdoor", result["classification"])
        self.assertEqual(result["summary_badge"], "Outdoor Recommended")
        self.assertEqual(result["verdict_color"], "success")
        self.assertTrue(len(result["primary_activities"]) > 0)
        self.assertTrue(len(result["indoor_suggestions"]) > 0)
        self.assertTrue(len(result["outdoor_suggestions"]) > 0)
        self.assertTrue(len(result["explanation"]) > 0)

    def test_pleasant_cloudy_weather(self):
        """Cloudy, 21°C, 50% humidity, 12 km/h wind -> Outdoor Favored"""
        percept = WeatherPercept(temperature=21, condition="Cloudy", humidity=50, wind_speed=12)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Outdoor", result["classification"])
        self.assertEqual(result["summary_badge"], "Outdoor Recommended")

    def test_rainy_weather(self):
        """Rainy, 19°C, 85% humidity, 15 km/h wind -> Indoor Favored"""
        percept = WeatherPercept(temperature=19, condition="Rainy", humidity=85, wind_speed=15)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Indoor", result["classification"])
        self.assertEqual(result["summary_badge"], "Indoor Recommended")
        # Check rainy outdoor alternative is included
        outdoor_names = [a["name"] for a in result["outdoor_suggestions"]]
        self.assertTrue(any("Umbrella" in name or "Rain" in name for name in outdoor_names))

    def test_severe_storm(self):
        """Stormy, 25°C, 90% humidity, 35 km/h wind -> Hazardous Indoor"""
        percept = WeatherPercept(temperature=25, condition="Stormy", humidity=90, wind_speed=35)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Hazardous", result["classification"])
        self.assertEqual(result["verdict_color"], "danger")
        self.assertTrue(any("No outdoor activities" in a["name"] for a in result["outdoor_suggestions"]))

    def test_gale_force_wind(self):
        """Sunny but 55 km/h wind -> Hazardous Indoor due to wind speed"""
        percept = WeatherPercept(temperature=22, condition="Sunny", humidity=40, wind_speed=55)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Hazardous", result["classification"])
        self.assertTrue(any("wind speed" in r.lower() for r in result["reasons"]))

    def test_extreme_heat(self):
        """Sunny, 42°C -> Hazardous / Indoor Favored"""
        percept = WeatherPercept(temperature=42, condition="Sunny", humidity=30, wind_speed=10)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Hazardous", result["classification"])
        self.assertTrue(any("heat" in r.lower() for r in result["reasons"]))

    def test_freezing_temperature(self):
        """Cloudy, -5°C -> Hazardous / Freezing Indoor"""
        percept = WeatherPercept(temperature=-5, condition="Cloudy", humidity=50, wind_speed=10)
        self.assertEqual(percept.validate(), [])

        result = self.agent.evaluate(percept)
        self.assertIn("Hazardous", result["classification"])
        self.assertTrue(any("freezing" in r.lower() for r in result["reasons"]))

    def test_validation_errors(self):
        """Invalid inputs should report clear errors"""
        invalid_percept = WeatherPercept(temperature=100, condition="SnowyVolcano", humidity=150, wind_speed=-10)
        errors = invalid_percept.validate()
        self.assertEqual(len(errors), 4)


if __name__ == "__main__":
    unittest.main()
