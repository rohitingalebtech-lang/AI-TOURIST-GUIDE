"""
database.py
SQLite database schema, initialization, and data access functions for Personalized AI Tourist Guide.
"""

import sqlite3
import json
import os
from travel_data import DESTINATIONS, ATTRACTIONS

DB_FILE = os.path.join(os.path.dirname(__file__), "travel_guide.db")

def get_db_connection():
    """Returns a connection to the SQLite database with row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database tables and populates seed data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Destinations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS destinations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        state TEXT NOT NULL,
        region TEXT NOT NULL,
        category TEXT NOT NULL,
        best_season TEXT NOT NULL,
        ideal_days TEXT NOT NULL,
        avg_daily_budget INTEGER NOT NULL,
        rating REAL NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        image TEXT NOT NULL,
        hero_caption TEXT,
        description TEXT NOT NULL,
        highlights TEXT NOT NULL,
        famous_foods TEXT NOT NULL,
        culture_tips TEXT NOT NULL,
        how_to_reach TEXT NOT NULL
    );
    """)

    # Attractions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attractions (
        id TEXT PRIMARY KEY,
        destination_id TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        entry_fee_inr INTEGER NOT NULL,
        entry_fee_foreign INTEGER NOT NULL,
        timings TEXT NOT NULL,
        ideal_duration TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        image TEXT NOT NULL,
        description TEXT NOT NULL,
        insider_tip TEXT,
        FOREIGN KEY (destination_id) REFERENCES destinations (id)
    );
    """)

    # Saved Trips Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_trips (
        id TEXT PRIMARY KEY,
        trip_title TEXT NOT NULL,
        destination_id TEXT NOT NULL,
        starting_city TEXT NOT NULL,
        traveler_type TEXT NOT NULL,
        duration_days INTEGER NOT NULL,
        budget_tier TEXT NOT NULL,
        pace TEXT NOT NULL,
        itinerary_data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    );
    """)

    # Chat history / queries log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        intent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Seed data if empty
    cursor.execute("SELECT COUNT(*) FROM destinations")
    count = cursor.fetchone()[0]

    if count == 0:
        for dest in DESTINATIONS:
            cursor.execute("""
            INSERT INTO destinations (
                id, name, title, state, region, category, best_season, ideal_days,
                avg_daily_budget, rating, lat, lng, image, hero_caption, description,
                highlights, famous_foods, culture_tips, how_to_reach
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dest["id"],
                dest["name"],
                dest["title"],
                dest["state"],
                dest["region"],
                dest["category"],
                dest["best_season"],
                dest["ideal_days"],
                dest["avg_daily_budget"],
                dest["rating"],
                dest["coordinates"][0],
                dest["coordinates"][1],
                dest["image"],
                dest.get("hero_caption", ""),
                dest["description"],
                json.dumps(dest["highlights"]),
                json.dumps(dest["famous_foods"]),
                json.dumps(dest["culture_tips"]),
                json.dumps(dest["how_to_reach"])
            ))

        for attr in ATTRACTIONS:
            cursor.execute("""
            INSERT INTO attractions (
                id, destination_id, name, category, entry_fee_inr, entry_fee_foreign,
                timings, ideal_duration, lat, lng, image, description, insider_tip
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attr["id"],
                attr["destination_id"],
                attr["name"],
                attr["category"],
                attr["entry_fee_inr"],
                attr["entry_fee_foreign"],
                attr["timings"],
                attr["ideal_duration"],
                attr["coordinates"][0],
                attr["coordinates"][1],
                attr["image"],
                attr["description"],
                attr.get("insider_tip", "")
            ))
        conn.commit()

    conn.close()

def get_all_destinations():
    """Retrieve all destinations formatted as dictionaries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations ORDER BY rating DESC, name ASC")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["highlights"] = json.loads(d["highlights"])
        d["famous_foods"] = json.loads(d["famous_foods"])
        d["culture_tips"] = json.loads(d["culture_tips"])
        d["how_to_reach"] = json.loads(d["how_to_reach"])
        d["coordinates"] = [d["lat"], d["lng"]]
        result.append(d)
    return result

def get_destination_by_id(dest_id):
    """Retrieve a single destination by ID along with its attractions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations WHERE id = ?", (dest_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None

    dest = dict(row)
    dest["highlights"] = json.loads(dest["highlights"])
    dest["famous_foods"] = json.loads(dest["famous_foods"])
    dest["culture_tips"] = json.loads(dest["culture_tips"])
    dest["how_to_reach"] = json.loads(dest["how_to_reach"])
    dest["coordinates"] = [dest["lat"], dest["lng"]]

    # Fetch attractions
    cursor.execute("SELECT * FROM attractions WHERE destination_id = ? ORDER BY name ASC", (dest_id,))
    attr_rows = cursor.fetchall()
    conn.close()

    dest["attractions"] = []
    for ar in attr_rows:
        ad = dict(ar)
        ad["coordinates"] = [ad["lat"], ad["lng"]]
        dest["attractions"].append(ad)

    return dest

def get_all_attractions():
    """Retrieve all attractions across destinations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, d.name as destination_name, d.state as destination_state 
        FROM attractions a 
        JOIN destinations d ON a.destination_id = d.id 
        ORDER BY a.name ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        d["coordinates"] = [d["lat"], d["lng"]]
        results.append(d)
    return results

def save_user_trip(trip_id, title, dest_id, starting_city, traveler_type, duration_days, budget_tier, pace, itinerary_data, notes=""):
    """Persist a generated trip itinerary to SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO saved_trips (
            id, trip_title, destination_id, starting_city, traveler_type,
            duration_days, budget_tier, pace, itinerary_data, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trip_id,
        title,
        dest_id,
        starting_city,
        traveler_type,
        duration_days,
        budget_tier,
        pace,
        json.dumps(itinerary_data),
        notes
    ))
    conn.commit()
    conn.close()
    return True

def get_saved_trips():
    """Fetch all saved user trips."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*, d.name as dest_name, d.state as dest_state, d.image as dest_image 
        FROM saved_trips s 
        LEFT JOIN destinations d ON s.destination_id = d.id 
        ORDER BY s.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        item = dict(r)
        item["itinerary_data"] = json.loads(item["itinerary_data"])
        results.append(item)
    return results

def delete_saved_trip(trip_id):
    """Delete a saved trip by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_trips WHERE id = ?", (trip_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def log_chat(query, response, intent="general"):
    """Log an interaction in the chat logs table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_logs (query, response, intent) VALUES (?, ?, ?)
    """, (query, response, intent))
    conn.commit()
    conn.close()
