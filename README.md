# 🇮🇳 PERSONALISED AI TOURIST GUIDE (YĀTRĀ AI)

A complete, professional, production-ready **AI Tourist Guide for travelling across India**.

Users can search for any city, landmark, fort, or temple across India, view real photographs from Wikimedia Commons, check live weather from Open-Meteo, plan realistic budget trips, compare transport options with verified booking links, and consult **Ananya**, an intelligent multi-lingual AI travel assistant supporting English, Hindi (हिंदी), and Marathi (मराठी).

---

## 🌟 Key Features & Capabilities

### 1. Search All Across India (OpenStreetMap + Wikipedia API)
* **Not restricted to hardcoded cities**: Search for any city, town, region, landmark, fort, temple, waterfall, beach, or national park in India (e.g. Pune, Mumbai, Delhi, Jaipur, Goa, Manali, Chakan, Nashik, Hampi, Shaniwar Wada, Dagdusheth Halwai Ganpati Temple, Sinhagad Fort, Ajanta Caves).
* **Live Nominatim Geocoding**: Free, accurate OpenStreetMap geocoding with custom User-Agent, debouncing (350ms), and SQLite caching to strictly respect API usage policies (1 req/sec).
* **Real Photographs & Verified Information**: Real destination photographs from Wikimedia Commons with CC-BY-SA attribution and verified Wikipedia extracts, with attractive high-res fallbacks.
* **Photographic Card Grid**: Cards display destination photo, place name & state, 1-line summary, category, distance from searched city, "View Details", "View on Map", and "Save Place" buttons.

### 2. Rich Destination Details Modal
* **Wikimedia Photo Gallery**: Interactive photo gallery carousel with thumbnail navigation and licensing attribution.
* **Live Weather Integration**: Real-time temperature (°C), conditions icon, and 3-day forecast powered by Open-Meteo (keyless & free).
* **Verified Advisory Notice**: Clear notice distinguishing Archaeological Survey of India (ASI) verified monument rates from variable local fees.
* **Logistics & Culture**: Best visiting season, ideal duration, authentic regional foods, cultural etiquette tips, and external Google Maps directions link.

### 3. Compact Interactive Map of India (Leaflet + OSM)
* **OpenStreetMap Leaflet Map**: Free, open map tiles with custom category-coded pins (Crimson Maroon for Heritage, Warm Saffron for Spiritual, Ocean Blue for Beaches, Forest Green for Mountains).
* **Two-Way Synchronization**:
  * Clicking "Map" on any card centers the map, zooms in, and opens its interactive popup.
  * Clicking any map pin highlights and smoothly scrolls to the corresponding card in the grid.
* **Map Controls**: Category filter pills and a "Center Map" bounds fitting button.

### 4. Simple Budget-Based Trip Planner
* **Input Parameters**: Starting city, destination city (or "Suggest Destinations for My Budget"), total budget in INR, number of travelers, departure and return dates, travel pace (Relaxed, Balanced, Packed), comfort tier, and travel interests.
* **Date Validation**: Ensures return date is on or after departure date, with automatic trip duration calculation.
* **Dynamic Day-by-Day Itinerary**: Generates a complete schedule divided into Morning, Afternoon, and Evening slots with realistic pacing, meal suggestions, and ASI entry fees.
* **Transparent Travel Math**: Itemized breakdown: Stay (45%), Food (25%), Transit (15%), Sightseeing (10%), Buffer (5%), with per-person and daily calculations.
* **Persistence & Printable Export**: Save itineraries to SQLite database (`/api/trips/save`), access under Saved Places, and generate clean print/PDF exports (`/trip/print/<trip_id>`).

