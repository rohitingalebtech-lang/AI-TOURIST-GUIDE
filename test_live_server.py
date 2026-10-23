"""
test_live_server.py
Direct HTTP integration test against the running Flask web server.
"""

import sys
import requests
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:5000"

def test_live_server():
    print("Testing live server at", BASE)

    # 1. Homepage
    r0 = requests.get(BASE)
    assert r0.status_code == 200
    assert "Yātrā AI" in r0.text
    print("[OK] Homepage (200 OK): Brand, HTML, and assets hydrated")

    # 2. Destinations API
    r1 = requests.get(f"{BASE}/api/destinations")
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["success"]
    print(f"[OK] /api/destinations: {d1['count']} destinations loaded")

    # 3. Destination Detail
    r2 = requests.get(f"{BASE}/api/destinations/jaipur")
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["data"]["name"] == "Jaipur"
    print(f"[OK] /api/destinations/jaipur: {d2['data']['name']} with {len(d2['data']['attractions'])} attractions")

    # 4. Transport Routes
    r3 = requests.get(f"{BASE}/api/transport")
    assert r3.status_code == 200
    d3 = r3.json()
    print(f"[OK] /api/transport: {len(d3['data'])} routes available")

    # 5. Itinerary Planner
    r4 = requests.post(f"{BASE}/api/planner/generate", json={
        "destination_id": "jaipur",
        "starting_city": "Delhi",
        "duration_days": 3,
        "traveler_type": "Couple / Romantic",
        "budget_tier": "moderate",
        "pace": "balanced"
    })
    assert r4.status_code == 200
    d4 = r4.json()
    assert d4["success"]
    print(f"[OK] /api/planner/generate: {len(d4['data']['days'])} days created. Total budget: {d4['data']['summary']['total_estimated_budget_inr']}")

    # 6. Chatbot Ananya
    r5 = requests.post(f"{BASE}/api/chat", json={"query": "How to book trains on IRCTC?"})
    assert r5.status_code == 200
    d5 = r5.json()
    assert "IRCTC" in d5["reply"]
    print("[OK] /api/chat: Ananya responded with IRCTC guidance")

    # 7. Save Trip
    r6 = requests.post(f"{BASE}/api/trips/save", json={
        "trip_title": "Jaipur Romantic Weekend",
        "destination_id": "jaipur",
        "starting_city": "Delhi",
        "traveler_type": "Couple / Romantic",
        "duration_days": 3,
        "budget_tier": "moderate",
        "pace": "balanced",
        "itinerary_data": d4["data"]
    })
    assert r6.status_code == 200
    d6 = r6.json()
    trip_id = d6["trip_id"]
    print(f"[OK] /api/trips/save: {d6['message']} (Trip ID: {trip_id})")

    # 8. Printable View
    r7 = requests.get(f"{BASE}/trip/print/{trip_id}")
    assert r7.status_code == 200
    assert "Jaipur Romantic Weekend" in r7.text
    print(f"[OK] /trip/print/{trip_id}: Print & PDF view generated ({len(r7.text)} bytes)")

    # 9. Practical Guide
    r8 = requests.get(f"{BASE}/api/practical-guide")
    assert r8.status_code == 200
    assert "visas" in r8.json()["data"]
    print("[OK] /api/practical-guide: Handbook data verified")

    # 10. Packing Checklist
    r9 = requests.get(f"{BASE}/api/packing-checklist")
    assert r9.status_code == 200
    assert len(r9.json()["data"]) >= 10
    print(f"[OK] /api/packing-checklist: {len(r9.json()['data'])} checklist items verified")

    print("\nALL 10 LIVE SERVER INTEGRATION TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_live_server()
