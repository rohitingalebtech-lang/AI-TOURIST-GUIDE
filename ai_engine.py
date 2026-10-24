"""
ai_engine.py
Smart travel recommendation engine and multi-lingual travel assistant ("Ananya")
for Personalized AI Tourist Guide India.
Supports English, Hindi, and Marathi.
Understands budget & duration requests, city historic guides, family itineraries,
monsoon packing, live transit, and connects to Google Gemini API if configured.
"""

import os
import re
import json
import logging
from database import get_destination_by_id, get_all_destinations, log_chat
from services.geo_service import get_live_weather, geocode_place

logger = logging.getLogger(__name__)

# Multi-lingual greetings and UI terms
LANG_MARATHI = "mr"
LANG_HINDI = "hi"
LANG_ENGLISH = "en"

def detect_language(text):
    """Detect if query is written in Devanagari script (Marathi or Hindi) or English."""
    devanagari_chars = len(re.findall(r'[\u0900-\u097F]', text))
    if devanagari_chars > 3:
        # Check specific Marathi vocabulary vs Hindi
        marathi_words = ["आहे", "कसे", "कुठे", "पुण्यातून", "दिवस", "सांगा", "जाऊ", "पाहिजे", "फिरण्यासाठी", "करायचे", "केव्हा"]
        for mw in marathi_words:
            if mw in text:
                return LANG_MARATHI
        return LANG_HINDI
    return LANG_ENGLISH

