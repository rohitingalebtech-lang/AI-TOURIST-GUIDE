"""
app.py
Main Flask application for Personalized AI Tourist Guide India.
Provides RESTful APIs, page routing, and security headers.
"""

import uuid
import json
import logging
from flask import Flask, render_template, request, jsonify, abort
from config import Config
from database import (
    init_db,
    get_all_destinations,
    get_destination_by_id,
    get_all_attractions,
    save_user_trip,
    get_saved_trips,
    delete_saved_trip
)
from travel_data import TRANSPORT_ROUTES, PRACTICAL_GUIDE, PACKING_ITEMS
from ai_engine import generate_custom_itinerary, ask_travel_ai

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database on startup
with app.app_context():
    init_db()
    logger.info("Database initialized successfully.")

# ----------------- SECURITY HEADERS -----------------
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# ----------------- WEB PAGES -----------------
@app.route("/")
def index():
    """Render the main homepage with initial server-side hydration."""
    destinations = get_all_destinations()
    saved_trips = get_saved_trips()
    return render_template(
        "index.html",
        destinations=destinations,
        transport_routes=TRANSPORT_ROUTES,
        practical_guide=PRACTICAL_GUIDE,
        packing_items=PACKING_ITEMS,
        saved_trips=saved_trips
    )

@app.route("/trip/print/<trip_id>")
def print_trip(trip_id):
    """Render a dedicated clean printable and PDF-ready view of a saved trip."""
    trips = get_saved_trips()
    target_trip = next((t for t in trips if t["id"] == trip_id), None)
    if not target_trip:
        abort(404)
    return render_template("print_trip.html", trip=target_trip)

# ----------------- REST API ENDPOINTS -----------------
@app.route("/api/destinations", methods=["GET"])
def api_destinations():
    """Get all destinations with optional filtering."""
    region = request.args.get("region")
    category = request.args.get("category")
    search = request.args.get("q", "").strip().lower()

    destinations = get_all_destinations()

    if region and region != "all":
        destinations = [d for d in destinations if d["region"].lower() == region.lower()]

    if category and category != "all":
        destinations = [d for d in destinations if category.lower() in d["category"].lower()]

    if search:
        destinations = [
            d for d in destinations
            if search in d["name"].lower()
            or search in d["state"].lower()
            or search in d["title"].lower()
            or any(search in h.lower() for h in d["highlights"])
        ]

    return jsonify({"success": True, "count": len(destinations), "data": destinations})

@app.route("/api/destinations/<dest_id>", methods=["GET"])
def api_destination_detail(dest_id):
    """Retrieve detailed information for a specific destination."""
    dest = get_destination_by_id(dest_id)
    if not dest:
        return jsonify({"success": False, "error": "Destination not found"}), 404
    return jsonify({"success": True, "data": dest})

@app.route("/api/attractions", methods=["GET"])
def api_attractions():
    """Get attractions, optionally filtered by destination."""
    dest_id = request.args.get("destination_id")
    attractions = get_all_attractions()
    if dest_id:
        attractions = [a for a in attractions if a["destination_id"] == dest_id]
    return jsonify({"success": True, "count": len(attractions), "data": attractions})

@app.route("/api/transport", methods=["GET"])
def api_transport():
    """Get available transport routes."""
    origin = request.args.get("origin")
    dest = request.args.get("destination")

    routes = TRANSPORT_ROUTES
    if origin:
        routes = [r for r in routes if origin.lower() in r["origin"].lower()]
    if dest:
        routes = [r for r in routes if dest.lower() in r["destination"].lower()]

    return jsonify({"success": True, "data": routes})

@app.route("/api/planner/generate", methods=["POST"])
def api_generate_itinerary():
    """Generate a custom trip plan and day-by-day itinerary."""
    data = request.get_json() or {}

    dest_id = data.get("destination_id", "jaipur")
    starting_city = data.get("starting_city", "Delhi")
    duration = data.get("duration_days", 3)
    traveler_type = data.get("traveler_type", "Solo")
    budget_tier = data.get("budget_tier", "moderate")
    pace = data.get("pace", "balanced")
    interests = data.get("interests", [])

    itinerary = generate_custom_itinerary(
        dest_id=dest_id,
        starting_city=starting_city,
        duration_days=duration,
        traveler_type=traveler_type,
        budget_tier=budget_tier,
        pace=pace,
        interests=interests
    )

    if not itinerary:
        return jsonify({"success": False, "error": "Unable to generate itinerary for destination"}), 400

    return jsonify({"success": True, "data": itinerary})

@app.route("/api/trips/save", methods=["POST"])
def api_save_trip():
    """Save an itinerary to the database."""
    data = request.get_json() or {}

    trip_id = data.get("id") or f"trip_{uuid.uuid4().hex[:8]}"
    title = data.get("trip_title", "My India Adventure")
    dest_id = data.get("destination_id", "jaipur")
    starting_city = data.get("starting_city", "Delhi")
    traveler_type = data.get("traveler_type", "Solo")
    duration_days = int(data.get("duration_days", 3))
    budget_tier = data.get("budget_tier", "moderate")
    pace = data.get("pace", "balanced")
    itinerary_data = data.get("itinerary_data", {})
    notes = data.get("notes", "")

    saved = save_user_trip(
        trip_id=trip_id,
        title=title,
        dest_id=dest_id,
        starting_city=starting_city,
        traveler_type=traveler_type,
        duration_days=duration_days,
        budget_tier=budget_tier,
        pace=pace,
        itinerary_data=itinerary_data,
        notes=notes
    )

    return jsonify({"success": saved, "trip_id": trip_id, "message": "Trip successfully saved!"})

@app.route("/api/trips", methods=["GET"])
def api_get_saved_trips():
    """Retrieve all saved user trips."""
    trips = get_saved_trips()
    return jsonify({"success": True, "count": len(trips), "data": trips})

@app.route("/api/trips/<trip_id>", methods=["DELETE"])
def api_delete_trip(trip_id):
    """Delete a saved trip."""
    deleted = delete_saved_trip(trip_id)
    return jsonify({"success": deleted, "message": "Trip deleted" if deleted else "Trip not found"})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Ananya AI travel assistant endpoint."""
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    context = data.get("context", "")

    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"}), 400

    bot_reply = ask_travel_ai(query, context=context)
    return jsonify({"success": True, "reply": bot_reply})

@app.route("/api/practical-guide", methods=["GET"])
def api_practical_guide():
    """Return the practical travel handbook."""
    return jsonify({"success": True, "data": PRACTICAL_GUIDE})

@app.route("/api/packing-checklist", methods=["GET"])
def api_packing_checklist():
    """Return the packing checklist items."""
    return jsonify({"success": True, "data": PACKING_ITEMS})

# ----------------- ERROR HANDLERS -----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal Server Error: {e}")
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
