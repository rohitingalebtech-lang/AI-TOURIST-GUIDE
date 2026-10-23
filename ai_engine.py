"""
ai_engine.py
Smart travel recommendation engine and travel chatbot ("Ananya") for Personalized AI Tourist Guide India.
Operates completely standalone with rich domain knowledge, and optionally connects to Gemini API if configured.
"""

import os
import re
import random
from database import get_destination_by_id, log_chat

# KNOWLEDGE BASE FOR CHATBOT INTENTS
KNOWLEDGE_RESPONSES = {
    "irctc_trains": {
        "keywords": ["irctc", "train", "rail", "tatkal", "berth", "sleeper", "vande bharat", "shatabdi", "train ticket", "railway"],
        "reply": """### 🚆 How to Book Trains & Navigate Indian Railways

1. **Official Booking Website**: Book exclusively on the official portal [irctc.co.in](https://www.irctc.co.in) or mobile app *IRCTC Rail Connect*. Third-party apps like ConfirmTkt and MakeMyTrip also offer smooth interfaces.
2. **Booking Window (ARP)**: General advance booking opens **120 days** before departure at 8:00 AM IST. For popular routes (like Delhi to Varanasi or Mumbai to Goa), book as early as possible.
3. **Tatkal Quota (Last-minute booking)**: Opens one day prior to journey at **10:00 AM IST for AC classes** and **11:00 AM IST for Non-AC (Sleeper)**.
4. **Foreign Tourist Quota (FTQ)**: International passport holders can book designated tourist quota seats on major trains via IRCTC online or at International Tourist Bureaus in major stations (New Delhi, CSMT Mumbai).
5. **Recommended Classes**:
   - **Vande Bharat & Shatabdi**: AC Chair Car (CC) or Executive Chair Car (EC)—clean, modern, meals included.
   - **Overnight Trains**: **2nd AC (2A)** or **3rd AC (3A)** offer the best balance of comfort, air conditioning, and bed linen provided.
6. **Live Running Status**: Download the free app **'Where is my Train'** to track train location and platform numbers offline using cell towers."""
    },
    "upi_payments": {
        "keywords": ["upi", "cash", "payment", "credit card", "atm", "money", "currency", "cheq", "rupee", "forex"],
        "reply": """### 💳 Money & UPI Payments in India

1. **UPI for Foreign Tourists**: International travelers can now access India's Unified Payments Interface via **'UPI One World'** prepaid wallets. You can sign up at designated counters at Delhi (DEL), Mumbai (BOM), and Bengaluru (BLR) international airports, or through RBI-authorized apps like *Cheq Global*.
2. **Where UPI Works**: Everywhere! From five-star dining to roadside coconut and chai stalls, almost every merchant displays a QR code scanner.
3. **Credit & Debit Cards**: International Visa and Mastercard work smoothly at hotels, sit-down restaurants, supermarket chains, and monument ticket portals. American Express is accepted only at select luxury hotels.
4. **Carrying Cash**: Keep ₹2,000 to ₹3,000 in physical cash (₹100, ₹200 notes) for rural temple towns, auto rickshaws, and places with intermittent network connectivity.
5. **ATM Advice**: Use ATMs attached directly to major national bank branches (SBI, HDFC, ICICI, Axis). Always select **'Charge in INR without conversion'** at the ATM screen to avoid hefty dynamic currency conversion (DCC) markups."""
    },
    "street_food_safety": {
        "keywords": ["delhi belly", "food", "street food", "water", "hygiene", "stomach", "sick", "eat", "safe to eat"],
        "reply": """### 🍲 Savoring Indian Street Food Safely

1. **Golden Rule: Eat Fresh & Hot**: Choose street stalls that have long, bustling queues of local families. High turnover means the ingredients are freshly cooked on high heat right in front of you.
2. **Drinking Water**: Strictly drink sealed bottled water from reliable brands (*Bisleri, Kinley, Aquafina*) or water filtered through reverse osmosis (RO). Never drink tap water. Check that the plastic seal ring is unbroken.
3. **Avoid Raw Cut Fruits & Unpeeled Salads**: Skip pre-sliced watermelon, papaya, and cucumbers kept out in open carts. Stick to fruits you can peel yourself (bananas, oranges, mangoes).
4. **Ice Cubes**: Avoid ice in roadside fruit juices unless you are at an established, hygienic indoor cafe.
5. **Yogurt / Curd (Dahi)**: Fresh curd, lassi, and raita are probiotic powerhouses and remarkably soothing for your digestive system in warm weather.
6. **Emergency Kit**: Always keep ORS (Oral Rehydration Salts) hydration sachets and digestive tablets in your daypack."""
    },
    "temple_culture": {
        "keywords": ["dress", "temple", "clothes", "modest", "shoes", "etiquette", "culture", "mosque", "gurdwara"],
        "reply": """### 🛕 Cultural Etiquette & Sacred Sites Dress Code

1. **Temple & Mosque Attire**: Wear loose, respectful clothing that covers your shoulders, chest, and knees. In South Indian temples (like Madurai Meenakshi or Padmanabhaswamy), traditional dhotis or cotton trousers are often mandatory for inner sanctums.
2. **Footwear Protocol**: All footwear (shoes, sandals, socks) must be removed before entering temples, mosques, and gurdwaras. Reputable temples have free or ₹5 monitored shoe storage counters (*Joota Ghar*).
3. **Head Covering**: In Sikh Gurdwaras (such as the Golden Temple in Amritsar) and certain mosques, head covering is mandatory for both men and women. Clean scarves or cloth bandanas are provided free at the gates.
4. **Right Hand Custom**: Offer donations, receive *prasad* (blessed food offerings), and shake hands using your right hand.
5. **Photography Rules**: Always check signage before taking photos inside sanctum sanctorums. When in doubt, ask the temple authorities or priests politely."""
    },
    "solo_female_safety": {
        "keywords": ["woman", "women", "female", "solo", "safety", "safe", "alone", "helpline", "night"],
        "reply": """### 🛡️ Safety Tips for Solo & Female Travelers

1. **Emergency Numbers**:
   - **112**: All-India Unified Emergency Helpline (Police, Ambulance, Fire)
   - **1091**: 24x7 Women's Helpline
   - **1363**: Ministry of Tourism Multi-lingual Helpline (English, French, German, Spanish, Hindi)
2. **Transportation at Night**:
   - Use verified ride-hailing apps like **Uber** or **Ola** with GPS tracking and driver verification enabled. Share your live ride tracking link with a trusted contact.
   - For trains, reserve **2nd AC (2A)** or **3rd AC (3A)** sleeper coaches which are monitored by Railway Protection Force (RPF) personnel.
   - In Delhi and Bengaluru, the first coach of the metro train is reserved exclusively for women.
3. **Accommodations**: Choose verified boutique heritage homestays, reputable 4-star/5-star hotels, or trusted hostel chains (*Zostel, The Hosteller*) with high female guest ratings.
4. **Dealing with Staring**: Direct eye contact can sometimes be misinterpreted. Wearing sunglasses helps deflect unwanted attention. A firm, polite **'Nahin, shukriya'** (No, thank you) or ignoring persistent touts is effective."""
    },
    "sim_card": {
        "keywords": ["sim", "esim", "internet", "airtel", "jio", "phone", "network", "data", "roaming"],
        "reply": """### 📱 SIM Cards, eSIM & Internet Connectivity

1. **Best Network Providers**: **Airtel** and **Jio** have the strongest 4G/5G coverage across India, including remote hill stations and heritage hubs.
2. **Instant eSIM (Before Landing)**: You can buy digital travel eSIMs from services like *Airalo* or *Nomad* before arrival. They activate upon touchdown without paperwork.
3. **Airport Kiosks**: Upon landing at Delhi (IGI), Mumbai (CSMT/BOM), or Bengaluru (BLR), visit the authorized Airtel or Jio kiosks in the baggage/arrival hall. You will need:
   - Your original passport
   - A copy of your Indian tourist visa
   - One passport-sized physical photograph
4. **Cost & Data Allowance**: Standard 28-day prepaid packs cost only **₹300 - ₹450 (~$4-5 USD)** and include unlimited local calls plus 1.5GB to 2GB high-speed 5G data per day."""
    },
    "scam_awareness": {
        "keywords": ["scam", "touts", "fake", "taxi", "commission", "cheat", "caution", "avoid"],
        "reply": """### ⚠️ Common Tourist Scams & How to Avoid Them

1. **'Your Hotel is Burned / Closed' Scam**: When arriving at Delhi Railway Station or Airport, rogue taxi drivers may tell you your booked hotel is closed due to a festival, fire, or protest, offering to drive you to a 'Government Tourist Office' instead. **Never believe this.** Call your hotel directly.
2. **Fake Government Tourist Offices**: Unlicensed travel agents along Connaught Place or Paharganj claim to be official Ministry of Tourism counters and sell overpriced package tours. The official government office is at Janpath, New Delhi.
3. **The 'Gem Export' Scam**: Particularly in Jaipur and Agra, strangers may invite you to buy gemstones or carpets to mail overseas for profit. This is a complete hoax.
4. **Pushy Temple Touts & Sadhus**: Individuals offering peacock feathers, wrist threads (*Mauli*), or blessings may demand exorbitant donations. Offer ₹10-20 politely or say a clear *'No, thank you'*.
5. **Always Use App Taxis or Prepaid Booths**: At airports and major train stations, book through Uber/Ola or use the police-regulated Prepaid Taxi booth inside the terminal."""
    },
    "ladakh_planning": {
        "keywords": ["ladakh", "leh", "pangong", "nubra", "khardung", "altitude", "ams"],
        "reply": """### 🏔️ Essential Planning for Leh Ladakh

1. **Mandatory Acclimatization**: Leh is at 3,500 meters (11,500 ft). You **MUST spend your first 48 hours resting** in Leh town without doing any strenuous climbs. Drink plenty of water and ginger-lemon honey tea.
2. **Inner Line Permits (ILP)**: Required for Pangong Tso, Nubra Valley, Khardung La, and Tso Moriri. Apply online at *lahdclehpermit.in* or have your hotel/local agency arrange it.
3. **Best Season**: June to September. Mountain passes (Manali-Leh and Srinagar-Leh) are open, and daytime temperatures range from 15°C to 25°C.
4. **What to Pack**: Heavy windproof jacket, thermal innerwear, polarized UV sunglasses (snow glare is intense), high-SPF sunscreen, and adequate cash in INR (ATMs are rare outside Leh)."""
    },
    "golden_triangle": {
        "keywords": ["golden triangle", "delhi agra jaipur", "first time", "itinerary", "route"],
        "reply": """### 🗺️ The Iconic Golden Triangle: Delhi – Agra – Jaipur

The Golden Triangle is India's most popular introductory route, covering approximately 720 km of historic heritage:
- **Recommended Duration**: 6 to 7 Days
- **Route Breakdown**:
  - **Days 1-2 (Delhi)**: Humayun's Tomb, Qutub Minar, Old Delhi Chandni Chowk street food, India Gate.
  - **Day 3 (Agra)**: Take the Gatimaan Express (100 mins); visit Agra Fort and sunset at Mehtab Bagh.
  - **Day 4 (Agra to Jaipur)**: Sunrise at the Taj Mahal. Travel to Jaipur via Fatehpur Sikri and Chand Baori stepwell.
  - **Days 5-6 (Jaipur)**: Amber Fort, Hawa Mahal, City Palace, Nahargarh sunset, Johari Bazaar shopping.
- **Best Travel Mode**: High-speed trains (Gatimaan, Vande Bharat) and expressways make this route smooth and stress-free."""
    }
}