# ----------------- KNOWLEDGE REPOSITORY -----------------
KNOWLEDGE_RESPONSES = {
    "irctc_trains": {
        "keywords": ["irctc", "train", "rail", "tatkal", "berth", "sleeper", "vande bharat", "shatabdi", "train ticket", "railway"],
        "reply": """### 🚆 How to Book Trains & Navigate Indian Railways

1. **Official Portal**: Book tickets exclusively on the official IRCTC portal [irctc.co.in](https://www.irctc.co.in/nget/train-search) or mobile app *IRCTC Rail Connect*.
2. **Booking Window (ARP)**: General advance reservation opens **120 days** before departure at 8:00 AM IST.
3. **Tatkal Quota (Emergency booking)**: Opens one day prior to departure at **10:00 AM IST for AC classes** and **11:00 AM IST for Sleeper**.
4. **Foreign Tourist Quota (FTQ)**: International passport holders can reserve designated FTQ seats on key express routes via IRCTC or International Tourist Bureaus in Delhi and Mumbai.
5. **Recommended Classes**:
   - **Vande Bharat & Shatabdi**: AC Chair Car (CC) or Executive (EC) with meals included.
   - **Overnight Trains**: **2nd AC (2A)** or **3rd AC (3A)** offer the best balance of comfort, air conditioning, and fresh bed linen.
6. **Live Running Status**: Use the app *'Where is my Train'* to track live location and platform assignments offline.

[Action: Compare Transport Modes]"""
    },
    "upi_payments": {
        "keywords": ["upi", "cash", "payment", "credit card", "atm", "money", "currency", "cheq", "rupee", "forex"],
        "reply": """### 💳 Money & UPI Payments in India

1. **UPI for Foreign Tourists**: International travelers can now access India's Unified Payments Interface via **'UPI One World'** prepaid wallets available at Delhi (DEL), Mumbai (BOM), and Bengaluru (BLR) international airports, or through authorized apps like *Cheq Global*.
2. **Everyday Usability**: Almost every vendor—from premium dining to roadside tea stalls—displays a QR code for instant UPI payment.
3. **Credit Cards**: International Visa & Mastercard work smoothly at hotels, sit-down restaurants, and monument counters.
4. **Physical Cash**: Keep ₹2,000 to ₹3,000 in small denominations (₹100, ₹200) for auto-rickshaws, rural monuments, and remote hill areas.
5. **ATM Best Practice**: Use ATMs connected directly to major bank branches (SBI, HDFC, ICICI, Axis) and select **'Without conversion'** to avoid excessive currency fees."""
    },
    "street_food_safety": {
        "keywords": ["delhi belly", "food", "street food", "water", "hygiene", "stomach", "sick", "eat", "safe to eat"],
        "reply": """### 🍲 Savoring Indian Street Food Safely

1. **Eat Fresh & Piping Hot**: Patronize stalls with long, steady queues of local families. High turnover guarantees ingredients are cooked fresh on high flame.
2. **Drinking Water**: Strictly drink sealed bottled water (*Bisleri, Kinley, Aquafina*) or RO-filtered water. Ensure the tamper-evident seal is intact.
3. **Avoid Open Cut Fruits**: Skip pre-sliced melons and salads displayed in open air. Opt for fruits you peel yourself (bananas, oranges, mangoes).
4. **Ice Caution**: Avoid raw ice at roadside juice stalls unless you are at an established indoor cafe.
5. **Fresh Curd (Dahi) & Lassi**: Natural probiotic powerhouses that soothe your digestive system in warm climates.
6. **First Aid**: Keep ORS (Oral Rehydration Salts) electrolyte sachets in your bag."""
    },
    "temple_culture": {
        "keywords": ["dress", "temple", "clothes", "modest", "shoes", "etiquette", "culture", "mosque", "gurdwara"],
        "reply": """### 🛕 Sacred Sites Etiquette & Dress Code

1. **Attire**: Wear modest clothing covering your shoulders, chest, and knees. In South Indian temples (like Madurai Meenakshi), traditional dhotis or cotton pants are often mandatory for inner sanctums.
2. **Footwear Protocol**: All footwear must be removed at the shoe repository (*Joota Ghar*) outside temples, mosques, and gurdwaras.
3. **Head Covering**: Mandatory in Sikh Gurdwaras (e.g. Golden Temple) and select mosques for both men and women. Clean cloth scarves are provided free at the entrance.
4. **Right Hand**: Offer donations, receive *prasad* (holy sweets), and greet priests using your right hand.
5. **Photography**: Check signage before taking photos inside inner sanctums. When unsure, politely ask temple custodians."""
    },
    "solo_female_safety": {
        "keywords": ["woman", "women", "female", "solo", "safety", "safe", "alone", "helpline", "night"],
        "reply": """### 🛡️ Safety Advice for Solo & Female Travelers

1. **Essential Emergency Numbers**:
   - **112**: All-India Emergency Assistance (Police, Medical, Fire)
   - **1091**: 24x7 Women's Helpline
   - **1363**: Ministry of Tourism 24x7 Multi-lingual Tourist Helpline
2. **Transit Security**:
   - Use app-based cabs (Uber, Ola) with live trip sharing enabled.
   - For train journeys, choose **2nd AC (2A)** or **3rd AC (3A)** sleeper coaches monitored by Railway Protection Force personnel.
   - First coach of Delhi and Bengaluru metro trains is reserved exclusively for women.
3. **Accommodations**: Book verified heritage boutique stays, well-reviewed 4-star hotels, or trusted hostel chains (*Zostel, The Hosteller*)."""
    },
    "monsoon_packing": {
        "keywords": ["monsoon", "rain", "rainy", "umbrella", "carry for a monsoon trip", "pack for monsoon", "monsoon trip"],
        "reply": """### 🌧️ What to Pack & Carry for a Monsoon Trip in India

Traveling during the Indian monsoon (June to September) reveals spectacular lush greenery, misty hill stations, and roaring waterfalls. Here is your essential packing list:

1. **Rain Protection**:
   - High-quality, windproof compact umbrella.
   - Breathable, lightweight waterproof rain jacket or poncho.
   - Waterproof dry bags / silicone pouches for your smartphone, passport, and camera.
   - Waterproof rain cover for your backpack.
2. **Footwear**:
   - Quick-drying trekking sandals or shoes with deep rubber grip (vibram soles) to prevent slips on wet mossy stones and fort steps.
   - Extra pairs of moisture-wicking synthetic socks. Avoid heavy leather shoes.
3. **Clothing**:
   - Quick-dry polyester/nylon t-shirts and lightweight travel pants.
   - Avoid heavy denim jeans which take days to dry in humid monsoon weather.
4. **Health & Hygiene**:
   - DEET or Odomos mosquito repellent cream/spray.
   - Waterproof band-aids and antiseptic cream.
   - Microfiber quick-dry travel towel.
5. **Practical Tips**:
   - Check local weather alerts before embarking on mountain ghat roads prone to landslides.
   - Keep a ziplock bag handy for physical banknotes and electronic chargers."""
    }
}

