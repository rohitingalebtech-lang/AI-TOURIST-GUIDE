"""
test_app.py
Comprehensive automated test suite verifying database, APIs, AI itinerary planner, and chat engine.
"""

import unittest
import json
from app import app
from database import init_db, get_all_destinations, get_destination_by_id, get_all_attractions
from ai_engine import generate_custom_itinerary, ask_travel_ai

class TravelAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            init_db()

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

    def test_ai_chatbot(self):
        # Test IRCTC intent
        reply_irctc = ask_travel_ai("How do I book a train ticket on IRCTC?")
        self.assertIn("IRCTC", reply_irctc)

        # Test UPI intent
        reply_upi = ask_travel_ai("Can foreign tourists use UPI payments in India?")
        self.assertIn("UPI", reply_upi)

        # Test Destination query
        reply_dest = ask_travel_ai("Tell me about visiting Munnar")
        self.assertIn("Munnar", reply_dest)

    def test_api_endpoints(self):
        # 1. Homepage
        res_home = self.app.get("/")
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b"Y\xc4\x81tr\xc4\x81 AI", res_home.data)

        # 2. Destinations API
        res_dest = self.app.get("/api/destinations")
        self.assertEqual(res_dest.status_code, 200)
        data_dest = json.loads(res_dest.data)
        self.assertTrue(data_dest["success"])
        self.assertGreaterEqual(data_dest["count"], 10)

        # 3. Transport API
        res_trans = self.app.get("/api/transport")
        self.assertEqual(res_trans.status_code, 200)
        data_trans = json.loads(res_trans.data)
        self.assertTrue(data_trans["success"])
        self.assertGreaterEqual(len(data_trans["data"]), 3)

        # 4. Generate Itinerary API
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
        self.assertEqual(len(plan_data["data"]["days"]), 4)

        # 5. Save Trip API
        res_save = self.app.post("/api/trips/save", json={
            "trip_title": "Goa Beach Holiday",
            "destination_id": "goa",
            "starting_city": "Mumbai",
            "traveler_type": "Group of Friends",
            "duration_days": 4,
            "budget_tier": "moderate",
            "pace": "balanced",
            "itinerary_data": plan_data["data"],
            "notes": "Testing trip persistence"
        })
        self.assertEqual(res_save.status_code, 200)
        save_res = json.loads(res_save.data)
        self.assertTrue(save_res["success"])
        saved_id = save_res["trip_id"]

        # 6. Get Saved Trips
        res_get_trips = self.app.get("/api/trips")
        self.assertEqual(res_get_trips.status_code, 200)
        trips_list = json.loads(res_get_trips.data)
        self.assertTrue(any(t["id"] == saved_id for t in trips_list["data"]))

        # 7. Print Trip Page
        res_print = self.app.get(f"/trip/print/{saved_id}")
        self.assertEqual(res_print.status_code, 200)
        self.assertIn(b"Goa Beach Holiday", res_print.data)

        # 8. Delete Trip API
        res_del = self.app.delete(f"/api/trips/{saved_id}")
        self.assertEqual(res_del.status_code, 200)
        del_data = json.loads(res_del.data)
        self.assertTrue(del_data["success"])

        # 9. Chat API
        res_chat = self.app.post("/api/chat", json={"query": "What is the dress code for temples?"})
        self.assertEqual(res_chat.status_code, 200)
        chat_data = json.loads(res_chat.data)
        self.assertTrue(chat_data["success"])
        self.assertIn("Temple", chat_data["reply"])

if __name__ == "__main__":
    unittest.main()
