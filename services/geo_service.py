"""
services/geo_service.py
Geographic and attraction search service covering all of India.
Uses OpenStreetMap Nominatim for geocoding, Wikipedia/Wikimedia Commons for
real attraction photos and verified descriptions, Open-Meteo for live weather,
and Haversine routing for transport cost/time estimates.
Includes local SQLite caching to respect rate limits and ensure offline resilience.
"""

import math
import time
import json
import logging
import sqlite3
import os
import re
import requests
from database import DB_FILE, get_all_destinations, get_destination_by_id

logger = logging.getLogger(__name__)

USER_AGENT = "PersonalisedAITouristGuideIndia/2.0 (Academic/Traveler Utility; contact: tour-guide@yatra.local)"
REQUEST_TIMEOUT = 5  # seconds

# In-memory fast cache
_MEMORY_CACHE = {}

def get_cache_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_cache_table():
    """Create persistent cache table for geocoding and external API calls."""
    try:
        conn = get_cache_conn()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_cache (
            cache_key TEXT PRIMARY KEY,
            data_json TEXT NOT NULL,
            created_at REAL NOT NULL,
            expires_at REAL NOT NULL
        );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Could not initialize cache table: {e}")

init_cache_table()

def get_cached_item(cache_key):
    now = time.time()
    if cache_key in _MEMORY_CACHE:
        val, exp = _MEMORY_CACHE[cache_key]
        if now < exp:
            return val
        else:
            del _MEMORY_CACHE[cache_key]

    try:
        conn = get_cache_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT data_json, expires_at FROM api_cache WHERE cache_key = ?", (cache_key,))
        row = cursor.fetchone()
        conn.close()
        if row and row["expires_at"] > now:
            data = json.loads(row["data_json"])
            _MEMORY_CACHE[cache_key] = (data, row["expires_at"])
            return data
    except Exception as e:
        logger.debug(f"Cache read error: {e}")
    return None