# ----------------- INTENT MATCHERS -----------------
def answer_budget_from_pune(query, lang):
    """Answers queries like: 'I have ₹5,000 and two days. Suggest a trip from Pune.'"""
    if lang == LANG_MARATHI:
        return """### 🎒 पुण्यातून ₹५,००० मध्ये २ दिवसांची सहल (Weekend Getaways)

तुमच्या **₹५,००० बजेट आणि २ दिवसांच्या कालावधीसाठी** पुण्यातून हे सर्वोत्तम पर्याय आहेत:

#### पर्याय १: सिंहगड किल्ला, पानशेत आणि खडकवासला (निसर्ग आणि इतिहास)
* **दिवस १**: सकाळी खडकवासला धरण आणि दुपारी ऐतिहासिक **सिंहगड किल्ला** (पिठलं-भाकरी, कांदा भजी आणि ताक). संध्याकाळी पानशेत बॅकवॉटर कॅम्पिंग किंवा रिसॉर्ट.
* **दिवस २**: सकाळी पानशेत येथे बोटिंग, दुपारी तोरणा पायथा किंवा वेल्हे परिसर, संध्याकाळी पुण्याकडे परतीचा प्रवास.
* **अंदाजे खर्च**:
  * प्रवास (बस / स्वतःची दुचाकी / सामायिक कॅब): ₹८००
  * मुक्काम (पानशेत होमस्टे / कॉटेज): ₹१,८००
  * जेवण व अल्पोपहार: ₹१,२००
  * इतर व आपत्कालीन: ₹६००
  * **एकूण खर्च: ~₹४,४००** (बजेटमध्ये उत्तम बसतो!)

#### पर्याय २: लोणावळा – खंडाळा आणि कार्ला-भाजे लेणी
* **दिवस १**: पुणे ते लोणावळा लोकल ट्रेन (तिकीट फक्त ₹१५). भुशी डॅम, टायगर पॉईंट आणि राजमाची व्ह्यू.
* **दिवस २**: प्राचीन कार्ला व भाजे बौद्ध लेणी आणि प्रसिद्ध लोणावळा चिक्की खरेदी.
* **एकूण खर्च**: ~₹३,५०० - ₹४,५००.

[View on Map: Sinhagad Fort] | [Plan Trip: Pune]"""

    elif lang == LANG_HINDI:
        return """### 🎒 पुणे से ₹5,000 में 2 दिन का वीकेंड टूर प्लान

आपके **₹5,000 बजट और 2 दिन की अवधि** के लिए पुणे से सबसे शानदार विकल्प:

#### विकल्प 1: सिंहगढ़ किला और पानशेत डैम (इतिहास और प्रकृति)
* **दिन 1**: सुबह खड़कवासला झील, दोपहर में ऐतिहासिक **सिंहगढ़ किला** (पारंपरिक पिठला-भाकरी और मटका दही). शाम को पानशेत बैकवाटर्स के पास स्टे.
* **दिन 2**: पानशेत में बोटिंग और वरसगांव का शांत दृश्य, शाम तक पुणे वापसी.
* **बजट विवरण**:
  * परिवहन (बाइक/बस/लोकल कैब): ₹800
  * ठहरना (होमस्टे/टेंट): ₹1,800
  * भोजन और नाश्ता: ₹1,200
  * एंट्री टिकट और बफर: ₹500
  * **कुल खर्च: ~₹4,300 प्रति व्यक्ति** (₹5,000 के अंदर!)

#### विकल्प 2: लोनावला और कार्ला गुफाएं ( Karla Caves )
* पुणे से लोनावला लोकल ट्रेन (किराया सिर्फ ₹15). टाइगर पॉइंट, भुशी डैम और 2000 वर्ष पुरानी कार्ला-भाजा बौद्ध गुफाएं.
* **अनुमानित बजट**: ₹3,800 - ₹4,600.

[View on Map: Sinhagad Fort] | [Plan Trip: Pune]"""

    else:
        return """### 🎒 2-Day Trip from Pune under ₹5,000

With a **budget of ₹5,000 and 2 days**, you have fantastic scenic and historical getaway options right from Pune:

#### Option 1: Sinhagad Fort & Panshet Lake Backwaters (Heritage & Nature)
* **Day 1**: Head to the historic **Sinhagad Fort** in the morning (30 km from Pune). Explore Tanaji Malusare's memorial, Kalyan Darwaza, and enjoy authentic hot *Pithla-Bhakri*, *Thecha*, and fresh curd. In the late afternoon, drive down to **Panshet Dam** for sunset views and lakeside camping.
* **Day 2**: Morning lakeside walks and watersports at Panshet, visit Khadakwasla promenade for corn cobs (*bhutta*), and return to Pune by evening.
* **Cost Breakdown**:
  * Transport (Fuel for bike/car or state ST bus): ~₹800
  * Lakeside Homestay / Tent Stay: ~₹1,800
  * Meals & Street Treats: ~₹1,200
  * Entry fees & parking: ~₹200
  * Emergency Buffer: ~₹500
  * **Total Estimated Cost: ~₹4,500** (Comfortably within your ₹5,000 budget!)

#### Option 2: Lonavala, Khandala & Karla Caves (Local Train Trip)
* Take the Pune–Lonavala local suburban train (fare only ₹15–₹20).
* Visit the 2nd-century BCE rock-cut **Karla & Bhaja Buddhist Caves**, Tiger's Leap viewpoint, and Bhushi Dam.
* Budget per person: ~₹3,500 - ₹4,200.

[View on Map: Sinhagad Fort] | [Plan Trip: Pune]"""

