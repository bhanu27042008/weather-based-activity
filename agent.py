"""
Weather-Based Activity Agent
----------------------------
A beginner-friendly rational agent implemented in Python for 2nd-year CSE (AIML) students.

AI Concept Background:
In Artificial Intelligence, a Rational Agent operates using the PEAS framework:
- Performance Measure: Safety, physical comfort, and appropriateness of activities.
- Environment: The current weather and atmospheric conditions.
- Actuators: Recommended activities, outdoor/indoor classification, and logical explanation.
- Sensors: Temperature, Weather Condition, Humidity, and Wind Speed inputs.

Author: Antigravity AI Pair Programmer
Target Audience: 2nd-Year Computer Science & Engineering (AIML) Students
"""

from typing import Dict, List, Any


class WeatherPercept:
    """
    Represents the percepts (sensory inputs) gathered by the agent.
    Percepts in our environment include:
      - temperature: Temperature in degrees Celsius (°C)
      - condition: General sky condition ('Sunny', 'Cloudy', 'Rainy', 'Stormy')
      - humidity: Relative humidity percentage (0% - 100%)
      - wind_speed: Wind speed in kilometers per hour (km/h)
    """
    def __init__(self, temperature: float, condition: str, humidity: float, wind_speed: float):
        self.temperature = float(temperature)
        self.condition = condition.strip().capitalize()
        self.humidity = float(humidity)
        self.wind_speed = float(wind_speed)

    def validate(self) -> List[str]:
        """Validates that percepts fall within realistic physical ranges."""
        errors = []
        if not (-50.0 <= self.temperature <= 60.0):
            errors.append(f"Temperature {self.temperature}°C is outside realistic range (-50°C to 60°C).")
        valid_conditions = ["Sunny", "Cloudy", "Rainy", "Stormy"]
        if self.condition not in valid_conditions:
            errors.append(f"Condition '{self.condition}' must be one of: {', '.join(valid_conditions)}.")
        if not (0.0 <= self.humidity <= 100.0):
            errors.append(f"Humidity {self.humidity}% must be between 0% and 100%.")
        if self.wind_speed < 0.0 or self.wind_speed > 250.0:
            errors.append(f"Wind speed {self.wind_speed} km/h must be between 0 and 250 km/h.")
        return errors