def set_cached_item(cache_key, data, ttl_seconds=86400):
    now = time.time()
    expires_at = now + ttl_seconds
    _MEMORY_CACHE[cache_key] = (data, expires_at)
    try:
        conn = get_cache_conn()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO api_cache (cache_key, data_json, created_at, expires_at)
        VALUES (?, ?, ?, ?)
        """, (cache_key, json.dumps(data), now, expires_at))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.debug(f"Cache write error: {e}")

# Rate limiter for Nominatim (1 request per second policy)
_LAST_NOMINATIM_CALL = 0

def _rate_limit_nominatim():
    global _LAST_NOMINATIM_CALL
    elapsed = time.time() - _LAST_NOMINATIM_CALL
    if elapsed < 1.05:
        time.sleep(1.05 - elapsed)
    _LAST_NOMINATIM_CALL = time.time()

# ----------------- GEOCODING VIA NOMINATIM -----------------
def geocode_place(query):
    """
    Geocode an Indian city, town, or landmark using Nominatim.
    Returns dict with lat, lng, name, display_name, state, country or None.
    """
    clean_q = query.strip()
    if not clean_q:
        return None

    cache_key = f"nominatim_geo:{clean_q.lower()}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    # Check local curated destinations first
    for dest in get_all_destinations():
        if clean_q.lower() == dest["name"].lower() or dest["name"].lower() in clean_q.lower():
            res = {
                "name": dest["name"],
                "display_name": f"{dest['name']}, {dest['state']}, India",
                "lat": dest["coordinates"][0],
                "lng": dest["coordinates"][1],
                "state": dest["state"],
                "type": "city",
                "is_curated": True,
                "curated_id": dest["id"]
            }
            set_cached_item(cache_key, res, ttl_seconds=604800)
            return res

    _rate_limit_nominatim()
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{clean_q}, India",
        "format": "json",
        "countrycodes": "in",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {"User-Agent": USER_AGENT}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            results = resp.json()
            if results:
                first = results[0]
                addr = first.get("address", {})
                state = addr.get("state") or addr.get("region") or "India"
                name = first.get("name") or clean_q.title()
                res = {
                    "name": name,
                    "display_name": first.get("display_name", f"{name}, India"),
                    "lat": float(first["lat"]),
                    "lng": float(first["lon"]),
                    "state": state,
                    "type": first.get("type", "place"),
                    "is_curated": False
                }
                set_cached_item(cache_key, res, ttl_seconds=604800)
                return res
    except Exception as e:
        logger.warning(f"Nominatim geocode failed for '{clean_q}': {e}")

    # Fallback to known Indian major hubs if network unavailable
    fallback_map = {
        "pune": (18.5204, 73.8567, "Maharashtra"),
        "mumbai": (19.0760, 72.8777, "Maharashtra"),
        "delhi": (28.6139, 77.2090, "Delhi"),
        "jaipur": (26.9124, 75.7873, "Rajasthan"),
        "goa": (15.2993, 74.1240, "Goa"),
        "manali": (32.2432, 77.1892, "Himachal Pradesh"),
        "chakan": (18.7594, 73.8574, "Maharashtra"),
        "nashik": (19.9975, 73.7898, "Maharashtra"),
        "hampi": (15.3350, 76.4600, "Karnataka"),
        "shaniwar wada": (18.5196, 73.8553, "Maharashtra"),
        "sinhagad": (18.3663, 73.7558, "Maharashtra"),
        "dagdusheth": (18.5165, 73.8561, "Maharashtra"),
        "ajanta": (20.5519, 75.7033, "Maharashtra"),
        "agra": (27.1767, 78.0081, "Uttar Pradesh"),
        "varanasi": (25.3176, 82.9739, "Uttar Pradesh"),
        "munnar": (10.0889, 77.0595, "Kerala"),
        "bengaluru": (12.9716, 77.5946, "Karnataka"),
        "kolkata": (22.5726, 88.3639, "West Bengal"),
        "chennai": (13.0827, 80.2707, "Tamil Nadu"),
        "hyderabad": (17.3850, 78.4867, "Telangana")
    }
    for k, (lat, lng, st) in fallback_map.items():
        if k in clean_q.lower():
            return {
                "name": clean_q.title(),
                "display_name": f"{clean_q.title()}, {st}, India",
                "lat": lat,
                "lng": lng,
                "state": st,
                "type": "place",
                "is_curated": False
            }

    return None

# ----------------- WIKIPEDIA / WIKIMEDIA ATTRACTIONS SEARCH -----------------
def search_wikipedia_attractions(lat, lng, radius_m=10000, limit=12):
    """
    Find nearby notable attractions via Wikipedia GeoSearch (max radius is 10000m).
    Fetches real images, extracts, and categories.
    """
    safe_radius = min(int(radius_m), 10000)
    cache_key = f"wiki_geo:{round(lat, 2)}_{round(lng, 2)}_{safe_radius}_{limit}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    headers = {"User-Agent": USER_AGENT}
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{lat}|{lng}",
        "gsradius": safe_radius,
        "gslimit": limit,
        "format": "json"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("query", {}).get("geosearch", [])
            if not items:
                return []

            page_ids = [str(item["pageid"]) for item in items]
            
            details_params = {
                "action": "query",
                "pageids": "|".join(page_ids),
                "prop": "pageimages|extracts|info",
                "inprop": "url",
                "pithumbsize": 800,
                "exintro": 1,
                "explaintext": 1,
                "exsentences": 2,
                "format": "json"
            }
            det_resp = requests.get(url, params=details_params, headers=headers, timeout=REQUEST_TIMEOUT)
            if det_resp.status_code == 200:
                pages_data = det_resp.json().get("query", {}).get("pages", {})
                attractions = []
                for item in items:
                    pid = str(item["pageid"])
                    page = pages_data.get(pid, {})
                    title = item.get("title", "")
                    
                    # Skip metro stations and administrative sub-districts if possible
                    if any(skip in title.lower() for skip in ["metro station", "railway station", "subdistrict", "constituency"]):
                        continue
                    
                    dist_km = round(item.get("dist", 0) / 1000.0, 1)
                    extract = page.get("extract", "").strip()
                    if not extract:
                        extract = f"Historical and cultural attraction located near {title}."
                    
                    category = categorize_attraction(title, extract)
                    thumb = page.get("thumbnail", {}).get("source")
                    if not thumb:
                        thumb = get_category_fallback_image(category)
                    
                    attractions.append({
                        "id": f"wiki_{pid}",
                        "name": title,
                        "category": category,
                        "description": extract,
                        "lat": item.get("lat"),
                        "lng": item.get("lon"),
                        "distance_km": dist_km,
                        "image": thumb,
                        "image_attribution": "Wikimedia Commons / Wikipedia (CC-BY-SA)",
                        "wiki_url": page.get("fullurl", f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"),
                        "source": "OpenStreetMap / Wikipedia"
                    })
                
                set_cached_item(cache_key, attractions, ttl_seconds=86400 * 3)
                return attractions
    except Exception as e:
        logger.warning(f"Wikipedia geosearch failed: {e}")

    return []

def search_wikipedia_by_text(query, limit=8):
    """
    Search Wikipedia for tourist attractions / monuments matching a text query (e.g., 'Pune tourist attractions', 'Chakan fort').
    """
    cache_key = f"wiki_text_search:{query.lower()}_{limit}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    headers = {"User-Agent": USER_AGENT}
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": f'"{query}" fort OR temple OR monument OR palace OR museum OR caves OR beach OR lake',
        "srlimit": limit,
        "format": "json"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            search_items = resp.json().get("query", {}).get("search", [])
            if not search_items:
                return []

            page_ids = [str(item["pageid"]) for item in search_items]
            details_params = {
                "action": "query",
                "pageids": "|".join(page_ids),
                "prop": "pageimages|extracts|coordinates|info",
                "inprop": "url",
                "pithumbsize": 800,
                "exintro": 1,
                "explaintext": 1,
                "exsentences": 2,
                "format": "json"
            }
            det_resp = requests.get(url, params=details_params, headers=headers, timeout=REQUEST_TIMEOUT)
            if det_resp.status_code == 200:
                pages = det_resp.json().get("query", {}).get("pages", {})
                results = []
                for pid, page in pages.items():
                    title = page.get("title", "")
                    if title.startswith("List of") or "metro" in title.lower():
                        continue
                    extract = page.get("extract", "").strip()
                    category = categorize_attraction(title, extract)
                    thumb = page.get("thumbnail", {}).get("source") or get_category_fallback_image(category)
                    coords = page.get("coordinates", [{}])[0]
                    
                    results.append({
                        "id": f"wiki_{pid}",
                        "name": title,
                        "category": category,
                        "description": extract if extract else f"Famous destination in {query.title()}.",
                        "lat": coords.get("lat"),
                        "lng": coords.get("lon"),
                        "image": thumb,
                        "image_attribution": "Wikimedia Commons / Wikipedia (CC-BY-SA)",
                        "wiki_url": page.get("fullurl"),
                        "source": "Wikimedia / Wikipedia"
                    })
                set_cached_item(cache_key, results, ttl_seconds=86400 * 3)
                return results
    except Exception as e:
        logger.warning(f"Wikipedia text search failed: {e}")

    return []

def search_wikipedia_page(title):
    """
    Search Wikipedia for a single specific attraction or landmark title.
    Returns detailed summary, image, and coordinates.
    """
    cache_key = f"wiki_page:{title.lower()}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    headers = {"User-Agent": USER_AGENT}
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages|extracts|coordinates|info",
        "inprop": "url",
        "pithumbsize": 1000,
        "exintro": 1,
        "explaintext": 1,
        "format": "json"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            pages = resp.json().get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if pid == "-1":
                    continue
                extract = page.get("extract", "")
                coords = page.get("coordinates", [{}])[0]
                category = categorize_attraction(title, extract)
                thumb = page.get("thumbnail", {}).get("source") or get_category_fallback_image(category)
                
                res = {
                    "id": f"wiki_{pid}",
                    "name": page.get("title", title),
                    "category": category,
                    "description": extract,
                    "lat": coords.get("lat"),
                    "lng": coords.get("lon"),
                    "image": thumb,
                    "image_attribution": "Wikimedia Commons / Wikipedia (CC-BY-SA)",
                    "wiki_url": page.get("fullurl"),
                    "source": "Wikimedia / Wikipedia"
                }
                set_cached_item(cache_key, res, ttl_seconds=86400 * 7)
                return res
    except Exception as e:
        logger.warning(f"Failed to fetch Wikipedia page '{title}': {e}")

    return None

def get_wikipedia_images_gallery(title, limit=4):
    """
    Retrieve multiple genuine photos from Wikimedia Commons for a destination/monument.
    """
    cache_key = f"wiki_gallery:{title.lower()}_{limit}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    headers = {"User-Agent": USER_AGENT}
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "images",
        "titles": title,
        "gimlimit": limit + 6,
        "prop": "imageinfo",
        "iiprop": "url|mime|extmetadata",
        "iiurlwidth": 900,
        "format": "json"
    }

    gallery = []
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            pages = resp.json().get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                infos = pdata.get("imageinfo", [])
                if infos:
                    info = infos[0]
                    mime = info.get("mime", "")
                    if "image/jpeg" in mime or "image/png" in mime or "image/webp" in mime:
                        thumb = info.get("thumburl") or info.get("url")
                        # Skip small SVGs, icons, or logos
                        if thumb and not any(ic in thumb.lower() for ic in ["logo", "icon", "stub", "flag", "symbol"]):
                            gallery.append({
                                "url": thumb,
                                "attribution": "Wikimedia Commons (CC-BY-SA)",
                                "title": pdata.get("title", "").replace("File:", "")
                            })
                            if len(gallery) >= limit:
                                break
    except Exception as e:
        logger.debug(f"Gallery fetch error for {title}: {e}")

    if gallery:
        set_cached_item(cache_key, gallery, ttl_seconds=86400 * 7)
    return gallery

def categorize_attraction(name, description):
    text = f"{name} {description}".lower()
    if any(k in text for k in ["fort", "palace", "wada", "haveli", "mahal", "tomb", "monument", "ruins", "heritage", "cave", "museum"]):
        return "Historical & Heritage"
    elif any(k in text for k in ["temple", "mandir", "mosque", "masjid", "gurdwara", "church", "cathedral", "ghat", "spiritual", "shrine", "ashram", "buddhist", "stupa"]):
        return "Spiritual & Sacred"
    elif any(k in text for k in ["beach", "sea", "coast", "cove", "cliff", "lighthouse"]):
        return "Beaches & Coastal"
    elif any(k in text for k in ["hill", "peak", "valley", "pass", "mountain", "trek", "himalaya", "viewpoint", "ghat"]):
        return "Mountains & Hills"
    elif any(k in text for k in ["waterfall", "falls", "lake", "river", "nature", "botanical", "garden", "forest"]):
        return "Nature & Waterfalls"
    elif any(k in text for k in ["wildlife", "national park", "sanctuary", "tiger", "safari", "bird", "zoo"]):
        return "Wildlife & Safari"
    elif any(k in text for k in ["market", "bazaar", "food", "street food", "restaurant", "cuisine", "thali"]):
        return "Food & Bazaars"
    elif any(k in text for k in ["adventure", "rafting", "paragliding", "skiing", "camp"]):
        return "Adventure"
    return "Sightseeing & Culture"

def get_category_fallback_image(category):
    """High-resolution reliable fallback images representing authentic Indian travel categories."""
    fallbacks = {
        "Historical & Heritage": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1000&q=80",
        "Spiritual & Sacred": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1000&q=80",
        "Beaches & Coastal": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=80",
        "Mountains & Hills": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1000&q=80",
        "Nature & Waterfalls": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1000&q=80",
        "Wildlife & Safari": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=1000&q=80",
        "Food & Bazaars": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1000&q=80",
        "Adventure": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1000&q=80"
    }
    return fallbacks.get(category, "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1000&q=80")

# ----------------- UNIFIED SEARCH ALL ACROSS INDIA -----------------
def search_india_all(query, category="all", limit=20):
    """
    Unified search covering any city, town, landmark, temple, fort, or park in India.
    Combines:
    1. Geocoding via Nominatim
    2. Local curated flagship destinations & attractions
    3. Wikipedia & Wikimedia Commons attractions & real photos
    """
    clean_q = query.strip()
    if not clean_q:
        dests = get_all_destinations()
        results = []
        for d in dests[:limit]:
            results.append({
                "id": d["id"],
                "name": d["name"],
                "location": f"{d['state']}, India",
                "state": d["state"],
                "category": d["category"],
                "description": d["title"],
                "full_description": d["description"],
                "lat": d["coordinates"][0],
                "lng": d["coordinates"][1],
                "image": d["image"],
                "image_attribution": "Curated Travel Archive (Unsplash/Wikimedia License)",
                "avg_daily_budget": d["avg_daily_budget"],
                "rating": d["rating"],
                "ideal_days": d["ideal_days"],
                "best_season": d["best_season"],
                "highlights": d["highlights"],
                "is_curated": True
            })
        return {"success": True, "count": len(results), "query": "", "results": results}

    results = []

    # 1. Check if query matches a local curated destination
    for d in get_all_destinations():
        if (clean_q.lower() in d["name"].lower() or 
            clean_q.lower() in d["state"].lower() or 
            any(clean_q.lower() in h.lower() for h in d["highlights"])):
            results.append({
                "id": d["id"],
                "name": d["name"],
                "location": f"{d['state']}, India",
                "state": d["state"],
                "category": d["category"],
                "description": d["title"],
                "full_description": d["description"],
                "lat": d["coordinates"][0],
                "lng": d["coordinates"][1],
                "image": d["image"],
                "image_attribution": "Verified Destination Archive",
                "avg_daily_budget": d["avg_daily_budget"],
                "rating": d["rating"],
                "ideal_days": d["ideal_days"],
                "best_season": d["best_season"],
                "highlights": d["highlights"],
                "is_curated": True
            })

    # 2. Check direct Wikipedia page for query itself (e.g. "Shaniwar Wada", "Chakan", "Sinhagad Fort", "Ajanta Caves")
    direct_page = search_wikipedia_page(clean_q)
    if direct_page and not any(r["name"].lower() == direct_page["name"].lower() for r in results):
        results.insert(0, {
            "id": direct_page["id"],
            "name": direct_page["name"],
            "location": f"India",
            "state": "India",
            "category": direct_page["category"],
            "description": (direct_page["description"][:160] + "...") if len(direct_page["description"]) > 160 else direct_page["description"],
            "full_description": direct_page["description"],
            "lat": direct_page["lat"],
            "lng": direct_page["lng"],
            "distance_km": 0.0,
            "image": direct_page["image"],
            "image_attribution": direct_page["image_attribution"],
            "wiki_url": direct_page.get("wiki_url"),
            "is_curated": False
        })

    # 3. Geocode query via Nominatim
    geo = geocode_place(clean_q)
    if geo:
        target_lat = geo["lat"]
        target_lng = geo["lng"]
        
        # If direct page was added, update its location tag with geocoded state
        if results and results[0].get("id") == direct_page.get("id", "") if direct_page else False:
            results[0]["location"] = f"{geo['name']}, {geo['state']}"
            results[0]["state"] = geo["state"]
            if not results[0]["lat"]:
                results[0]["lat"] = target_lat
                results[0]["lng"] = target_lng

        # A. Query Wikipedia landmark/attraction search first to get iconic sights (e.g. Shaniwar Wada, Aga Khan Palace)
        text_items = search_wikipedia_by_text(geo["name"], limit=8)
        for item in text_items:
            if not any(r["name"].lower() == item["name"].lower() for r in results):
                results.append({
                    "id": item["id"],
                    "name": item["name"],
                    "location": f"{geo['name']}, {geo['state']}",
                    "state": geo["state"],
                    "category": item["category"],
                    "description": (item["description"][:150] + "...") if len(item["description"]) > 150 else item["description"],
                    "full_description": item["description"],
                    "lat": item["lat"] or target_lat,
                    "lng": item["lng"] or target_lng,
                    "image": item["image"],
                    "image_attribution": item["image_attribution"],
                    "wiki_url": item.get("wiki_url"),
                    "is_curated": False
                })

        # B. Supplement with Wikipedia GeoSearch nearby notable attractions
        nearby = search_wikipedia_attractions(target_lat, target_lng, radius_m=10000, limit=10)
        for item in nearby:
            # Skip mere villages/hamlets if we already have good attractions
            desc_lower = item["description"].lower()
            title_lower = item["name"].lower()
            if any(h in title_lower or h in desc_lower for h in ["village in", "census town", "hamlet", "sub-district", "constituency"]) and item["category"] == "Sightseeing & Culture":
                continue

            if not any(r["name"].lower() == item["name"].lower() for r in results):
                results.append({
                    "id": item["id"],
                    "name": item["name"],
                    "location": f"Near {geo['name']}, {geo['state']}",
                    "state": geo["state"],
                    "category": item["category"],
                    "description": (item["description"][:150] + "...") if len(item["description"]) > 150 else item["description"],
                    "full_description": item["description"],
                    "lat": item["lat"] or target_lat,
                    "lng": item["lng"] or target_lng,
                    "distance_km": item["distance_km"],
                    "image": item["image"],
                    "image_attribution": item["image_attribution"],
                    "wiki_url": item.get("wiki_url"),
                    "is_curated": False
                })

    # Filter by category if requested
    if category and category.lower() != "all":
        cat_lower = category.lower()
        results = [r for r in results if cat_lower in r["category"].lower()]

    # Deduplicate by name
    seen_names = set()
    deduped = []
    for r in results:
        normalized = r["name"].strip().lower()
        if normalized not in seen_names:
            seen_names.add(normalized)
            deduped.append(r)

    return {
        "success": True,
        "query": clean_q,
        "geocoded": geo,
        "count": len(deduped),
        "results": deduped[:limit]
    }

# ----------------- DETAILED DESTINATION / PLACE DETAILS -----------------
def get_place_full_details(place_id_or_name):
    """
    Get full details for a destination or attraction:
    Photo gallery, short intro, live weather, verified entry fees notice,
    directions link, activities, visiting tips, and nearby spots.
    """
    # Check if curated destination in DB
    curated = get_destination_by_id(place_id_or_name.lower())
    if curated:
        weather = get_live_weather(curated["coordinates"][0], curated["coordinates"][1])
        gallery = [
            {"url": curated["image"], "attribution": "Verified Destination Archive", "title": curated["name"]}
        ]
        # Add attraction images to gallery
        for a in curated.get("attractions", [])[:3]:
            if a.get("image"):
                gallery.append({"url": a["image"], "attribution": "ASI / Monument Archive", "title": a["name"]})

        return {
            "success": True,
            "id": curated["id"],
            "name": curated["name"],
            "title": curated["title"],
            "state": curated["state"],
            "location": f"{curated['name']}, {curated['state']}, India",
            "category": curated["category"],
            "description": curated["description"],
            "highlights": curated["highlights"],
            "gallery": gallery,
            "coordinates": curated["coordinates"],
            "best_season": curated["best_season"],
            "ideal_days": curated["ideal_days"],
            "avg_daily_budget": curated["avg_daily_budget"],
            "rating": curated["rating"],
            "famous_foods": curated["famous_foods"],
            "culture_tips": curated["culture_tips"],
            "how_to_reach": curated["how_to_reach"],
            "attractions": curated.get("attractions", []),
            "weather": weather,
            "opening_hours": "Typically 09:00 AM - 05:30 PM (ASI monuments). Check individual attractions.",
            "entry_fee_note": "Domestic: ~₹25 - ₹50 per ASI monument; Foreign: ~₹300 - ₹600. Book on asi.payumoney.com or ASI portal.",
            "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={curated['coordinates'][0]},{curated['coordinates'][1]}",
            "is_curated": True
        }

    # Otherwise fetch live from Wikipedia
    clean_title = place_id_or_name.replace("wiki_", "")
    page_info = search_wikipedia_page(clean_title)
    if not page_info:
        # Try direct search
        results = search_india_all(clean_title, limit=1)
        if results["results"]:
            first = results["results"][0]
            clean_title = first["name"]
            page_info = search_wikipedia_page(clean_title) or first

    if not page_info:
        return {"success": False, "error": "Destination details not found"}

    lat = page_info.get("lat") or 20.5937
    lng = page_info.get("lng") or 78.9629

    weather = get_live_weather(lat, lng) if page_info.get("lat") else None
    gallery = get_wikipedia_images_gallery(page_info["name"], limit=4)
    if not gallery and page_info.get("image"):
        gallery = [{"url": page_info["image"], "attribution": page_info.get("image_attribution", "Wikimedia Commons"), "title": page_info["name"]}]

    # Fetch nearby recommendations
    nearby = search_wikipedia_attractions(lat, lng, radius_m=10000, limit=5)
    nearby_clean = [
        {"name": n["name"], "category": n["category"], "distance_km": n.get("distance_km", 0), "image": n["image"]}
        for n in nearby if n["name"].lower() != page_info["name"].lower()
    ]

    return {
        "success": True,
        "id": page_info.get("id", clean_title.lower()),
        "name": page_info["name"],
        "title": f"Explore {page_info['name']}",
        "location": page_info.get("location", f"{page_info['name']}, India"),
        "state": page_info.get("state", "India"),
        "category": page_info.get("category", "Heritage & Culture"),
        "description": page_info.get("description", ""),
        "gallery": gallery,
        "coordinates": [lat, lng],
        "weather": weather,
        "opening_hours": "Please verify local timings and public holiday schedules before visiting.",
        "entry_fee_note": "Entry fees vary or free admission; please check official state tourism / ASI ticket counters.",
        "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={lat},{lng}",
        "wiki_url": page_info.get("wiki_url"),
        "nearby_attractions": nearby_clean,
        "is_curated": False
    }

# ----------------- LIVE WEATHER VIA OPEN-METEO -----------------
def get_live_weather(lat, lng):
    """
    Fetch real-time weather and 3-day forecast from Open-Meteo (Keyless & Free).
    """
    cache_key = f"weather:{round(lat, 2)}_{round(lng, 2)}"
    cached = get_cached_item(cache_key)
    if cached:
        return cached

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "Asia/Kolkata"
    }

    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            cw = data.get("current_weather", {})
            temp = cw.get("temperature")
            wcode = cw.get("weathercode", 0)
            cond_text, cond_icon = interpret_wmo_code(wcode)
            
            daily = data.get("daily", {})
            forecast = []
            dates = daily.get("time", [])
            max_t = daily.get("temperature_2m_max", [])
            min_t = daily.get("temperature_2m_min", [])
            codes = daily.get("weathercode", [])
            
            for i in range(min(3, len(dates))):
                d_cond, d_icon = interpret_wmo_code(codes[i] if i < len(codes) else 0)
                forecast.append({
                    "date": dates[i],
                    "max_temp": max_t[i] if i < len(max_t) else temp,
                    "min_temp": min_t[i] if i < len(min_t) else temp,
                    "condition": d_cond,
                    "icon": d_icon
                })

            result = {
                "success": True,
                "temperature": temp,
                "condition": cond_text,
                "icon": cond_icon,
                "windspeed_kmh": cw.get("windspeed"),
                "forecast": forecast,
                "source": "Open-Meteo (WMO standard)"
            }
            # Cache for 1 hour
            set_cached_item(cache_key, result, ttl_seconds=3600)
            return result
    except Exception as e:
        logger.warning(f"Open-Meteo weather fetch error: {e}")

    return {
        "success": False,
        "temperature": 26,
        "condition": "Pleasant / Clear",
        "icon": "☀️",
        "forecast": [],
        "note": "Live weather temporarily unavailable; showing typical seasonal baseline."
    }

def interpret_wmo_code(code):
    """Map WMO weather code to friendly human text and emoji."""
    if code == 0:
        return "Clear Sky", "☀️"
    elif code in [1, 2]:
        return "Partly Cloudy", "🌤️"
    elif code == 3:
        return "Overcast", "☁️"
    elif code in [45, 48]:
        return "Misty / Foggy", "🌫️"
    elif code in [51, 53, 55]:
        return "Light Drizzle", "🌦️"
    elif code in [61, 63, 65]:
        return "Rain Showers", "🌧️"
    elif code in [71, 73, 75]:
        return "Snowfall", "❄️"
    elif code in [80, 81, 82]:
        return "Heavy Showers", "⛈️"
    elif code in [95, 96, 99]:
        return "Thunderstorm", "⚡"
    return "Mild & Clear", "🌤️"

# ----------------- DISTANCE & TRANSPORT COMPARISON -----------------
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate Great Circle distance between two points on Earth in km."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def estimate_transport_modes(origin_name, dest_name, origin_coords=None, dest_coords=None):
    """
    Calculate realistic, transparent travel estimates between any two places in India.
    Provides estimated duration, cost ranges, and verified booking links.
    """
    if not origin_coords:
        og = geocode_place(origin_name)
        if og:
            origin_coords = (og["lat"], og["lng"])
        else:
            origin_coords = (28.6139, 77.2090)

    if not dest_coords:
        dg = geocode_place(dest_name)
        if dg:
            dest_coords = (dg["lat"], dg["lng"])
        else:
            dest_coords = (26.9124, 75.7873)

    direct_dist = calculate_haversine_distance(
        origin_coords[0], origin_coords[1],
        dest_coords[0], dest_coords[1]
    )
    road_dist = max(10, int(direct_dist * 1.25))

    modes = []

    # 1. Train Option
    train_speed = 65
    train_hours = round(road_dist / train_speed, 1)
    if train_hours < 2:
        train_duration = f"{int(train_hours * 60)} mins"
    else:
        train_duration = f"{int(train_hours)}h {int((train_hours % 1) * 60)}m"

    sleeper_fare = max(180, int(road_dist * 0.45))
    third_ac_fare = max(550, int(road_dist * 1.15))
    second_ac_fare = max(800, int(road_dist * 1.70))

    modes.append({
        "mode": "Train",
        "icon": "🚆",
        "duration": train_duration,
        "price_range": f"₹{sleeper_fare:,} - ₹{third_ac_fare:,}",
        "classes": f"SL (₹{sleeper_fare}) / 3A (₹{third_ac_fare}) / 2A (₹{second_ac_fare})",
        "recommendation": "Best balance of affordability and comfort. Book 3A or Vande Bharat.",
        "booking_label": "Book on IRCTC",
        "booking_url": "https://www.irctc.co.in/nget/train-search",
        "is_recommended": True if 200 <= road_dist <= 1200 else False
    })

    # 2. Inter-City Bus Option
    bus_speed = 45
    bus_hours = round(road_dist / bus_speed, 1)
    bus_duration = f"{int(bus_hours)}h {int((bus_hours % 1) * 60)}m"
    bus_fare_low = max(250, int(road_dist * 1.1))
    bus_fare_high = max(500, int(road_dist * 1.9))

    modes.append({
        "mode": "Bus",
        "icon": "🚌",
        "duration": bus_duration,
        "price_range": f"₹{bus_fare_low:,} - ₹{bus_fare_high:,}",
        "classes": "AC Sleeper / Volvo Multi-Axle",
        "recommendation": "Ideal for overnight journeys and routes without direct train lines.",
        "booking_label": "Search RedBus",
        "booking_url": f"https://www.redbus.in/bus-tickets/{origin_name.lower()}-to-{dest_name.lower()}",
        "is_recommended": True if road_dist < 450 else False
    })

    # 3. Flight Option (if distance >= 250km)
    if direct_dist >= 250:
        flight_duration = f"{max(1, int(direct_dist / 600))}h {int(((direct_dist / 600) % 1) * 60 + 40)}m"
        flight_fare_low = max(2800, int(3000 + (direct_dist - 250) * 2.2))
        flight_fare_high = int(flight_fare_low * 1.6)
        modes.append({
            "mode": "Flight",
            "icon": "✈️",
            "duration": flight_duration,
            "price_range": f"₹{flight_fare_low:,} - ₹{flight_fare_high:,}",
            "classes": "Economy (IndiGo, Air India, Akasa Air)",
            "recommendation": "Fastest choice for long-distance travel. Book 2-3 weeks in advance.",
            "booking_label": "Compare Flights",
            "booking_url": f"https://www.google.com/travel/flights?q=flights%20from%20{origin_name}%20to%20{dest_name}",
            "is_recommended": True if road_dist > 800 else False
        })

    # 4. Taxi / Private Car
    cab_hours = round(road_dist / 55, 1)
    cab_duration = f"{int(cab_hours)}h {int((cab_hours % 1) * 60)}m"
    cab_fare = int(road_dist * 14) + 400
    modes.append({
        "mode": "Taxi / Car",
        "icon": "🚗",
        "duration": cab_duration,
        "price_range": f"₹{cab_fare:,} - ₹{int(cab_fare * 1.25):,}",
        "classes": "Sedan (Dzire) / SUV (Ertiga/Innova)",
        "recommendation": "Door-to-door flexibility and scenic stops. Great for groups and families.",
        "booking_label": "Check MakeMyTrip Cabs",
        "booking_url": "https://www.makemytrip.com/cabs/",
        "is_recommended": True if road_dist <= 300 else False
    })

    return {
        "origin": origin_name,
        "destination": dest_name,
        "road_distance_km": road_dist,
        "direct_distance_km": direct_dist,
        "modes": modes,
        "disclaimer": "Fares and travel times are transparent estimates based on average Indian transit speeds and class rates. Check provider links for real-time seat availability."
    }