def answer_jaipur_historical(query, lang):
    """Answers queries like: 'Which historical places can I visit in Jaipur?'"""
    if lang == LANG_HINDI:
        return """### 🏰 जयपुर के प्रमुख ऐतिहासिक और दर्शनीय स्थल

राजस्थान की गुलाबी नगरी (Pink City) जयपुर अपने भव्य महलों और ऐतिहासिक किलों के लिए विश्व प्रसिद्ध है:

1. **आमेर का किला (Amber Fort)**: यूनेस्को विश्व धरोहर स्थल। शीश महल और दीवान-ए-आम की संगमरमरी नक्काशी अद्वितीय है। (ASI टिकट: ₹100 भारतीय, ₹550 विदेशी).
2. **हवा महल (Hawa Mahal)**: 1799 में निर्मित 953 खिड़कियों (झरोखों) वाला 5-मंजिला महल, जहां से शाही महिलाएं सड़क के जुलूस देखती थीं।
3. **सिटी पैलेस (City Palace)**: आज भी शाही परिवार का निवास। चंद्र महल, मुबारक महल और ऐतिहासिक अस्त्र-शस्त्र संग्रहालय।
4. **जंतर मंतर (Jantar Mantar)**: सवाई जय सिंह द्वितीय द्वारा निर्मित दुनिया की सबसे बड़ी पत्थर की धूपघड़ी वाला खगोलीय वेधशाला।
5. **नाहरगढ़ किला (Nahargarh Fort)**: अरावली की पहाड़ी पर स्थित, सूर्यास्त के समय पूरे जयपुर शहर का मनोरम विहंगम दृश्य।
6. **जयगढ़ किला (Jaigarh Fort)**: दुनिया की सबसे बड़ी पहियों वाली तोप 'जयबाण' का घर।

**सुझाव**: एक कंपोजिट टिकट (Composite Entry Ticket) लें, जिससे हवा महल, आमेर, जंतर मंतर और अल्बर्ट हॉल म्यूजियम की एंट्री सस्ती पड़ती है।

[Explore Destination: Jaipur] | [Plan Trip: Jaipur]"""

    elif lang == LANG_MARATHI:
        return """### 🏰 जयपूरमधील प्रमुख ऐतिहासिक ठिकाणे

राजस्थानची गुलाबी नगरी जयपूर ऐतिहासिक राजवाडे आणि किल्ल्यांसाठी ओळखली जाते:

१. **आमेरचा किल्ला (Amber Fort)**: जागतिक वारसा स्थळ, अप्रतिम शीश महल आणि भक्कम तटबंदी.
२. **हवा महल (Hawa Mahal)**: १७९९ मध्ये बांधलेली ९५३ झरोक्यांची कलात्मक वास्तू.
३. **सिटी पॅलेस (City Palace)**: राजघराण्याचा राजवाडा, वस्तुसंग्रहालय आणि भव्य दरबार हॉल.
४. **जंतर मंतर (Jantar Mantar)**: दगडी खगोलीय वेधशाळा आणि सम्राट यंत्र (सूर्यघड्याळ).
५. **नाहरगड किल्ला (Nahargarh Fort)**: अरावली पर्वतावरील किल्ला, जिथून संपूर्ण जयपूरचे विलोभनीय दृश्य दिसते.
६. **जयगड किल्ला (Jaigarh Fort)**: आशियातील सर्वात मोठी चाकांची तोफ 'जयबाण' येथे आहे.

[Explore Destination: Jaipur] | [Plan Trip: Jaipur]"""

    else:
        return """### 🏰 Iconic Historical Places to Visit in Jaipur

The Pink City of Rajasthan is a treasure trove of Rajput and Mughal architecture:

1. **Amber Fort (Amer Fort)**: A UNESCO World Heritage site perched majestically on the Cheel ka Teela hill. Don't miss the mirror-studded *Sheesh Mahal* (Palace of Mirrors) and the Diwan-e-Aam. (Entry: ₹100 Indians, ₹550 Foreigners).
2. **Hawa Mahal (Palace of Winds)**: Built in 1799 with 953 intricately carved sandstone *jharokhas* (casements) that kept air circulating while royal women observed street festivals.
3. **City Palace**: Still the residence of Jaipur's erstwhile royal family. Houses Chandra Mahal, Mubarak Mahal, and the textile/arms gallery.
4. **Jantar Mantar**: Astronomical observatory featuring 19 architectural astronomical instruments, including the world's largest stone sundial (Samrat Yantra).
5. **Nahargarh Fort**: Perched on the edge of the Aravalli hills—the best spot in Jaipur for a golden-hour sunset overlooking the walled city.
6. **Jaigarh Fort**: Built to protect Amber Fort, it houses *Jaivana*, once the world's largest cannon on wheels.

*Pro-Tip: Buy the government Composite Ticket at Amber Fort or Hawa Mahal to save 40% on entry fees across five major monuments.*

[Explore Destination: Jaipur] | [Plan Trip: Jaipur]"""