class ActivityAgent:
    """
    A Knowledge-Based Rational Agent that maps weather percepts to rational actions.
    
    A rational agent selects an action that is expected to maximize its performance measure,
    given the evidence provided by the percept sequence and built-in knowledge.
    """

    def __init__(self):
        # Curated knowledge base of activities
        self.outdoor_activities_pool = {
            "ideal": [
                {"name": "Cycling / Biking", "icon": "🚲", "desc": "Great aerobic exercise under pleasant weather."},
                {"name": "Jogging or Running", "icon": "🏃", "desc": "Keep fit with an outdoor run in fresh air."},
                {"name": "Picnic in the Park", "icon": "🧺", "desc": "Relax outdoors with family or friends."},
                {"name": "Outdoor Sports (Football/Cricket/Tennis)", "icon": "⚽", "desc": "Active team or racket sports."},
                {"name": "Nature Photography / Sightseeing", "icon": "📸", "desc": "Capture natural light and scenic views."}
            ],
            "mild": [
                {"name": "Brisk Walking / Strolling", "icon": "🚶", "desc": "Gentle outdoor walk with a light jacket."},
                {"name": "Outdoor Cafe / Terrace Seating", "icon": "☕", "desc": "Enjoy a warm beverage in open air."},
                {"name": "Balcony Gardening", "icon": "🌱", "desc": "Tend to plants and flowers without travelling far."}
            ],
            "rainy_outdoor": [
                {"name": "Rain Walk with Umbrella", "icon": "☂️", "desc": "Short, peaceful walk if you enjoy rainy ambiance."},
                {"name": "Rain Photography", "icon": "🌧️", "desc": "Capture reflections and droplets from a covered spot."}
            ]
        }

        self.indoor_activities_pool = {
            "active": [
                {"name": "Gym Workout & Fitness", "icon": "🏋️", "desc": "Strength and cardio training in a controlled indoor climate."},
                {"name": "Indoor Badminton / Squash", "icon": "🏸", "desc": "Fast-paced indoor court sports."},
                {"name": "Indoor Swimming (Heated Pool)", "icon": "🏊", "desc": "Low-impact full-body workout away from rain/wind."},
                {"name": "Bowling Alley", "icon": "🎳", "desc": "Fun group or solo indoor game."}
            ],
            "leisure": [
                {"name": "Reading a Book", "icon": "📖", "desc": "Cozy reading session with coffee or tea."},
                {"name": "Board Games / Video Games", "icon": "🎲", "desc": "Engaging mental play with friends or family."},
                {"name": "Movie or Documentary Marathon", "icon": "🎬", "desc": "Stream your favorite films from the comfort of a couch."},
                {"name": "Cooking or Baking", "icon": "🍳", "desc": "Try out a new recipe in the warm kitchen."},
                {"name": "Visit a Museum / Art Gallery", "icon": "🏛️", "desc": "Cultural exploration sheltered from external weather."}
            ],
            "productive": [
                {"name": "Coding / AI Project Work", "icon": "💻", "desc": "Great uninterrupted focus time for programming."},
                {"name": "Online Learning & Skill Building", "icon": "🎓", "desc": "Learn a new topic or practice tutorials indoors."}
            ]
        }

    def evaluate(self, percept: WeatherPercept) -> Dict[str, Any]:
        """
        Agent Function: f(Percept) -> Action (Recommendation & Reasoning)
        
        The decision logic proceeds through three sequential reasoning stages:
        1. Safety Filter (Severe weather, storms, gale-force winds, extreme temperatures)
        2. Thermal Comfort & Precipitation Check
        3. Activity Selection & Rational Explanation Synthesis
        """
        temp = percept.temperature
        cond = percept.condition
        hum = percept.humidity
        wind = percept.wind_speed

        reasons: List[str] = []
        caution_notes: List[str] = []

        # -------------------------------------------------------------
        # STAGE 1: SAFETY REASONING (Is outdoor activity safe?)
        # -------------------------------------------------------------
        is_severe = False

        if cond == "Stormy":
            is_severe = True
            reasons.append("⚡ Stormy conditions present lightning hazard, strong downpours, and reduced visibility.")
            caution_notes.append("Safety priority: All outdoor activities must be avoided during thunderstorms.")

        if wind >= 45.0:
            is_severe = True
            reasons.append(f"💨 High wind speed ({wind} km/h) can cause flying debris, unstable footing, and falling branches.")
            caution_notes.append("Outdoor exposure is hazardous due to gale-level wind gusts.")

        if temp >= 40.0:
            is_severe = True
            reasons.append(f"🔥 Extreme heat ({temp}°C) poses a significant risk of heat exhaustion and heatstroke.")
            caution_notes.append("Prolonged outdoor exposure under 40°C+ heat is dangerous.")

        if temp <= 0.0:
            is_severe = True
            reasons.append(f"❄️ Sub-zero freezing temperature ({temp}°C) causes frostbite risk and slippery ice surfaces.")
            caution_notes.append("Freezing conditions make outdoor physical activities unsafe without specialized gear.")

        if is_severe:
            classification = "Indoor Favored (Hazardous / Severe Weather)"
            summary_badge = "Indoor Recommended"
            verdict_color = "danger"

            primary_activities = [
                self.indoor_activities_pool["leisure"][0],     # Reading
                self.indoor_activities_pool["leisure"][1],     # Board games
                self.indoor_activities_pool["leisure"][2],     # Movies
                self.indoor_activities_pool["productive"][0]   # Coding
            ]
            indoor_suggestions = self.indoor_activities_pool["leisure"] + self.indoor_activities_pool["productive"]
            outdoor_suggestions = [
                {"name": "No outdoor activities advised", "icon": "🚫", "desc": "Weather is currently unsafe for outdoor recreation."}
            ]

            explanation = (
                "The agent's safety rules detected severe atmospheric conditions. "
                + " ".join(reasons)
                + " Rational agents prioritize human safety over recreation, hence recommending cozy, secure indoor pursuits."
            )

            return {
                "classification": classification,
                "summary_badge": summary_badge,
                "verdict_color": verdict_color,
                "explanation": explanation,
                "reasons": reasons,
                "caution_notes": caution_notes,
                "primary_activities": primary_activities,
                "indoor_suggestions": indoor_suggestions,
                "outdoor_suggestions": outdoor_suggestions,
                "percept": {
                    "temperature": temp,
                    "condition": cond,
                    "humidity": hum,
                    "wind_speed": wind
                }
            }

        # -------------------------------------------------------------
        # STAGE 2: PRECIPITATION & THERMAL COMFORT REASONING
        # -------------------------------------------------------------
        
        # Scenario A: Rainy Weather (Non-stormy rain)
        if cond == "Rainy":
            classification = "Indoor Favored (Precipitation & Wet Ground)"
            summary_badge = "Indoor Recommended"
            verdict_color = "info"

            reasons.append(f"🌧️ Active rainfall makes grounds slippery and outdoor sports impractical.")
            if hum >= 80.0:
                reasons.append(f"💧 High humidity ({hum}%) slows evaporation, causing a damp and chilly feel.")

            explanation = (
                "Rainfall dampens outdoor spaces and creates slip hazards for sports and workouts. "
                "The agent recommends indoor recreation, cultural visits, or fitness centers, with calm rainy-day alternatives."
            )

            primary_activities = [
                self.indoor_activities_pool["active"][0],      # Gym
                self.indoor_activities_pool["leisure"][4],     # Museum / Gallery
                self.indoor_activities_pool["leisure"][2],     # Movie
                self.indoor_activities_pool["leisure"][0]      # Reading
            ]
            indoor_suggestions = self.indoor_activities_pool["active"] + self.indoor_activities_pool["leisure"][:3]
            outdoor_suggestions = self.outdoor_activities_pool["rainy_outdoor"]

            return {
                "classification": classification,
                "summary_badge": summary_badge,
                "verdict_color": verdict_color,
                "explanation": explanation,
                "reasons": reasons,
                "caution_notes": ["Carry an umbrella or raincoat if stepping outside briefly."],
                "primary_activities": primary_activities,
                "indoor_suggestions": indoor_suggestions,
                "outdoor_suggestions": outdoor_suggestions,
                "percept": {
                    "temperature": temp,
                    "condition": cond,
                    "humidity": hum,
                    "wind_speed": wind
                }
            }

        # Scenario B: High Heat or Muggy Weather (Sunny/Cloudy with Temp >= 33°C or high Heat Index)
        if temp >= 33.0 or (temp >= 30.0 and hum >= 75.0):
            classification = "Indoor Favored (High Heat & Humidity)"
            summary_badge = "Indoor Recommended"
            verdict_color = "warning"

            reasons.append(f"☀️ High temperature ({temp}°C) combined with {hum}% humidity increases thermal stress.")
            reasons.append("🥵 Vigorous outdoor exertion in high heat can trigger dehydration and cramps.")

            explanation = (
                f"The thermal comfort index is uncomfortably warm at {temp}°C with {hum}% humidity. "
                "To optimize health and comfort, the agent recommends air-conditioned or shaded indoor activities, "
                "or refreshing water-based recreation."
            )

            primary_activities = [
                self.indoor_activities_pool["active"][2],      # Indoor swimming
                self.indoor_activities_pool["active"][0],      # AC Gym
                self.indoor_activities_pool["leisure"][4],     # Museum / Mall
                self.indoor_activities_pool["leisure"][2]      # Movie theater
            ]
            indoor_suggestions = self.indoor_activities_pool["active"] + self.indoor_activities_pool["leisure"]
            outdoor_suggestions = [
                {"name": "Early Evening Stroll", "icon": "🌆", "desc": "Wait until after sunset when temperature cools down."},
                {"name": "Shaded Tree Sitting", "icon": "🌳", "desc": "Rest in full shade with plenty of hydration."}
            ]

            return {
                "classification": classification,
                "summary_badge": summary_badge,
                "verdict_color": verdict_color,
                "explanation": explanation,
                "reasons": reasons,
                "caution_notes": ["Stay hydrated! Drink plenty of water and avoid direct midday sun."],
                "primary_activities": primary_activities,
                "indoor_suggestions": indoor_suggestions,
                "outdoor_suggestions": outdoor_suggestions,
                "percept": {
                    "temperature": temp,
                    "condition": cond,
                    "humidity": hum,
                    "wind_speed": wind
                }
            }

        # Scenario C: Chilly Weather (Temp between 0°C and 12°C)
        if temp < 12.0:
            classification = "Indoor Favored (Cold & Chilly)"
            summary_badge = "Indoor Recommended"
            verdict_color = "secondary"

            reasons.append(f"🧥 Low temperature ({temp}°C) creates cold discomfort for prolonged outdoor presence.")
            if wind > 20.0:
                reasons.append(f"🌬️ Moderate wind ({wind} km/h) creates significant wind-chill.")

            explanation = (
                f"At {temp}°C, the ambient atmosphere is cold. While short brisk walks in warm jackets are feasible, "
                "the agent rationally recommends heated indoor venues, warm beverages, and indoor hobbies for optimal comfort."
            )

            primary_activities = [
                self.indoor_activities_pool["leisure"][0],     # Reading
                self.indoor_activities_pool["leisure"][3],     # Cooking warm meals
                self.indoor_activities_pool["active"][0],      # Indoor gym workout
                self.outdoor_activities_pool["mild"][0]        # Brisk walk with coat
            ]
            indoor_suggestions = self.indoor_activities_pool["leisure"] + self.indoor_activities_pool["active"]
            outdoor_suggestions = [
                {"name": "Brisk Walk in Warm Jacket", "icon": "🧥", "desc": "Invigorating cold-weather walk if layered properly."},
                {"name": "Outdoor Hot Coffee Break", "icon": "☕", "desc": "Sip hot coffee or tea in warm sunlight."}
            ]

            return {
                "classification": classification,
                "summary_badge": summary_badge,
                "verdict_color": verdict_color,
                "explanation": explanation,
                "reasons": reasons,
                "caution_notes": ["Wear warm thermal layers if going outdoors."],
                "primary_activities": primary_activities,
                "indoor_suggestions": indoor_suggestions,
                "outdoor_suggestions": outdoor_suggestions,
                "percept": {
                    "temperature": temp,
                    "condition": cond,
                    "humidity": hum,
                    "wind_speed": wind
                }
            }

        # -------------------------------------------------------------
        # STAGE 3: PLEASANT & IDEAL OUTDOOR CONDITIONS
        # -------------------------------------------------------------
        # Temperature is 12°C - 32°C, Condition is Sunny or Cloudy, Wind < 45 km/h
        
        classification = "Outdoor Favored (Pleasant & Comfortable Weather)"
        summary_badge = "Outdoor Recommended"
        verdict_color = "success"

        reasons.append(f"🌤️ Condition is {cond} with a pleasant temperature of {temp}°C.")
        if 18.0 <= temp <= 26.0 and hum <= 65.0:
            reasons.append(f"🌿 Perfect thermal comfort zone with moderate humidity ({hum}%).")
        else:
            reasons.append(f"💨 Gentle breeze at {wind} km/h keeps the air fresh.")

        if cond == "Sunny":
            explanation = (
                f"Clear sunny skies and moderate temperature ({temp}°C) make conditions ideal for outdoor fitness, "
                "sports, and social gatherings. The rational agent maximizes environmental utility by recommending outdoor activities."
            )
            primary_activities = [
                self.outdoor_activities_pool["ideal"][0],      # Cycling
                self.outdoor_activities_pool["ideal"][1],      # Jogging
                self.outdoor_activities_pool["ideal"][2],      # Picnic
                self.outdoor_activities_pool["ideal"][3]       # Outdoor sports
            ]
        else:  # Cloudy
            explanation = (
                f"Cloudy weather provides natural shade from intense UV radiation while maintaining comfortable temperatures ({temp}°C). "
                "This is ideal for distance walking, cycling, or city exploration without overheating."
            )
            primary_activities = [
                self.outdoor_activities_pool["ideal"][0],      # Cycling
                self.outdoor_activities_pool["ideal"][4],      # Photography
                self.outdoor_activities_pool["mild"][0],       # Brisk walk
                self.outdoor_activities_pool["mild"][1]        # Outdoor cafe
            ]

        indoor_suggestions = self.indoor_activities_pool["leisure"][:3] + self.indoor_activities_pool["productive"]
        outdoor_suggestions = self.outdoor_activities_pool["ideal"] + self.outdoor_activities_pool["mild"]

        return {
            "classification": classification,
            "summary_badge": summary_badge,
            "verdict_color": verdict_color,
            "explanation": explanation,
            "reasons": reasons,
            "caution_notes": ["Don't forget sunscreen or sunglasses if sunny!"] if cond == "Sunny" else [],
            "primary_activities": primary_activities,
            "indoor_suggestions": indoor_suggestions,
            "outdoor_suggestions": outdoor_suggestions,
            "percept": {
                "temperature": temp,
                "condition": cond,
                "humidity": hum,
                "wind_speed": wind
            }
        }
