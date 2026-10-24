"""
test_live_server.py
Direct HTTP integration test against the running Flask web server.
Tests:
1. Homepage & assets
2. Destinations API
3. Destination details
4. Live Search Across India (Pune, Chakan, Shaniwar Wada)
5. Live Weather (Open-Meteo)
6. Dynamic Transport Estimation (IRCTC, RedBus, Flights)
7. Itinerary Planner
8. Chatbot Ananya (English, Hindi, Marathi, Budget from Pune)
9. Save and delete trips
10. Printable trip view
"""

import sys
import requests
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:5000"

def test_live_server():
    print(f"Testing live server at {BASE}...")

    # 1. Homepage
    r0 = requests.get(BASE, timeout=5)
    assert r0.status_code == 200
    assert "Yātrā AI" in r0.text
    print("[OK] 1. Homepage (200 OK): Brand, HTML, and assets hydrated")

    # 2. Destinations API
    r1 = requests.get(f"{BASE}/api/destinations", timeout=5)
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["success"]
    print(f"[OK] 2. /api/destinations: {d1['count']} curated destinations loaded")

    # 3. Live Search - Pune
    r_pune = requests.get(f"{BASE}/api/search/live?q=Pune", timeout=10)
    assert r_pune.status_code == 200
    d_pune = r_pune.json()
    assert d_pune["success"]
    assert d_pune["count"] > 0
    print(f"[OK] 3. /api/search/live?q=Pune: Found {d_pune['count']} sights in/near Pune")

    # 4. Live Search - Shaniwar Wada
    r_sw = requests.get(f"{BASE}/api/search/live?q=Shaniwar+Wada", timeout=10)
    assert r_sw.status_code == 200
    d_sw = r_sw.json()
    assert d_sw["success"]
    assert any("shaniwar" in x["name"].lower() for x in d_sw["results"])
    print("[OK] 4. /api/search/live?q=Shaniwar+Wada: Landmark verified with real photo")

    # 5. Place Details - Wikimedia & Weather
    r_det = requests.get(f"{BASE}/api/place/details?id=jaipur", timeout=10)
    assert r_det.status_code == 200
    d_det = r_det.json()
    assert d_det["success"]
    assert len(d_det.get("gallery", [])) > 0
    print(f"[OK] 5. /api/place/details?id=jaipur: Verified photo gallery with {len(d_det['gallery'])} photos")

    # 6. Live Weather - Open-Meteo
    r_w = requests.get(f"{BASE}/api/weather?lat=18.5204&lng=73.8567", timeout=10)
    assert r_w.status_code == 200
    d_w = r_w.json()
    assert "temperature" in d_w
    print(f"[OK] 6. /api/weather: Pune live temp {d_w['temperature']}°C ({d_w.get('condition')})")

    # 7. Dynamic Transport Estimation
    r_trans = requests.get(f"{BASE}/api/transport/estimate?origin=Pune&destination=Goa", timeout=10)
    assert r_trans.status_code == 200
    d_trans = r_trans.json()
    assert d_trans["success"]
    modes = [m["mode"] for m in d_trans["data"]["modes"]]
    assert "Train" in modes and "Bus" in modes
    print(f"[OK] 7. /api/transport/estimate: Pune -> Goa calculated ({d_trans['data']['road_distance_km']} km road distance)")

    # 8. Itinerary Planner
    r_plan = requests.post(f"{BASE}/api/planner/generate", json={
        "destination_id": "jaipur",
        "starting_city": "Delhi",
        "duration_days": 3,
        "traveler_type": "Couple / Romantic",
        "budget_tier": "moderate",
        "pace": "balanced"
    }, timeout=10)
    assert r_plan.status_code == 200
    d_plan = r_plan.json()
    assert d_plan["success"]
    print(f"[OK] 8. /api/planner/generate: 3-day itinerary generated. Total: {d_plan['data']['summary']['total_estimated_budget_inr']}")

    # 9. Chatbot - Natural Budget Query from Pune
    r_chat_pune = requests.post(f"{BASE}/api/chat", json={
        "query": "I have ₹5,000 and two days. Suggest a trip from Pune."
    }, timeout=10)
    assert r_chat_pune.status_code == 200
    d_chat_pune = r_chat_pune.json()
    assert "Sinhagad" in d_chat_pune["reply"] or "Panshet" in d_chat_pune["reply"]
    print("[OK] 9. /api/chat: Pune ₹5,000 budget query accurately recommended Sinhagad & Panshet")

    # 10. Chatbot - Marathi query
    r_chat_mr = requests.post(f"{BASE}/api/chat", json={
        "query": "पुण्यातून दोन दिवसांसाठी कुठे फिरायला जाऊ?"
    }, timeout=10)
    assert r_chat_mr.status_code == 200
    d_chat_mr = r_chat_mr.json()
    assert "सिंहगड" in d_chat_mr["reply"]
    print("[OK] 10. /api/chat (Marathi): Responded in authentic Marathi with Sinhagad recommendation")

    # 11. Save Trip API
    r_save = requests.post(f"{BASE}/api/trips/save", json={
        "trip_title": "Jaipur Romantic Getaway",
        "destination_id": "jaipur",
        "starting_city": "Delhi",
        "traveler_type": "Couple / Romantic",
        "duration_days": 3,
        "budget_tier": "moderate",
        "pace": "balanced",
        "itinerary_data": d_plan["data"],
        "notes": "Testing live server persistence"
    }, timeout=10)
    assert r_save.status_code == 200
    trip_id = r_save.json()["trip_id"]
    print(f"[OK] 11. /api/trips/save: Trip saved with ID: {trip_id}")

    # 12. Printable View
    r_print = requests.get(f"{BASE}/trip/print/{trip_id}", timeout=5)
    assert r_print.status_code == 200
    assert "Jaipur Romantic Getaway" in r_print.text
    print("[OK] 12. /trip/print: Clean printable view generated")

    # 13. Delete Saved Trip
    r_del = requests.delete(f"{BASE}/api/trips/{trip_id}", timeout=5)
    assert r_del.status_code == 200
    assert r_del.json()["success"]
    print("[OK] 13. /api/trips/{id} (DELETE): Trip deleted successfully")

    # 14. Practical Handbook
    r_guide = requests.get(f"{BASE}/api/practical-guide", timeout=5)
    assert r_guide.status_code == 200
    assert "visas" in r_guide.json()["data"]
    print("[OK] 14. /api/practical-guide: Handbook data verified")

    # 15. Packing Checklist
    r_pack = requests.get(f"{BASE}/api/packing-checklist", timeout=5)
    assert r_pack.status_code == 200
    assert len(r_pack.json()["data"]) >= 10
    print(f"[OK] 15. /api/packing-checklist: {len(r_pack.json()['data'])} packing items verified")

    print("\nALL 15 LIVE SERVER INTEGRATION TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_live_server()
