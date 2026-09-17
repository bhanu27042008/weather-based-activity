"""
Weather-Based Activity Agent - Web Application (Flask)
------------------------------------------------------
This file sets up a lightweight Flask web server that connects the user interface
with our Rational Agent (ActivityAgent).

Routes:
  - GET  /              : Renders the clean, modern web interface.
  - POST /api/recommend : Accepts weather percepts via JSON, evaluates them via the
                          Rational Agent, and returns recommendations and reasoning.
  - POST /recommend     : Fallback form POST route that supports standard HTML forms.
  - GET  /health        : Simple health check endpoint.

Author: Antigravity AI Pair Programmer
Target Audience: 2nd-Year Computer Science & Engineering (AIML) Students
"""

from flask import Flask, render_template, request, jsonify
from agent import WeatherPercept, ActivityAgent
import os

app = Flask(__name__)
agent = ActivityAgent()


@app.route("/", methods=["GET"])
def index():
    """Renders the main user interface."""
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """
    JSON API endpoint for asynchronous recommendation requests.
    Expects JSON payload:
      {
        "temperature": float,
        "condition": "Sunny" | "Cloudy" | "Rainy" | "Stormy",
        "humidity": float,
        "wind_speed": float
      }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "errors": ["Invalid JSON payload or empty request."]}), 400

    try:
        raw_temp = data.get("temperature")
        raw_cond = data.get("condition")
        raw_hum = data.get("humidity")
        raw_wind = data.get("wind_speed")

        # Check for missing fields
        missing = []
        if raw_temp is None or raw_temp == "":
            missing.append("Temperature")
        if raw_cond is None or raw_cond == "":
            missing.append("Weather Condition")
        if raw_hum is None or raw_hum == "":
            missing.append("Humidity")
        if raw_wind is None or raw_wind == "":
            missing.append("Wind Speed")

        if missing:
            return jsonify({
                "success": False,
                "errors": [f"Missing required field(s): {', '.join(missing)}"]
            }), 400

        # Create percept object
        percept = WeatherPercept(
            temperature=float(raw_temp),
            condition=str(raw_cond),
            humidity=float(raw_hum),
            wind_speed=float(raw_wind)
        )

        # Validate percept ranges
        errors = percept.validate()
        if errors:
            return jsonify({"success": False, "errors": errors}), 422

        # Agent reasoning & recommendation
        decision = agent.evaluate(percept)
        return jsonify({"success": True, "data": decision})

    except ValueError as val_err:
        return jsonify({"success": False, "errors": [f"Invalid number format: {str(val_err)}"]}), 400
    except Exception as ex:
        return jsonify({"success": False, "errors": [f"An unexpected error occurred: {str(ex)}"]}), 500


@app.route("/recommend", methods=["POST"])
def form_recommend():
    """
    Standard HTML Form submission handler.
    Allows the application to work seamlessly even without JavaScript.
    """
    try:
        temp = request.form.get("temperature")
        cond = request.form.get("condition")
        hum = request.form.get("humidity")
        wind = request.form.get("wind_speed")

        percept = WeatherPercept(temp, cond, hum, wind)
        errors = percept.validate()
        if errors:
            return render_template("index.html", errors=errors, form_data=request.form)

        decision = agent.evaluate(percept)
        return render_template("index.html", decision=decision, form_data=request.form)
    except Exception as ex:
        return render_template("index.html", errors=[str(ex)], form_data=request.form)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint to verify server is running."""
    return jsonify({"status": "healthy", "service": "Weather-Based Activity Agent"})


if __name__ == "__main__":
    import sys
    # Ensure stdout handles unicode gracefully on Windows shells
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    port = int(os.environ.get("PORT", 5000))
    print("============================================================")
    print(" [*] Weather-Based Activity Agent Server Running!")
    print(f" [*] Access the Web UI at: http://127.0.0.1:{port}/")
    print(" [*] Architecture: Russell & Norvig Rational Agent (PEAS)")
    print("============================================================")
    app.run(host="127.0.0.1", port=port, debug=True)