### 5. Inter-City Transport Comparison Engine
* **Dynamic Route Calculator**: Compare travel between ANY origin and destination in India.
* **Multi-Modal Comparison**:
  * **Train**: Sleeper, 3AC, 2AC, and Vande Bharat estimates with direct booking link to [IRCTC](https://www.irctc.co.in/nget/train-search).
  * **Bus**: AC Sleeper and Volvo Multi-Axle duration and fare brackets with link to [RedBus](https://www.redbus.in).
  * **Flight**: Economy flight estimates for routes > 250 km with link to [Google Flights](https://www.google.com/travel/flights).
  * **Taxi / Car**: Realistic road distance calculation (Detour factor 1.25) at ₹14/km + tolls with link to [MakeMyTrip Cabs](https://www.makemytrip.com/cabs/).

### 6. "Ananya" — Multi-Lingual AI Travel Assistant
* **Floating Chat Widget**: Accessible from every page via the bottom-right launcher button, plus navigation bar trigger.
* **Multi-Lingual Support**: Fluent in English, Hindi (हिंदी), and Marathi (मराठी) with automatic language detection and manual language pills.
* **Understands Natural Questions**:
  * *"I have ₹5,000 and two days. Suggest a trip from Pune."* &rarr; Tailor-made getaways to Sinhagad Fort, Panshet Dam, and Lonavala with cost breakdown under ₹5,000.
  * *"Which historical places can I visit in Jaipur?"* &rarr; Amber Fort, Hawa Mahal, City Palace, Jantar Mantar, Nahargarh Fort with ASI tickets.
  * *"Plan a three-day family trip to Goa."* &rarr; Family-friendly beaches (Candolim/Morjim), Fort Aguada, Old Goa UNESCO churches, Spice Plantation, and Mandovi cruise.
  * *"What should I carry for a monsoon trip?"* &rarr; Comprehensive monsoon packing list (quick-dry layers, vibram-grip footwear, waterproof pouches, umbrella).
  * *"पुण्यातून दोन दिवसांसाठी कुठे फिरायला जाऊ?"* (Marathi) &rarr; Authentic Marathi response with weekend options.
  * *"जयपुर में कौन से ऐतिहासिक स्थल देखने लायक हैं?"* (Hindi) &rarr; Authentic Hindi response with heritage monuments.
* **Interactive Action Buttons**: Bot messages include clickable buttons (`[Plan Trip]`, `[View on Map]`, `[Explore Destination]`) that directly control the website!
* **Gemini API Integration**: Uses Google Gemini API if `GEMINI_API_KEY` is configured in `.env`, with automatic, zero-error fallback to the rich built-in knowledge engine.

### 7. Practical Traveler Handbook & Packing Checklist
* **Handbook**: Essential tabs covering e-Visas, UPI for foreigners (*UPI One World*), Indian SIM cards (Airtel/Jio), cultural etiquette, and emergency dispatch (**112**, **1091**, **1363**).
* **Interactive Checklist**: Categorized packing list with progress bar, custom item addition, and browser `localStorage` persistence.

---

## 🛠️ Architecture & Tech Stack

* **Backend**: Python 3.11+, Flask 3.1, SQLite3, Requests, Gunicorn, Python-Dotenv.
* **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Design System with editorial green `#163A2E`, terracotta `#C2633E`, and warm gold `#B8860B`), Vanilla JavaScript (ES6+ modular architecture).
* **Mapping**: Leaflet.js with OpenStreetMap Carto tiles.
* **Geocoding & Data**: OpenStreetMap Nominatim API, Wikipedia GeoSearch & Search APIs, Wikimedia Commons API.
* **Weather**: Open-Meteo Keyless API.
* **Security**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, parameterised SQL queries, input sanitisation.

---

## 🚀 Local Setup & Running Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/personalised-ai-tourist-guide.git
cd personalised-ai-tourist-guide
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (Optional)
```bash
# Copy example configuration
cp .env.example .env
```
*Note: The application runs 100% standalone out of the box with zero required API keys. If you wish to enable Google Gemini AI, set `GEMINI_API_KEY=your_key` in `.env`.*

### 5. Run the application
```bash
# Development mode
python app.py

# Production WSGI server (Gunicorn)
gunicorn app:app --bind 127.0.0.1:5000
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 🧪 Testing

The project includes an automated test suite with 100% passing tests:

### Run unit & functional tests (26 automated test cases)
```bash
python test_app.py
```
Verifies:
* Database seeding and destination data integrity
* Search across India (Pune, Delhi, Goa, Chakan, Shaniwar Wada)
* Empty search and fallback handling
* Destination details and Wikimedia photo gallery retrieval
* Open-Meteo live weather API
* Transport route calculations
* Budget calculations and date validation
* Chatbot questions (Pune ₹5,000 budget, Jaipur history, Goa family, monsoon packing, Hindi, Marathi)
* Itinerary saving, retrieval, printable view, and deletion
* Production security headers

### Run live server integration tests (15 live HTTP checks)
```bash
# Ensure server is running in a separate terminal: python app.py
python test_live_server.py
```

---

## ☁️ Free Deployment Guide (Render)

The project includes `Procfile` and `render.yaml` for one-click deployment on Render:

1. Push your repository to **GitHub**.
2. Log into [Render.com](https://render.com) and click **New + &rarr; Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Under **Environment Variables**, add:
   - `FLASK_DEBUG` = `0`
   - `SECRET_KEY` = *(click Generate or enter a secure string)*
   - `PYTHON_VERSION` = `3.11.9`
   - `GEMINI_API_KEY` = *(optional)*
6. Click **Create Web Service**. Your app will deploy live with free SSL!

---

## 📜 Public API Usage & Attribution

* **OpenStreetMap & Nominatim**: Map tiles & geocoding &copy; [OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Usage follows the Nominatim Acceptable Use Policy with custom identification headers, rate limiting (1 req/sec), and persistent local caching.
* **Wikimedia Commons / Wikipedia**: Destination images and extracts provided under Creative Commons Attribution-ShareAlike (CC-BY-SA).
* **Open-Meteo**: Weather forecasts provided under the CC-BY 4.0 license using WMO weather codes.
* **Indian Railways / ASI**: Train routes and monument fees are reference averages based on published Indian Railway and Archaeological Survey of India schedules.
