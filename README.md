# 🇮🇳 PERSONALISED AI TOURIST GUIDE (YĀTRĀ AI)

A complete, production-ready, authentic web application designed to help travelers discover destinations across India, explore verified attractions and real ticket pricing, compare transport routes, plan realistic trips by budget, generate custom daily itineraries, and consult an intelligent travel assistant.

Built as an accessible, cost-effective full-stack project utilizing free, standard libraries and open data with zero required commercial dependencies or paid hosting requirements.

---

## 🌟 Highlights & Core Features

1. **Editorial Travel Aesthetic**:
   - Designed with an editorial travel magazine visual direction (deep forest green accents `#163A2E`, warm cream and parchment tones `#FAF8F5`, `#F4EFE6`, and warm spice accents `#C2633E`).
   - Clean card architecture, responsive grids, and typography pairing `Playfair Display` with `Plus Jakarta Sans`.
   - Real, curated high-resolution photography without generic AI-generated stock fillers.

2. **Destination Discovery Across India**:
   - Spanning North, South, West, East, and Northeast India (Jaipur, Varanasi, Munnar, Goa, Agra, Leh Ladakh, Udaipur, Rishikesh, Hampi, Darjeeling, Kochi, Shillong, Amritsar, Pondicherry, Kaziranga).
   - Filterable by geographic region, travel category (Heritage, Spiritual, Hills, Beaches, Wildlife, Adventure), season, and daily budget tier.
   - Comprehensive attraction details: Archaeological Survey of India (ASI) ticket fees for domestic vs. international visitors, timings, insider tips, and cultural etiquette.

3. **Interactive Map of India (Leaflet + OpenStreetMap)**:
   - Full interactive map powered by Leaflet and OpenStreetMap tiles (100% free, no credit card or Google Maps API key required).
   - Custom color-coded pins categorized by destination style with rich preview popups.
   - Live category filter pills on the map.

4. **Personalized Trip Planner & Day-by-Day Itinerary Generator**:
   - Select departure city, target destination, trip length (1 to 7 days), traveler profile (Solo, Couple, Family, Friends, Senior), budget tier, and travel pace (Relaxed, Balanced, Packed).
   - Dynamically constructs a structured schedule broken down into **Morning**, **Afternoon**, and **Evening** slots with authentic dining recommendations, monument logistics, and daily cost estimates.

5. **Financial Clarity & Dynamic Budget Calculator**:
   - Live expense calculator for travelers, trip length, and tier.
   - Transparent visual breakdown: Accommodation (45%), Food (25%), Local Transit (15%), Sightseeing (10%), Buffer (5%).
   - Actionable money-saving travel advice (IRCTC advance booking, metro smartcards, ASI e-ticket discounts).

6. **Inter-City Transport Comparison Engine**:
   - Compare Flights, High-Speed Trains (Vande Bharat, Shatabdi, Gatimaan), AC Volvo Buses, and Expressway Cabs for major Indian corridors.
   - Duration, estimated fare ranges in INR (₹), and realistic booking guidance.

7. **"Ananya" — Intelligent AI Travel Assistant**:
   - Chatbot with deep domain expertise in Indian travel:
     - IRCTC train reservations, Tatkal booking rules, and Foreign Tourist Quota.
     - UPI digital payments for foreigners (*UPI One World*).
     - Food hygiene, avoiding Delhi belly, and water safety.
     - Temple dress codes, footwear customs, and cultural norms.
     - Solo female travel safety, verified night transit, and emergency numbers (**112**, **1091**, **1363**).
     - Common tourist scams and prevention.
   - Works 100% standalone out of the box with zero required external API keys, while seamlessly supporting optional Google Gemini API keys via `.env`.

8. **Practical Traveler Handbook**:
   - In-depth verified guides for Indian e-Visa, UPI and ATM fees, SIM cards (Airtel/Jio) and eSIMs, cultural etiquette, and emergency dispatch.

9. **Interactive Packing Checklist**:
   - Categorized by Documents, Modest & Seasonal Clothing, Health & First Aid, and Electronics.
   - Checkbox state persists in `localStorage`.
   - Real-time progress bar, custom item addition, and print-ready format.

10. **Saved Trips & PDF/Printable Export**:
    - Persists generated itineraries in SQLite database and provides a dedicated print/PDF stylesheet (`/trip/print/<trip_id>`).

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask, SQLite3, Requests, Python-Dotenv, Gunicorn.
- **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Design System), Vanilla JavaScript (ES6+ modular scripts), Leaflet 1.9.4.
- **Map Tiles**: OpenStreetMap.
- **Data Persistence**: SQLite (`travel_guide.db`) automatically seeded on initial launch.
- **Deployment**: Render / Heroku ready with `Procfile` and `render.yaml`.

---

## 📁 Project Directory Structure

```
├── app.py                      # Main Flask application and RESTful API endpoints
├── config.py                   # Environment settings and application configuration
├── database.py                 # SQLite database schema, seeding, and queries
├── travel_data.py              # Rich, verified Indian travel dataset (destinations, sights, routes)
├── ai_engine.py                # AI itinerary generator and Ananya chatbot engine
├── requirements.txt            # Python dependencies (Flask, Gunicorn, Requests, etc.)
├── Procfile                    # Cloud deployment process command
├── render.yaml                 # Render cloud infrastructure blueprint
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete documentation
├── static/
│   ├── css/
│   │   ├── style.css           # Editorial travel magazine design system & responsive layout
│   │   └── print.css           # Paper & PDF print-optimized stylesheet
│   └── js/
│       ├── app.js              # UI coordinator, search filter, active navigation, modal
│       ├── map.js              # Leaflet.js interactive map & custom markers
│       ├── planner.js          # Trip planner & dynamic daily itinerary generator
│       ├── budget.js           # Budget calculator & transport comparator
│       ├── chatbot.js          # Ananya AI Travel Assistant
│       └── checklist.js        # Interactive packing checklist with browser persistence
└── templates/
    ├── base.html               # Base layout template with header, footer, toast & modal
    ├── index.html              # Main interactive single-page portal
    ├── print_trip.html         # Dedicated clean printable & PDF export view
    ├── 404.html                # Custom 404 page
    └── 500.html                # Custom 500 page
```

---

## 🚀 Local Development Setup

### 1. Clone or Open the Workspace
```bash
git clone <your-repo-url>
cd "PME project"
```

### 2. (Optional) Create & Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access in Your Browser
Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

*The SQLite database (`travel_guide.db`) will automatically initialize and populate all destinations and attractions on first launch.*

---

## 🌐 Free Cloud Deployment on Render

1. Push your repository to **GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Personalized AI Tourist Guide India"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

2. Go to [Render.com](https://render.com) and create a free account.
3. Click **New +** &rarr; **Web Service**.
4. Connect your GitHub repository.
5. Render will automatically detect the Python environment:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
6. Click **Deploy Web Service**. Your app will be live with a free HTTPS URL in minutes!

---

## 🔒 Security & Best Practices

- **Zero SQL Injection**: All database operations use SQLite parameterized queries (`?` placeholders).
- **Security Headers**: Standard headers added on every response (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection`, `Referrer-Policy`).
- **Input Sanitization**: User inputs escaped before DOM insertion.
- **No Hardcoded Secrets**: Secrets and optional API keys loaded securely via environment variables.

---

## 📜 License
This project is open-source and free for educational, student, and personal travel use.