def generate_custom_itinerary(dest_id, starting_city, duration_days, traveler_type, budget_tier, pace, interests=None):
    """
    Dynamically generates a detailed, realistic day-by-day travel itinerary
    customized by user profile, duration, budget, and travel speed.
    """
    dest = get_destination_by_id(dest_id)
    if not dest:
        return None

    duration = max(1, min(int(duration_days), 7))
    attractions = dest.get("attractions", [])
    highlights = dest.get("highlights", [])
    foods = dest.get("famous_foods", [])
    culture_tips = dest.get("culture_tips", [])
    
    # Cost multiplier based on budget tier
    tier_mult = {"budget": 1.0, "moderate": 1.8, "luxury": 3.8}.get(budget_tier.lower(), 1.5)
    base_cost = dest.get("avg_daily_budget", 2500)
    est_daily_cost = int(base_cost * tier_mult)

    days_plan = []

    # Activity scheduling templates per destination
    for day_num in range(1, duration + 1):
        day_theme = f"Exploration & Culture"
        if day_num == 1:
            day_theme = f"Arrival in {dest['name']}, Heritage Landmarks & Golden Hour"
        elif day_num == 2:
            day_theme = f"Architectural Wonders, Artisan Bazaars & Local Flavors"
        elif day_num == 3:
            day_theme = f"Hidden Sanctuaries, Panoramic Vistas & Sunset Spectacle"
        elif day_num == 4:
            day_theme = f"Immersive Day Trip & Nature Trails"
        else:
            day_theme = f"Slow Travel, Traditional Crafts & Farewell Feast"

        # Select morning, afternoon, evening highlights
        attr_idx = (day_num - 1) % max(1, len(attractions))
        main_attr = attractions[attr_idx] if attractions else None

        food_sample = foods[(day_num - 1) % max(1, len(foods))] if foods else {"dish": "Local Regional Thali", "desc": "Authentic regional lunch served on a traditional platter"}
        
        # Build morning section
        if day_num == 1:
            morning = {
                "time": "08:30 AM - 11:30 AM",
                "title": f"Arrival & Check-in at your hotel in {dest['name']}",
                "detail": f"Arrive from {starting_city}, settle into your accommodations, and enjoy fresh regional tea or coffee. Review maps and set out with your essentials.",
                "transport": "Prepaid airport/station taxi or booked cab to hotel",
                "est_cost": f"₹{int(400 * tier_mult)}"
            }
        else:
            morning_attr_name = main_attr["name"] if main_attr else highlights[(day_num * 2 - 2) % len(highlights)]
            morning = {
                "time": "07:30 AM - 11:00 AM",
                "title": f"Visit {morning_attr_name}",
                "detail": main_attr["description"] if main_attr else f"Explore {morning_attr_name} in the gentle morning light before midday crowds peak.",
                "tip": main_attr.get("insider_tip", "Reach early for clear photography without long queues."),
                "transport": "Auto-rickshaw or local cab (approx 15-20 mins)",
                "est_cost": f"₹{main_attr['entry_fee_inr'] if main_attr else 100} entry"
            }

        # Build afternoon section
        sec_attr_name = highlights[(day_num * 2 - 1) % len(highlights)] if highlights else "City Heritage Center"
        afternoon = {
            "time": "12:30 PM - 03:30 PM",
            "title": f"Authentic Lunch & Discovering {sec_attr_name}",
            "food_highlight": f"Must-try lunch: {food_sample['dish']} — {food_sample['desc']}",
            "detail": f"Dine at a renowned local eatery. Follow lunch with an exploration of {sec_attr_name}, engaging with local craftsmen and cultural displays.",
            "pace_note": "During hotter months, spend this window in air-conditioned museums or shaded courtyard cafes." if pace != "packed" else "Fast-paced walk through nearby historic quarters."
        }

        # Build evening section
        evening_spots = [
            f"Sunset panorama over {dest['name']}'s iconic skyline",
            f"Vibrant stroll through centuries-old bazaars and souvenir markets",
            f"Traditional folk music performance and rooftop dinner overlooking illuminated monuments",
            f"Relaxed riverside/lakeside promenade stroll under the stars"
        ]
        evening_choice = evening_spots[(day_num - 1) % len(evening_spots)]

        evening = {
            "time": "05:00 PM - 09:00 PM",
            "title": evening_choice,
            "detail": f"Experience the magic of twilight in {dest['name']}. Savor street treats, absorb the acoustic buzz, and conclude with a leisurely dinner.",
            "tip": culture_tips[(day_num - 1) % len(culture_tips)] if culture_tips else "Respect local photography norms and keep change handy for street vendors."
        }

        days_plan.append({
            "day": day_num,
            "theme": day_theme,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "estimated_daily_budget": f"₹{est_daily_cost:,}"
        })

    total_est_cost = est_daily_cost * duration

    itinerary_payload = {
        "destination": dest,
        "parameters": {
            "starting_city": starting_city,
            "duration_days": duration,
            "traveler_type": traveler_type,
            "budget_tier": budget_tier,
            "pace": pace
        },
        "days": days_plan,
        "summary": {
            "total_estimated_budget_inr": f"₹{total_est_cost:,}",
            "per_person_per_day": f"₹{est_daily_cost:,}",
            "budget_breakdown": {
                "accommodation": int(total_est_cost * 0.45),
                "food_and_dining": int(total_est_cost * 0.25),
                "transport_and_cabs": int(total_est_cost * 0.15),
                "monument_tickets_activities": int(total_est_cost * 0.10),
                "buffer_and_tips": int(total_est_cost * 0.05)
            },
            "packing_advisory": "Carry comfortable walking shoes, universal power bank, cotton layers, and a modest scarf for shrines.",
            "emergency_numbers": "National Emergency: 112 | Tourist Helpline: 1363"
        }
    }

    return itinerary_payload

