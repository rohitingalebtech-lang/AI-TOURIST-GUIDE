"""
test_app.py
Comprehensive automated test suite verifying:
1. Application startup and routes
2. Search across India (Pune, Delhi, Goa, Chakan, Shaniwar Wada)
3. Empty search and offline fallback handling
4. Destination details and Wikimedia image fallback
5. Open-Meteo live weather endpoint
6. Transport route calculation and official booking links
7. Budget planner validation and itinerary generation
8. Multi-lingual AI travel assistant ("Ananya") in English, Hindi, and Marathi
9. Database persistence, trip saving and deletion
10. Production security headers
"""

import unittest
import json
from app import app
from database import init_db, get_all_destinations, get_destination_by_id, get_all_attractions
from ai_engine import generate_custom_itinerary, ask_travel_ai
from services.geo_service import search_india_all, get_place_full_details, get_live_weather, estimate_transport_modes

class TravelAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            init_db()

    # 1. DATABASE & SEEDING TESTS
    def test_database_seeding(self):
        destinations = get_all_destinations()
        self.assertGreaterEqual(len(destinations), 10)
        self.assertTrue(any(d["id"] == "jaipur" for d in destinations))
        self.assertTrue(any(d["id"] == "munnar" for d in destinations))
        
        attractions = get_all_attractions()
        self.assertGreaterEqual(len(attractions), 10)

    def test_destination_detail(self):
        dest = get_destination_by_id("jaipur")
        self.assertIsNotNone(dest)
        self.assertEqual(dest["name"], "Jaipur")
        self.assertIn("highlights", dest)
        self.assertIn("attractions", dest)
        self.assertGreater(len(dest["attractions"]), 0)

    # 2. SEARCH ACROSS INDIA TESTS (Pune, Delhi, Goa, Chakan, Shaniwar Wada)
    def test_search_pune(self):
        res = self.app.get("/api/search/live?q=Pune")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreater(data["count"], 0)
        # Sights or city should match Pune
        has_pune = any("pune" in r["name"].lower() or "pune" in r.get("location", "").lower() for r in data["results"])
        self.assertTrue(has_pune)

    def test_search_delhi(self):
        res = self.app.get("/api/search/live?q=Delhi")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreater(data["count"], 0)

    def test_search_goa(self):
        res = self.app.get("/api/search/live?q=Goa")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreater(data["count"], 0)

    def test_search_chakan(self):
        res = self.app.get("/api/search/live?q=Chakan")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreater(data["count"], 0)

    def test_search_shaniwar_wada(self):
        res = self.app.get("/api/search/live?q=Shaniwar+Wada")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreater(data["count"], 0)
        self.assertTrue(any("shaniwar" in r["name"].lower() for r in data["results"]))

    # 3. EMPTY SEARCH & FALLBACK TESTS
    def test_search_no_results(self):
        res = self.app.get("/api/search/live?q=xyznonexistentplace123456")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["count"], 0)

    def test_search_empty_query_returns_curated(self):
        res = self.app.get("/api/search/live?q=")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["count"], 10)

    # 4. DESTINATION DETAILS & WIKIMEDIA IMAGE FALLBACK
    def test_place_details_curated(self):
        res = self.app.get("/api/place/details?id=jaipur")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["name"], "Jaipur")
        self.assertGreater(len(data["gallery"]), 0)

    def test_place_details_live_landmark(self):
        res = self.app.get("/api/place/details?id=Shaniwar_Wada")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertIn("Shaniwar", data["name"])
        self.assertIn("gallery", data)

    def test_place_details_missing_param(self):
        res = self.app.get("/api/place/details")
        self.assertEqual(res.status_code, 400)

    # 5. OPEN-METEO LIVE WEATHER ENDPOINT
    def test_weather_api(self):
        # Coordinates for Pune
        res = self.app.get("/api/weather?lat=18.5204&lng=73.8567")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("temperature", data)
        self.assertIn("condition", data)

    def test_weather_invalid_coords(self):
        res = self.app.get("/api/weather?lat=abc&lng=def")
        self.assertEqual(res.status_code, 400)

    # 6. DYNAMIC TRANSPORT ROUTE ESTIMATION
    def test_transport_estimate(self):
        res = self.app.get("/api/transport/estimate?origin=Pune&destination=Goa")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertIn("modes", data["data"])
        modes = [m["mode"] for m in data["data"]["modes"]]
        self.assertIn("Train", modes)
        self.assertIn("Bus", modes)
        self.assertIn("Taxi / Car", modes)

    # 7. ITINERARY PLANNER & BUDGET TESTS
    def test_itinerary_generator(self):
        plan = generate_custom_itinerary(
            dest_id="jaipur",
            starting_city="Delhi",
            duration_days=3,
            traveler_type="Couple / Romantic",
            budget_tier="moderate",
            pace="balanced"
        )
        self.assertIsNotNone(plan)
        self.assertEqual(len(plan["days"]), 3)
        self.assertIn("morning", plan["days"][0])
        self.assertIn("afternoon", plan["days"][0])
        self.assertIn("evening", plan["days"][0])
        self.assertIn("summary", plan)
        self.assertIn("budget_breakdown", plan["summary"])
        self.assertIn("buffer_and_tips", plan["summary"]["budget_breakdown"])

    # 8. MULTI-LINGUAL CHATBOT ("ANANYA") NATURAL QUERIES
    def test_chat_pune_budget(self):
        reply = ask_travel_ai("I have ₹5,000 and two days. Suggest a trip from Pune.")
        self.assertTrue("Sinhagad" in reply or "Panshet" in reply or "Lonavala" in reply)
        self.assertIn("5,000", reply)

    def test_chat_jaipur_historic(self):
        reply = ask_travel_ai("Which historical places can I visit in Jaipur?")
        self.assertIn("Amber Fort", reply)
        self.assertIn("Hawa Mahal", reply)

    def test_chat_goa_family(self):
        reply = ask_travel_ai("Plan a three-day family trip to Goa.")
        self.assertTrue("Family" in reply or "family" in reply)
        self.assertTrue("Aguada" in reply or "Spice" in reply)

    def test_chat_monsoon_packing(self):
        reply = ask_travel_ai("What should I carry for a monsoon trip?")
        self.assertIn("umbrella", reply.lower())
        self.assertIn("waterproof", reply.lower())

    def test_chat_hindi_query(self):
        reply = ask_travel_ai("जयपुर में कौन से ऐतिहासिक स्थल देखने लायक हैं?")
        self.assertIn("आमेर", reply)

    def test_chat_marathi_query(self):
        reply = ask_travel_ai("पुण्यातून दोन दिवसांसाठी कुठे फिरायला जाऊ?")
        self.assertIn("सिंहगड", reply)

    def test_chat_irctc_intent(self):
        reply = ask_travel_ai("How do I book a train ticket on IRCTC?")
        self.assertIn("IRCTC", reply)

    def test_chat_upi_intent(self):
        reply = ask_travel_ai("Can foreign tourists use UPI payments in India?")
        self.assertIn("UPI", reply)

    # 9. PERSISTENCE & SAVED TRIPS API
    def test_save_and_delete_trip(self):
        # 1. Generate itinerary
        res_plan = self.app.post("/api/planner/generate", json={
            "destination_id": "goa",
            "starting_city": "Mumbai",
            "duration_days": 4,
            "traveler_type": "Group of Friends",
            "budget_tier": "moderate",
            "pace": "balanced"
        })
        self.assertEqual(res_plan.status_code, 200)
        plan_data = json.loads(res_plan.data)
        self.assertTrue(plan_data["success"])

        # 2. Save trip
        res_save = self.app.post("/api/trips/save", json={
            "trip_title": "Goa Beach Friends Trip",
            "destination_id": "goa",
            "starting_city": "Mumbai",
            "traveler_type": "Group of Friends",
            "duration_days": 4,
            "budget_tier": "moderate",
            "pace": "balanced",
            "itinerary_data": plan_data["data"],
            "notes": "Testing persistence"
        })
        self.assertEqual(res_save.status_code, 200)
        save_res = json.loads(res_save.data)
        self.assertTrue(save_res["success"])
        saved_id = save_res["trip_id"]

        # 3. Retrieve saved trips
        res_get = self.app.get("/api/trips")
        self.assertEqual(res_get.status_code, 200)
        trips_list = json.loads(res_get.data)
        self.assertTrue(any(t["id"] == saved_id for t in trips_list["data"]))

        # 4. View print page
        res_print = self.app.get(f"/trip/print/{saved_id}")
        self.assertEqual(res_print.status_code, 200)
        self.assertIn(b"Goa Beach Friends Trip", res_print.data)

        # 5. Delete saved trip
        res_del = self.app.delete(f"/api/trips/{saved_id}")
        self.assertEqual(res_del.status_code, 200)
        del_res = json.loads(res_del.data)
        self.assertTrue(del_res["success"])

    # 10. SECURITY HEADERS
    def test_security_headers(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(res.headers.get("X-XSS-Protection"), "1; mode=block")
        self.assertIn("strict-origin", res.headers.get("Referrer-Policy"))

if __name__ == "__main__":
    unittest.main()