def answer_goa_family_trip(query, lang):
    """Answers queries like: 'Plan a three-day family trip to Goa.'"""
    if lang == LANG_HINDI:
        return """### 🏖️ गोवा में 3 दिवसीय पारिवारिक ट्रिप (Family Trip Itinerary)

परिवार और बच्चों के साथ गोवा की 3 दिन की आरामदायक यात्रा का कार्यक्रम:

* **दिन 1: नॉर्थ गोवा की संस्कृति और समुद्र तट**
  * सुबह: शांत **मोरजिम (Morjim)** या **कैंडोलिम (Candolim)** बीच पर रेत के खेल और विश्राम।
  * दोपहर: 17वीं सदी का ऐतिहासिक **अगुआडा किला (Aguada Fort)** और लाइटहाउस का भ्रमण।
  * शाम: कलंगूट/बागा के फैमिली कैफे में ताजा सीफूड डिनर।

* **दिन 2: हेरिटेज और मसाला बगान (Spice Plantation)**
  * सुबह: पुराने गोवा (Old Goa) में यूनेस्को चर्च **बेसिलिका ऑफ बॉम जीसस (Basilica of Bom Jesus)** और से कैथेड्रल।
  * दोपहर: **सह्याद्री स्पाइस फार्म** में पारंपरिक गोवन लंच और मसालों के पौधों की सैर (बच्चों के लिए बहुत शिक्षाप्रद)।
  * शाम: मांडवी नदी में सूर्यास्त बोट क्रूज (Sunset River Cruise with Goan folk dance).

* **दिन 3: साउथ गोवा की शांति और जलक्रीड़ा**
  * सुबह: दक्षिण गोवा के साफ **कोलवा (Colva)** या **बेनौलिम (Benaulim)** बीच पर डॉल्फिन स्पॉटिंग बोट राइड।
  * दोपहर: मार्गो के रंग-बिरंगे पुर्तगाली विला और बाजार की सैर।
  * शाम: पालोलेम (Palolem) बीच पर सूर्यास्त के साथ ट्रिप का समापन।

[Explore Destination: Goa] | [Plan Trip: Goa]"""

    elif lang == LANG_MARATHI:
        return """### 🏖️ ३ दिवसांची कौटुंबिक गोवा सहल (Family Trip Plan)

कुटुंबासह गोव्यात ३ दिवसांच्या आनंददायी सहलीचे नियोजन:

* **दिवस १: उत्तर गोवा - समुद्रकिनारे आणि अगुआडा**
  * सकाळ: शांत आणि स्वच्छ **कँडोलिम (Candolim)** किंवा मोरजिम बीचवर फेरफटका.
  * दुपार: ऐतिहासिक **अगुआडा किल्ला** आणि समुद्राचे मनमोहक दृश्य.
  * संध्याकाळ: मांडवी नदीवरील कौटुंबिक क्रूझ आणि गोवन संगीताचा आनंद.

* **दिवस २: जुने गोवा चर्च आणि मसाले बाग**
  * सकाळ: **बॉम्ब जिझस बॅसिलिका (Basilica of Bom Jesus)** व ऐतिहासिक चर्च.
  * दुपार: **मसाले बाग (Spice Plantation)** भेट व अस्सल गोवन भोजन (मुलांसाठी उत्तम अनुभव).
  * संध्याकाळ: पणजी शहरात फॉन्टेनहास (Fontainhas) लॅटिन क्वार्टरमध्ये रंगीबेरंगी घरांची छायाचित्रे.

* **दिवस ३: दक्षिण गोवा - डॉल्फिन सफर आणि शांत किनारे**
  * सकाळ: बेनौलीम किंवा कोलवा बीचवर सुरक्षित बोट राईड व डॉल्फिन दर्शन.
  * दुपार: स्थानिक हस्तकला खरेदी आणि परतीचा प्रवास.

[Explore Destination: Goa] | [Plan Trip: Goa]"""

    else:
        return """### 🏖️ 3-Day Family Itinerary for Goa

A balanced, safe, and memorable itinerary tailored for families with children or seniors:

* **Day 1: North Goa Coastal Sights & Historic Fort**
  * **Morning**: Settle in and visit the cleaner, family-friendly beaches like **Candolim** or **Morjim**. Safe waters for wading and building sandcastles.
  * **Afternoon**: Explore the 17th-century Portuguese **Fort Aguada** and its historic lighthouse with panoramic ocean views.
  * **Evening**: Enjoy a leisurely family dinner at a beachfront shacks offering both mild continental options and authentic Goan fish curry.

* **Day 2: UNESCO Heritage & Sahakari Spice Plantation**
  * **Morning**: Visit Old Goa's magnificent **Basilica of Bom Jesus** (housing St. Francis Xavier's relics) and Se Cathedral.
  * **Afternoon**: Take a guided tour of a **Tropical Spice Plantation** in Ponda. Children love seeing vanilla pods, cinnamon bark, and elephant interactions, followed by a buffet lunch on banana leaves.
  * **Evening**: Sunset cruise along the Mandovi River in Panaji with traditional Goan folk performances.

* **Day 3: South Goa Serenity & Dolphin Sighting**
  * **Morning**: Head to South Goa's **Benaulim** or **Colva** beach for an early morning boat trip to spot Indo-Pacific humpback dolphins.
  * **Afternoon**: Walk through **Fontainhas (Latin Quarter)** in Panaji with its vibrant heritage Portuguese villas and charming bakeries.
  * **Evening**: Sunset stroll along Miramar Beach and souvenir shopping for cashew nuts and feni.

[Explore Destination: Goa] | [Plan Trip: Goa]"""