def ask_travel_ai(query, context=None):
    """
    Answers user travel questions with intelligent intent matching and comprehensive knowledge.
    Optionally calls Google Gemini API if GEMINI_API_KEY is present in the environment.
    """
    clean_query = query.strip().lower()

    # Check for Gemini API key first if configured
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            import google.genai as genai
            client = genai.Client(api_key=gemini_key)
            prompt = f"""You are Ananya, an expert, warm, and highly knowledgeable Indian Travel Guide assistant.
The user is asking: "{query}"
Context about their trip: {context if context else 'None specified'}.
Provide a clear, helpful, authentic, and culturally accurate answer in Markdown format.
Include practical travel tips, estimated prices in Indian Rupees (INR ₹) where relevant, safety advice, and respectful etiquette. Avoid robotic fluff."""
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            if response and response.text:
                log_chat(query, response.text, "gemini_api")
                return response.text
        except Exception as e:
            # Silently fallback to built-in knowledge engine
            pass

    # Built-in Smart Domain Matching Engine
    for intent_name, data in KNOWLEDGE_RESPONSES.items():
        for kw in data["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', clean_query):
                log_chat(query, data["reply"], intent_name)
                return data["reply"]

    # Destination-specific matching
    destinations = ["jaipur", "varanasi", "munnar", "goa", "agra", "ladakh", "udaipur", "rishikesh", "hampi", "darjeeling", "kochi", "shillong", "amritsar", "pondicherry", "kaziranga"]
    for d in destinations:
        if d in clean_query:
            dest_obj = get_destination_by_id(d)
            if dest_obj:
                reply = f"""### 🌟 Travel Insights for {dest_obj['name']} ({dest_obj['state']})

- **Category**: {dest_obj['category']}
- **Best Time to Visit**: {dest_obj['best_season']}
- **Ideal Duration**: {dest_obj['ideal_days']}
- **Average Daily Budget**: Approx ₹{dest_obj['avg_daily_budget']:,} per person

**Key Highlights to Experience**:
{chr(10).join(['* ' + h for h in dest_obj['highlights']])}

**Must-Try Local Delicacies**:
{chr(10).join(['* **' + f['dish'] + '**: ' + f['desc'] for f in dest_obj['famous_foods']])}

**Local Etiquette & Pro Tips**:
{chr(10).join(['* ' + tip for tip in dest_obj['culture_tips']])}

**How to Reach**:
- **By Air**: {dest_obj['how_to_reach'].get('air', 'Check nearest domestic airport')}
- **By Train**: {dest_obj['how_to_reach'].get('rail', 'Check Indian Railways connections')}
- **By Road**: {dest_obj['how_to_reach'].get('road', 'Accessible via National Highways')}"""
                log_chat(query, reply, f"dest_{d}")
                return reply

    # Default friendly, comprehensive guidance
    default_reply = """### Namaste! I am Ananya, your AI Travel Guide for India.

I can help you with comprehensive, real-world advice on:
- **Train Travel & IRCTC**: How to book tickets, Vande Bharat routes, Tatkal, and Foreign Tourist Quota.
- **Payments & UPI**: Using UPI One World, credit cards, ATMs, and cash tips.
- **Health & Street Food**: Avoiding Delhi belly, drinking water safety, and authentic dish recommendations.
- **Cultural Etiquette**: Temple dress codes, footwear rules, and customs.
- **Solo & Female Travel Safety**: Verified transport, helpline numbers (**112**, **1091**), and secure stays.
- **Packing & Essentials**: What to pack for tropical, desert, and Himalayan destinations.
- **Destination Guides**: In-depth guidance for Jaipur, Varanasi, Munnar, Goa, Agra, Ladakh, Hampi, and more!

*Feel free to ask a specific question, such as "How do I book trains on IRCTC?", "What should I wear to South Indian temples?", or "Best 3-day itinerary for Jaipur?"*"""

    log_chat(query, default_reply, "fallback")
    return default_reply