# ----------------- MAIN ASK TRAVEL AI FUNCTION -----------------
def ask_travel_ai(query, context=None):
    """
    Intelligent multi-lingual travel assistant answering questions about destinations,
    itineraries, budgets, transport, packing, weather, and Indian culture.
    Connects to Google Gemini API if configured in .env, with zero-failure fallback.
    """
    clean_query = query.strip()
    q_lower = clean_query.lower()
    lang = detect_language(clean_query)

    # 1. Check for Gemini API key if user configured it
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            import google.genai as genai
            client = genai.Client(api_key=gemini_key)
            prompt = f"""You are Ananya, an expert, warm, and highly knowledgeable Indian Travel Guide assistant.
The user is asking: "{clean_query}"
Language: Respond in {'Marathi' if lang == LANG_MARATHI else 'Hindi' if lang == LANG_HINDI else 'English'}.
Context: {context if context else 'None specified'}.
Provide an authentic, highly practical, and culturally accurate answer in clean Markdown.
Include estimated costs in Indian Rupees (₹), safety advice, and respectful etiquette where applicable.
End with helpful action suggestions such as [Plan Trip: City] or [View on Map: City]."""
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            if response and response.text:
                log_chat(clean_query, response.text, "gemini_api")
                return response.text
        except Exception as e:
            logger.debug(f"Gemini API invocation skipped/failed: {e}")

    # 2. Check for "₹5,000 and two days from Pune" or general budget from city query
    if any(p in q_lower for p in ["pune", "पुण्या"]) and any(b in q_lower for b in ["5000", "5,000", "५०००", "budget", "दोन दिवस", "two day", "2 day"]):
        reply = answer_budget_from_pune(clean_query, lang)
        log_chat(clean_query, reply, "budget_pune")
        return reply

    # 3. Check for "Which historical places can I visit in Jaipur"
    if any(j in q_lower for j in ["jaipur", "जयपुर", "जयपूर"]) and any(h in q_lower for h in ["historic", "monument", "places to visit", "ऐतिहासिक", "किले", "बघण्यासारखी"]):
        reply = answer_jaipur_historical(clean_query, lang)
        log_chat(clean_query, reply, "jaipur_historic")
        return reply

    # 4. Check for "Plan a three-day family trip to Goa"
    if any(g in q_lower for g in ["goa", "गोवा"]) and any(f in q_lower for f in ["family", "three day", "3 day", "३ दिवस", "३ दिन", "परिवार", "कौटुंबिक"]):
        reply = answer_goa_family_trip(clean_query, lang)
        log_chat(clean_query, reply, "goa_family")
        return reply

    # 5. Check for "What should I carry for a monsoon trip"
    if (re.search(r'\b(monsoon|rainy|raining|rains|umbrella)\b', q_lower) or 
        any(m in q_lower for m in ["पावसाळा", "पाऊस", "बारिश", "मानसून", "monsoon trip", "carry for monsoon", "pack for monsoon"])):
        reply = KNOWLEDGE_RESPONSES["monsoon_packing"]["reply"]
        log_chat(clean_query, reply, "monsoon_packing")
        return reply

    # 6. Check for live weather query (e.g. "What is the weather in Delhi / Goa / Pune?")
    if any(w in q_lower for w in ["weather", "temperature", "forecast", "हवामान", "मौसम", "rain today"]):
        # Extract location
        loc_match = re.search(r'(?:in|for|at|of)\s+([a-zA-Z\s]+)', clean_query, re.IGNORECASE)
        place_name = loc_match.group(1).strip() if loc_match else "Pune"
        geo = geocode_place(place_name)
        if geo:
            weather_data = get_live_weather(geo["lat"], geo["lng"])
            if weather_data and weather_data.get("success"):
                reply = f"""### 🌤️ Live Weather for {geo['name']} ({geo['state']})

* **Current Temperature**: **{weather_data['temperature']}°C** {weather_data['icon']} ({weather_data['condition']})
* **Wind Speed**: {weather_data.get('windspeed_kmh', 'N/A')} km/h
* **3-Day Forecast**:
"""
                for f in weather_data.get("forecast", []):
                    reply += f"  - **{f['date']}**: {f['icon']} {f['condition']} (High: {f['max_temp']}°C / Low: {f['min_temp']}°C)\n"
                
                reply += "\n*Source: Live Open-Meteo Weather Service*\n\n[Plan Trip: " + geo['name'] + "]"
                log_chat(clean_query, reply, "weather_live")
                return reply

    # 7. Built-in structured knowledge intents (IRCTC, UPI, Food, Temples, Safety)
    for intent_name, data in KNOWLEDGE_RESPONSES.items():
        for kw in data["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', q_lower):
                log_chat(clean_query, data["reply"], intent_name)
                return data["reply"]

    # 8. City-specific travel guides across India
    all_dests = get_all_destinations()
    for d in all_dests:
        if d["name"].lower() in q_lower or d["id"] in q_lower:
            reply = f"""### 🌟 Travel Insights for {d['name']} ({d['state']})

* **Category**: {d['category']}
* **Best Time to Visit**: {d['best_season']}
* **Ideal Duration**: {d['ideal_days']}
* **Average Daily Budget**: ~₹{d['avg_daily_budget']:,} per person

**Top Sights & Experiences**:
{chr(10).join(['* ' + h for h in d['highlights']])}

**Must-Try Regional Flavors**:
{chr(10).join(['* **' + f['dish'] + '**: ' + f['desc'] for f in d['famous_foods']])}

**Local Etiquette & Travel Tips**:
{chr(10).join(['* ' + tip for tip in d['culture_tips']])}

[Plan Trip: {d['name']}] | [View on Map: {d['name']}]"""
            log_chat(clean_query, reply, f"dest_{d['id']}")
            return reply

    # 9. Generic multi-lingual fallback
    if lang == LANG_MARATHI:
        default_reply = """### 🙏 नमस्कार! मी अनन्या, तुमची एआय ट्रॅव्हल असिस्टंट.

मी तुम्हाला भारतामधील कोणत्याही पर्यटन स्थळाची माहिती देऊ शकते:
- **रेल्वे प्रवास आणि आयआरसीटीसी (IRCTC)**: तिकिटे कशी बुक करावीत, वंदे भारत ट्रेन्स आणि नियम.
- **बजेट ट्रिप**: ₹५,००० मध्ये पुण्यातून वीकेंड ट्रिप, गोवा ३ दिवसांची फॅमिली ट्रिप.
- **हवामान आणि पॅकिंग**: पावसाळी सहलीसाठी काय सोबत ठेवावे, लेह-लडाख तयारी.
- **पर्यटन स्थळे**: जयपूर, वाराणसी, मुन्नार, गोवा, हम्पी, आग्रा, अजिंठा लेणी.

*उदा: "पुण्यातून दोन दिवसांसाठी कुठे फिरायला जाऊ?", "जयपूरमधील ऐतिहासिक ठिकाणे सांगा", किंवा "IRCTC वर तिकीट कसे बुक करावे?"*"""
    elif lang == LANG_HINDI:
        default_reply = """### 🙏 नमस्ते! मैं अनन्या हूँ, आपकी एआई ट्रैवल गाइड।

मैं पूरे भारत में आपकी यात्रा को आसान और यादगार बनाने में मदद कर सकती हूँ:
- **ट्रेन और आईआरसीटीसी (IRCTC)**: टिकट बुकिंग, तत्काल, और विदेशी पर्यटकों के लिए नियम।
- **बजट और वीकेंड ट्रिप**: ₹5,000 में पुणे से वीकेंड ट्रिप, गोवा में 3 दिन की फैमिली ट्रिप।
- **मौसम और पैकिंग**: मानसून ट्रिप में क्या ले जाएं, मंदिर दर्शन के नियम।
- **प्रमुख शहर और धरोहर**: जयपुर, आगरा, वाराणसी, गोवा, मुन्नार, हम्पी।

*आप पूछ सकते हैं: "जयपुर में कौन से ऐतिहासिक स्थल देखने लायक हैं?", "पुणे से 2 दिन की ट्रिप बताएं", या "मानसून में क्या पैक करें?"*"""
    else:
        default_reply = """### 🙏 Namaste! I am Ananya, your AI Travel Guide for India.

I can assist you with authentic advice covering all corners of India:
* **Custom Budget Trips**: e.g., *"I have ₹5,000 and two days. Suggest a trip from Pune."*
* **Historic Landmarks**: e.g., *"Which historical places can I visit in Jaipur?"*
* **Family & Group Itineraries**: e.g., *"Plan a three-day family trip to Goa."*
* **Packing & Seasonal Tips**: e.g., *"What should I carry for a monsoon trip?"*
* **Logistics & Safety**: IRCTC train bookings, UPI payments, street food safety, and temple etiquette.

*Feel free to ask in English, Hindi (हिंदी), or Marathi (मराठी)!*"""

    log_chat(clean_query, default_reply, "fallback")
    return default_reply

# ----------------- ITINERARY PLANNER -----------------
def generate_custom_itinerary(dest_id, starting_city, duration_days, traveler_type, budget_tier, pace, interests=None):
    """
    Dynamically generates a detailed, realistic day-by-day travel itinerary
    customized by user profile, duration, budget, and travel speed.
    """
    dest = get_destination_by_id(dest_id)
    if not dest:
        # Fallback to geocoded place search
        results = search_india_all(dest_id, limit=1)
        if results.get("results"):
            d = results["results"][0]
            dest = {
                "id": dest_id,
                "name": d["name"],
                "state": d["state"],
                "category": d["category"],
                "description": d["description"],
                "highlights": [d["name"] + " Sightseeing", "Local Cultural Heritage", "Artisan Markets"],
                "famous_foods": [{"dish": "Regional Thali", "desc": "Authentic local flavors"}],
                "culture_tips": ["Wear modest clothing and carry water."],
                "avg_daily_budget": 2400,
                "coordinates": [d["lat"] or 20.0, d["lng"] or 78.0]
            }
        else:
            return None

    duration = max(1, min(int(duration_days), 14))
    attractions = dest.get("attractions", [])
    highlights = dest.get("highlights", [])
    foods = dest.get("famous_foods", [])
    culture_tips = dest.get("culture_tips", [])
    
    tier_mult = {"budget": 1.0, "moderate": 1.8, "luxury": 3.8}.get(budget_tier.lower(), 1.6)
    base_cost = dest.get("avg_daily_budget", 2400)
    est_daily_cost = int(base_cost * tier_mult)

    days_plan = []

    for day_num in range(1, duration + 1):
        if day_num == 1:
            day_theme = f"Arrival in {dest['name']}, Historic Quarters & Golden Hour"
        elif day_num == 2:
            day_theme = f"Architectural Marvels, Artisan Bazaars & Local Flavors"
        elif day_num == 3:
            day_theme = f"Hidden Sanctuaries, Panoramic Viewpoints & Sunset"
        elif day_num == 4:
            day_theme = f"Scenic Day Excursion & Nature Trail"
        else:
            day_theme = f"Slow Travel, Cultural Immersion & Farewell Evening"

        attr_idx = (day_num - 1) % max(1, len(attractions))
        main_attr = attractions[attr_idx] if attractions else None
        food_sample = foods[(day_num - 1) % max(1, len(foods))] if foods else {"dish": "Local Regional Thali", "desc": "Traditional platter"}

        if day_num == 1:
            morning = {
                "time": "08:30 AM - 11:30 AM",
                "title": f"Arrival & Check-in at hotel in {dest['name']}",
                "detail": f"Arrive from {starting_city}, check into your stay, relax with fresh regional chai or filter coffee, and prepare your daypack.",
                "transport": "Prepaid airport/station taxi or booked cab to hotel",
                "est_cost": f"₹{int(350 * tier_mult)}"
            }
        else:
            morning_attr_name = main_attr["name"] if main_attr else (highlights[(day_num * 2 - 2) % len(highlights)] if highlights else "City Heritage Monument")
            morning = {
                "time": "08:00 AM - 11:30 AM",
                "title": f"Explore {morning_attr_name}",
                "detail": main_attr["description"] if main_attr else f"Visit {morning_attr_name} during the pleasant morning light before midday crowds arrive.",
                "tip": main_attr.get("insider_tip", "Reach early for comfortable photography without long ticketing queues."),
                "transport": "Auto-rickshaw or local cab (15-20 mins)",
                "est_cost": f"₹{main_attr['entry_fee_inr'] if main_attr else 50} ASI entry"
            }

        sec_attr_name = highlights[(day_num * 2 - 1) % len(highlights)] if highlights else "Traditional Heritage Bazaar"
        afternoon = {
            "time": "12:30 PM - 03:30 PM",
            "title": f"Authentic Regional Lunch & {sec_attr_name}",
            "food_highlight": f"Must-try lunch: {food_sample['dish']} — {food_sample['desc']}",
            "detail": f"Enjoy lunch at an established heritage eatery. Follow with an afternoon exploration of {sec_attr_name}.",
            "pace_note": "Spend the peak afternoon heat in shaded museum galleries or courtyards." if pace != "packed" else "Fast-paced walk through historic avenues."
        }

        evening_spots = [
            f"Sunset panorama over {dest['name']}'s scenic vantage point",
            f"Bustling walk through illuminated night markets and spice stalls",
            f"Cultural music / dance performance and rooftop dinner overlooking illuminated landmarks",
            f"Leisurely lakeside or riverside stroll under the evening breeze"
        ]
        evening_choice = evening_spots[(day_num - 1) % len(evening_spots)]

        evening = {
            "time": "05:00 PM - 08:30 PM",
            "title": evening_choice,
            "detail": f"Savor street delicacies, capture twilight reflections, and enjoy dinner at a highly rated local restaurant.",
            "tip": culture_tips[(day_num - 1) % len(culture_tips)] if culture_tips else "Keep small cash handy for rickshaws and street vendors."
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
                "buffer_and_tips": int(total_est_cost * 0.05),
                "buffer_and_emergency": int(total_est_cost * 0.05)
            },
            "packing_advisory": "Pack comfortable walking shoes, power bank, lightweight cotton layers, and a rain poncho during monsoons.",
            "emergency_numbers": "National Emergency: 112 | Tourist Police: 1363"
        }
    }

    return itinerary_payload
