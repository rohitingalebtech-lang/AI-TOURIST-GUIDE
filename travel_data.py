"""
travel_data.py
Rich, realistic, curated dataset for Indian destinations, attractions, and transport routes.
Spanning North, South, West, East, Central, and Northeast India.
"""

DESTINATIONS = [
    {
        "id": "jaipur",
        "name": "Jaipur",
        "title": "The Pink City of Royalty & Palaces",
        "state": "Rajasthan",
        "region": "North",
        "category": "Heritage & Culture",
        "best_season": "Winter (Oct - Mar)",
        "ideal_days": "3-4 days",
        "avg_daily_budget": 2400,
        "rating": 4.8,
        "coordinates": [26.9124, 75.7873],
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Hawa Mahal bathed in morning sunlight, Jaipur",
        "description": "The capital of Rajasthan, Jaipur is celebrated for its rose-pink terracotta architecture, majestic hilltop forts, vibrant bazaars, and opulent royal history. Founded in 1727 by Maharaja Sawai Jai Singh II, it forms the famous Golden Triangle alongside Delhi and Agra.",
        "highlights": ["Hawa Mahal", "Amber Fort", "City Palace", "Jantar Mantar", "Nahargarh Fort Sunset"],
        "famous_foods": [
            {"dish": "Dal Baati Churma", "desc": "Crisp baked wheat dumplings with spiced lentils and sweetened powdered grain"},
            {"dish": "Pyaaz Kachori", "desc": "Flaky deep-fried pastry stuffed with spicy onion filling from Rawat Mishtan Bhandar"},
            {"dish": "Ghevar", "desc": "Honeycomb disc-shaped sweet soaked in saffron sugar syrup during festivals"},
            {"dish": "Laal Maas", "desc": "Fiery Rajasthani mutton curry simmered with Mathania red chillies"}
        ],
        "culture_tips": [
            "Bargain politely in Johari Bazaar and Bapu Bazaar—starting at about 50-60% of quoted prices is standard.",
            "Dress modestly when visiting temples and the City Palace; cover shoulders and knees.",
            "Take the government-approved electric shuttle or walk up to Amber Fort rather than using elephant rides for ethical reasons.",
            "Visit Nahargarh Fort around 4:30 PM to catch a panoramic golden hour over the entire walled city."
        ],
        "how_to_reach": {
            "air": "Jaipur International Airport (JAI), 13 km from city center; domestic & select Gulf flights.",
            "rail": "Jaipur Junction (JP) is connected by Shatabdi, Vande Bharat, and superfast trains to Delhi (4.5 hrs) and Mumbai.",
            "road": "Well-connected via NH48 and Delhi-Mumbai Expressway. Frequent AC Volvo buses from ISBT Delhi (5 hrs)."
        }
    },
    {
        "id": "varanasi",
        "name": "Varanasi",
        "title": "The Spiritual Heart of the Sacred Ganga",
        "state": "Uttar Pradesh",
        "region": "North",
        "category": "Spiritual & Wellness",
        "best_season": "Winter (Oct - Mar)",
        "ideal_days": "2-3 days",
        "avg_daily_budget": 1800,
        "rating": 4.9,
        "coordinates": [25.3176, 82.9739],
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Evening Ganga Aarti ceremony at Dashashwamedh Ghat, Varanasi",
        "description": "One of the world's oldest continuously inhabited cities, Varanasi (Kashi) is the spiritual epicenter of Hinduism on the banks of the Holy River Ganga. Here life and afterlife meet along timeless stone ghats, winding alleyways, and reverberating temple chants.",
        "highlights": ["Dashashwamedh Ghat Aarti", "Kashi Vishwanath Temple", "Sunrise Boat Ride", "Assi Ghat Morning Yoga", "Sarnath Buddhist Stupa"],
        "famous_foods": [
            {"dish": "Banarasi Kachori Sabzi", "desc": "Crispy puffed puris served with tangy spiced potato-chickpea curry at morning stalls"},
            {"dish": "Malaiyo", "desc": "Winter dessert made of delicate saffron-flavored milk froth topped with pistachios"},
            {"dish": "Banarasi Paan", "desc": "Aromatic betel leaf filled with gulkand, supari, and spices—an iconic digestif"},
            {"dish": "Blue Lassi / Peda", "desc": "Thick hand-churned curd lassi topped with malai and seasonal fruits"}
        ],
        "culture_tips": [
            "Maintain utmost silence and strictly avoid photography at Manikarnika and Harishchandra burning ghats out of respect.",
            "Book government-registered hand-rowed boats at Assi or Dashashwamedh Ghat at sunrise (approx ₹300-500 per person).",
            "Be prepared to remove footwear outside ghats and temple complexes; carry a small cloth bag for your shoes.",
            "Beware of unauthorized touts claiming to be temple priests demanding expensive ritual donations."
        ],
        "how_to_reach": {
            "air": "Lal Bahadur Shastri International Airport (VNS), 25 km from ghats; direct flights from Delhi, Mumbai, Bengaluru.",
            "rail": "Varanasi Junction (BSB) and Pt. Deen Dayal Upadhyaya Junction (DDU) receive Vande Bharat Express from New Delhi (8 hrs).",
            "road": "Connected via NH19. Overnight luxury sleeper buses available from Lucknow and Delhi."
        }
    },
    {
        "id": "munnar",
        "name": "Munnar",
        "title": "Misty Hills & Emerald Tea Plantations",
        "state": "Kerala",
        "region": "South",
        "category": "Hill Stations & Nature",
        "best_season": "Sept - Mar & Monsoon for greenery",
        "ideal_days": "3-4 days",
        "avg_daily_budget": 2800,
        "rating": 4.8,
        "coordinates": [10.0889, 77.0595],
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Rolling tea estates veiled in early morning mist, Munnar",
        "description": "Perched at 1,600 meters above sea level in the Western Ghats of Kerala, Munnar was once the summer resort of the British administration. It is blanketed with rolling carpeted tea estates, cascading waterfalls, winding mountain paths, and the endangered Nilgiri Tahr.",
        "highlights": ["Eravikulam National Park", "Mattupetty Dam", "Kolukkumalai Tea Estate (World's Highest)", "Attukad Waterfalls", "Top Station"],
        "famous_foods": [
            {"dish": "Kerala Appam with Vegetable Stew", "desc": "Lacy fermented rice pancakes with coconut milk infused vegetable curry"},
            {"dish": "Freshly Brewed Munnar BOP Tea", "desc": "Pure single-origin Broken Orange Pekoe black tea freshly plucked from estates"},
            {"dish": "Malabar Parotta & Beef/Mushroom Roast", "desc": "Layered flaky flatbread with spicy slow-cooked masala gravy"},
            {"dish": "Puttu and Kadala Curry", "desc": "Steamed cylindrical rice cake layered with grated coconut and black chickpea curry"}
        ],
        "culture_tips": [
            "Carry a warm fleece jacket; temperatures drop significantly in the evening and early morning.",
            "Buy tea and spices directly from estate retail counters (KDHP / Ripple Tea) to ensure authentic non-adulterated quality.",
            "Respect the protected wildlife in Eravikulam; strictly no plastic waste and stay on marked trails.",
            "Hire a local 4x4 Jeep driver for the sunrise trek to Kolukkumalai as regular vehicles cannot traverse the boulder roads."
        ],
        "how_to_reach": {
            "air": "Cochin International Airport (COK) is 110 km away (approx 3.5 to 4 hours scenic drive through spice hills).",
            "rail": "Nearest major railheads are Aluva (110 km) and Ernakulam Junction (125 km).",
            "road": "Frequent KSRTC express buses from Kochi, Kottayam, and Madurai. Scenic winding Ghat roads via NH85."
        }
    },
    {
        "id": "goa",
        "name": "Goa",
        "title": "Sun-Kissed Beaches, Portuguese Heritage & Susegad",
        "state": "Goa",
        "region": "West",
        "category": "Beaches & Coastal",
        "best_season": "Nov - Feb (Winter) / Jul - Aug (Lush Green Monsoon)",
        "ideal_days": "4-5 days",
        "avg_daily_budget": 3200,
        "rating": 4.7,
        "coordinates": [15.2993, 74.1240],
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Golden coastline and palm fronds at Palolem Beach, South Goa",
        "description": "India's pocket-sized coastal paradise blends 450 years of Portuguese influence with vibrant tropical Konkan vibes. North Goa is famed for lively beach shacks, night markets, and water sports, while South Goa offers tranquil pristine sands, spice plantations, and quiet heritage villages.",
        "highlights": ["Old Goa Churches (Basilica of Bom Jesus)", "Palolem & Agonda Beaches", "Dudhsagar Waterfalls", "Fontainhas Latin Quarter", "Aguada & Chapora Forts"],
        "famous_foods": [
            {"dish": "Goan Fish Curry Thali", "desc": "Fresh kingfish or pomfret in tangy kokum-coconut gravy served with rice and kismoor"},
            {"dish": "Pork Vindaloo / Chicken Xacuti", "desc": "Signature Goan curries with Portuguese vinegar or roasted coconut spice blends"},
            {"dish": "Bebinca", "desc": "Traditional multi-layered baked Indo-Portuguese pudding made of coconut milk and egg yolks"},
            {"dish": "Poi Bread with Chorizo", "desc": "Crusty local earthen-oven baked Goan bread filled with spiced Goan sausage"}
        ],
        "culture_tips": [
            "Embrace 'Susegad'—the relaxed, contented pace of Goan lifestyle. Many smaller shops close between 1:30 PM and 4:00 PM.",
            "Rent a self-drive scooter (₹350-500/day); always wear a helmet, carry your original driving license, and strictly never drink and ride.",
            "Dress respectfully when entering historic churches like Basilica of Bom Jesus and Se Cathedral (shoulders and knees covered).",
            "Support eco-friendly beach shacks and never litter glass bottles or plastics on coastal shorelines."
        ],
        "how_to_reach": {
            "air": "Two international airports: Dabolim Airport (GOI) in South/Central Goa and Manohar International Airport Mopa (GOX) in North Goa.",
            "rail": "Madgaon Junction (MAO) and Thivim (THVM) connected by Konkan Railway including Vande Bharat & Tejas Express from Mumbai.",
            "road": "Connected via NH66. Overnight sleeper buses run daily from Mumbai, Pune, and Bengaluru."
        }
    },
    {
        "id": "agra",
        "name": "Agra",
        "title": "Architectural Wonder of the Mughal Dynasty",
        "state": "Uttar Pradesh",
        "region": "North",
        "category": "Heritage & Culture",
        "best_season": "Oct - Mar",
        "ideal_days": "1-2 days",
        "avg_daily_budget": 2200,
        "rating": 4.9,
        "coordinates": [27.1767, 78.0081],
        "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "The majestic white marble facade of the Taj Mahal at dawn",
        "description": "Situated on the banks of River Yamuna, Agra was the imperial capital of the Mughal Empire under Akbar, Jahangir, and Shah Jahan. It is home to three UNESCO World Heritage Sites including the ethereal Taj Mahal, Agra Fort, and the abandoned sandstone city of Fatehpur Sikri.",
        "highlights": ["Taj Mahal Sunrise", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh Sunset View", "Itmad-ud-Daulah (Baby Taj)"],
        "famous_foods": [
            {"dish": "Agra Petha", "desc": "Translucent candied ash gourd sweet available in classic, kesar, paan, and chocolate flavors"},
            {"dish": "Bedmi Puri & Aloo", "desc": "Crisp urad dal stuffed puris served with spicy fenugreek-infused potato curry"},
            {"dish": "Mughlai Biryani & Kebabs", "desc": "Slow-cooked aromatic basmati rice layered with tender meat, saffron, and whole spices"},
            {"dish": "Jalebi with Rabri", "desc": "Hot spiral crisps soaked in sugar syrup served over chilled thickened creamy milk"}
        ],
        "culture_tips": [
            "The Taj Mahal is strictly CLOSED on Fridays for congregational prayers. Plan your dates accordingly.",
            "Book official ASI monument tickets online at asi.payumoney.com to skip massive physical ticket queues and get an automatic ₹50 discount.",
            "Tripods, large bags, drones, lighters, and eatables are strictly prohibited inside the Taj Mahal complex.",
            "Visit Mehtab Bagh across the river around 5:00 PM for a serene view of the Taj reflecting in the Yamuna without the massive crowds."
        ],
        "how_to_reach": {
            "air": "Agra Airport has limited flights; most travelers fly into New Delhi (DEL) and take express trains or expressway.",
            "rail": "Agra Cantt (AGC) is served by Gatimaan Express (100 mins from Delhi) and Bhopal Shatabdi.",
            "road": "Yamuna Expressway offers a seamless 3.5-hour drive from New Delhi/Noida."
        }
    },
    {
        "id": "ladakh",
        "name": "Leh Ladakh",
        "title": "High-Altitude Passes, Monasteries & Azure Lakes",
        "state": "Ladakh (UT)",
        "region": "North",
        "category": "Adventure & Mountain",
        "best_season": "May - Sept (Roads open & warm days)",
        "ideal_days": "6-7 days",
        "avg_daily_budget": 3800,
        "rating": 4.9,
        "coordinates": [34.1526, 77.5771],
        "image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Dramatic mountain reflection over Pangong Tso, Ladakh",
        "description": "Known as the 'Land of High Passes', Ladakh is an alpine desert nestled between the Karakoram and Himalayan ranges. With ancient Tibetan Buddhist monasteries perched on craggy pinnacles, shifting sand dunes of Nubra Valley, and the chameleon waters of Pangong Tso, it is a high-altitude marvel.",
        "highlights": ["Pangong Tso Lake", "Nubra Valley & Hunder Sand Dunes", "Khardung La Pass (5,359m)", "Thiksey Monastery", "Hemis Gompa"],
        "famous_foods": [
            {"dish": "Ladakhi Thukpa", "desc": "Hearty Tibetan noodle soup with seasonal mountain greens, broth, and mild local spices"},
            {"dish": "Steamed Momos & Tingmo", "desc": "Delicate handmade dumplings and steamed flower-shaped yeast bread served with chili chutney"},
            {"dish": "Butter Tea (Gur Gur Chai)", "desc": "Traditional savory pink tea churned with yak butter, salt, and tea leaves"},
            {"dish": "Skyu", "desc": "Traditional Ladakhi pasta dish simmered with root vegetables and meat in a rich aromatic broth"}
        ],
        "culture_tips": [
            "ACCLIMATIZATION IS MANDATORY: Spend your first full 48 hours resting in Leh town (3,500m) without strenuous physical activity to prevent AMS (Altitude Sickness).",
            "Inner Line Permits (ILP) are required for domestic & foreign tourists visiting Nubra, Pangong, and Tso Moriri (easily applied online or via local agencies).",
            "Carry adequate cash (INR) as ATMs in Nubra and Pangong are unreliable with frequent network outages.",
            "Walk clockwise around chortens (stupas), mani walls, and inside prayer halls of gompas."
        ],
        "how_to_reach": {
            "air": "Kushok Bakula Rimpochee Airport (IXL) in Leh has daily direct flights from Delhi, Mumbai, and Srinagar.",
            "rail": "No direct rail connectivity; nearest major railhead is Jammu Tawi or Chandigarh.",
            "road": "Two legendary road routes: Manali-Leh Highway (475 km) and Srinagar-Leh Highway (420 km), open June through mid-October."
        }
    },
    {
        "id": "udaipur",
        "name": "Udaipur",
        "title": "City of Lakes, Floating Palaces & Romance",
        "state": "Rajasthan",
        "region": "West",
        "category": "Heritage & Culture",
        "best_season": "Oct - Mar",
        "ideal_days": "3 days",
        "avg_daily_budget": 3000,
        "rating": 4.8,
        "coordinates": [24.5854, 73.7125],
        "image": "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Lake Pichola and the illuminated City Palace of Udaipur",
        "description": "Referred to as the 'Venice of the East', Udaipur is cradled by the purple Aravalli hills and wrapped around a series of serene artificial lakes. Founded in 1559 by Maharana Udai Singh II, it boasts grand marble palaces, lakeside ghats, and romantic boat rides.",
        "highlights": ["City Palace & Museum", "Lake Pichola Sunset Boat Cruise", "Jag Mandir Island", "Saheliyon Ki Bari", "Bagore Ki Haveli Cultural Dance"],
        "famous_foods": [
            {"dish": "Mawa Kachori", "desc": "Sweet fried pastry stuffed with sweetened khoya and dry fruits dipped in sugar syrup"},
            {"dish": "Rajasthani Gatte Ki Sabzi", "desc": "Poached gram flour dumplings simmered in a spiced tangy yogurt gravy"},
            {"dish": "Mirchi Bada", "desc": "Spicy batter-fried stuffed green chili fritters served with mint coriander chutney"},
            {"dish": "Mewari Khichdi", "desc": "Slow-cooked savory grain porridge prepared with pure desi ghee and mild spices"}
        ],
        "culture_tips": [
            "Attend the Dharohar Folk Dance show at Bagore Ki Haveli at 7:00 PM; purchase tickets by 5:00 PM as seats fill up fast.",
            "Opt for a sunset boat cruise on Lake Pichola departing from the City Palace jetty for prime golden-hour lighting.",
            "Explore the old city lanes around Gangaur Ghat on foot; large cars cannot navigate the narrow alleyways.",
            "Support local miniature painting artists, but verify hand-painted art versus printed fabric."
        ],
        "how_to_reach": {
            "air": "Maharana Pratap Airport (UDR), 22 km from city center; direct flights to Delhi, Mumbai, Bengaluru, Jaipur.",
            "rail": "Udaipur City Railway Station (UDZ) connects directly to Delhi (Mewar Express) and Mumbai.",
            "road": "Connected via NH48. Overnight luxury sleeper buses available from Ahmedabad (4 hrs) and Jaipur (6.5 hrs)."
        }
    },
    {
        "id": "rishikesh",
        "name": "Rishikesh",
        "title": "Yoga Capital of the World & Himalayan Gateway",
        "state": "Uttarakhand",
        "region": "North",
        "category": "Spiritual & Adventure",
        "best_season": "Oct - Apr (rafting season: Sept - June)",
        "ideal_days": "3-4 days",
        "avg_daily_budget": 2000,
        "rating": 4.8,
        "coordinates": [30.0869, 78.2676],
        "image": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Suspension bridge and tranquil Ganga riverbanks in Rishikesh",
        "description": "Where the emerald Ganga leaves the Shivalik Himalayas and flows into the northern plains, Rishikesh serves as a global sanctuary for yoga, meditation, and high-adrenaline white-water rafting. Beatles visited in 1968, putting its serene ashrams on the world cultural map.",
        "highlights": ["Triveni Ghat Evening Aarti", "White Water Rafting (Grade III-IV)", "The Beatles Ashram (Chaurasi Kutia)", "Lakshman & Ram Jhula", "Neer Garh Waterfall Trek"],
        "famous_foods": [
            {"dish": "Ayurvedic Sattvic Thali", "desc": "Clean, organic, wholesome vegetarian meal prepared without onion and garlic"},
            {"dish": "Garhwali Kafuli & Mandua Roti", "desc": "Traditional spinach-fenugreek leafy mash served with finger millet flatbread"},
            {"dish": "Fresh Ginger Lemon Honey Tea", "desc": "Everyday mountain cafe staple brewed with freshly crushed ginger and wild honey"},
            {"dish": "Aloo Puri at Chotiwala", "desc": "Classic pilgrimage breakfast served by the iconic heritage eatery near Ram Jhula"}
        ],
        "culture_tips": [
            "Rishikesh is a strictly vegetarian and alcohol-free sacred town by municipal law; respect this sanctuary.",
            "Only book white-water rafting with Uttarakhand Tourism-registered operators equipped with certified helmets and life jackets.",
            "Wear slip-on shoes when visiting ashrams and yoga centers as footwear is removed at entrances.",
            "Cross Ram Jhula and Janki Setu on foot or shared electric auto to soak in the river breezes."
        ],
        "how_to_reach": {
            "air": "Dehradun Jolly Grant Airport (DED) is just 21 km away (35-min cab ride).",
            "rail": "Yog Nagari Rishikesh (YNRK) and Haridwar Junction (25 km away) are linked to all major Indian cities via Vande Bharat & Shatabdi.",
            "road": "Connected via Delhi-Meerut Expressway and NH334 (5.5 hrs drive from Delhi)."
        }
    },
    {
        "id": "hampi",
        "name": "Hampi",
        "title": "Bouldered Ruins of the Vijayanagara Empire",
        "state": "Karnataka",
        "region": "South",
        "category": "Heritage & Culture",
        "best_season": "Oct - Feb (Pleasant weather)",
        "ideal_days": "2-3 days",
        "avg_daily_budget": 1900,
        "rating": 4.9,
        "coordinates": [15.3350, 76.4600],
        "image": "https://images.unsplash.com/photo-1600100397608-f010f443b772?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "The Stone Chariot at the Vijaya Vittala Temple complex, Hampi",
        "description": "A surreal UNESCO World Heritage landscape where millions of giant rust-colored granite boulders surround the colossal ruins of the 14th-century Vijayanagara Empire. Once one of the richest cities in medieval Europe and Asia, it is divided by the tranquil Tungabhadra River.",
        "highlights": ["Virupaksha Temple", "Vijaya Vittala Stone Chariot & Musical Pillars", "Matanga Hill Sunrise", "Lotus Mahal & Elephant Stables", "Coracle Boat Ride on Tungabhadra"],
        "famous_foods": [
            {"dish": "North Karnataka Jolada Rotti Oota", "desc": "Jowar flatbread with spicy brinjal curry (Ennegayi), peanut chutney, and curd"},
            {"dish": "South Indian Filter Coffee", "desc": "Strong dark chicory roast decoction served frothed with whole boiled milk in a dabarah"},
            {"dish": "Banana Leaf Thali at Mango Tree", "desc": "Wholesome regional rice meal with sambar, rasam, kootu, papad, and payasam"},
            {"dish": "Bisi Bele Bath", "desc": "Spiced rice, lentil, and vegetable mash topped with roasted cashews and hot ghee"}
        ],
        "culture_tips": [
            "Rent a bicycle (₹150/day) or scooter to comfortably explore the sprawling 41 sq km open-air museum.",
            "Climb Matanga Hill by 5:30 AM for what travelers consider one of the most breathtaking sunrises in Asia.",
            "Carry a refillable water bottle, broad-brim hat, and sunscreen; daytime granite rock heat can be intense even in winter.",
            "Take an authentic round wicker coracle boat ride near the river ghats to experience ancient river transport."
        ],
        "how_to_reach": {
            "air": "Nearest airports are Jindal Vijaynagar Airport Vidyanagar (40 km, limited) and Hubballi Airport (140 km).",
            "rail": "Hospet Junction (Hosapete - HPT) is just 13 km away, connected via overnight Hampi Express from Bengaluru.",
            "road": "Regular KSRTC Airavat luxury Volvo buses connect Hospet to Bengaluru (340 km / 7 hrs) and Goa (320 km)."
        }
    },
    {
        "id": "darjeeling",
        "name": "Darjeeling",
        "title": "Queen of the Hills, Toy Train & Kanchenjunga",
        "state": "West Bengal",
        "region": "East",
        "category": "Hill Stations & Nature",
        "best_season": "Mar - May & Oct - Dec",
        "ideal_days": "3-4 days",
        "avg_daily_budget": 2500,
        "rating": 4.7,
        "coordinates": [27.0410, 88.2663],
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Darjeeling Himalayan Railway steam locomotive running through hill curves",
        "description": "Perched at 2,050 meters against the backdrop of Mt. Kanchenjunga (the world's third highest peak), Darjeeling is synonymous with the world's most prized orthodox black teas, the UNESCO-listed steam Toy Train, and rich Tibetan and Nepali mountain culture.",
        "highlights": ["Tiger Hill Sunrise over Kanchenjunga", "Darjeeling Himalayan Railway Joyride", "Happy Valley Tea Estate", "Himalayan Mountaineering Institute & Zoo", "Batasia Loop"],
        "famous_foods": [
            {"dish": "First Flush Darjeeling Tea", "desc": "Spring harvest champagne of teas with light floral muscatel notes enjoyed black"},
            {"dish": "Steamed Pork or Vegetable Momos", "desc": "Served piping hot with fiery red Dalle Khursani chili sauce and clear soup"},
            {"dish": "Thukpa & Shaphalay", "desc": "Warm noodle soup and crispy deep-fried meat-stuffed Tibetan bread pockets"},
            {"dish": "Churpee & Gundruk", "desc": "Traditional hardened mountain cheese snack and fermented leafy green soup"}
        ],
        "culture_tips": [
            "Book your DHR Toy Train Joyride (Darjeeling to Ghum and back) weeks in advance on IRCTC as tickets sell out quickly.",
            "Leave for Tiger Hill by 4:00 AM to beat tourist vehicle traffic and secure a clear view spot before the sun rises at ~5:15 AM.",
            "Walk down to the Mall Road / Chowrasta in the evening for bookshops, local musicians, and leisurely tea tasting.",
            "Respect Buddhist customs: spin prayer wheels in a clockwise direction only."
        ],
        "how_to_reach": {
            "air": "Bagdogra Airport (IXB) is 70 km away (approx 3 hours scenic climb through tea hills).",
            "rail": "New Jalpaiguri (NJP) is the major rail junction (75 km), linked by Vande Bharat and Rajdhani from Kolkata and Delhi.",
            "road": "Shared and private 4WD taxis operate frequently between Siliguri/NJP and Darjeeling via Hill Cart Road."
        }
    },
    {
        "id": "kochi",
        "name": "Kochi",
        "title": "Spice Coast Gateway, Colonial Forts & Art Biennale",
        "state": "Kerala",
        "region": "South",
        "category": "Heritage & Coastal",
        "best_season": "Oct - Mar",
        "ideal_days": "2-3 days",
        "avg_daily_budget": 2600,
        "rating": 4.7,
        "coordinates": [9.9312, 76.2673],
        "image": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Cantilevered Chinese Fishing Nets along the Fort Kochi waterfront at sunset",
        "description": "Known as the 'Queen of the Arabian Sea', Kochi (Cochin) has been an international spice trading hub for over 600 years. Its storied heritage weaves Chinese fishing nets, Jewish synagogues, Portuguese churches, Dutch palaces, and the celebrated Kochi-Muziris Art Biennale.",
        "highlights": ["Chinese Fishing Nets at Sunset", "Mattancherry Dutch Palace", "Paradesi Synagogue & Jew Town", "Kathakali Classical Dance Performance", "Fort Kochi Heritage Art Walk"],
        "famous_foods": [
            {"dish": "Karimeen Pollichathu", "desc": "Pearl spot fish marinated in spicy shallot paste, wrapped in banana leaf and pan-roasted"},
            {"dish": "Kochi Malabar Biryani", "desc": "Fragrant Kaima rice cooked with tender meat, mild spices, fried onions, and raisins"},
            {"dish": "Appam & Alleppey Fish Curry", "desc": "Fluffy bowl-shaped rice hoppers with tangy raw-mango fish curry"},
            {"dish": "Pazham Pori", "desc": "Crispy golden ripe banana fritters enjoyed with afternoon tea at local tea shops"}
        ],
        "culture_tips": [
            "Use the Kochi Water Metro—India's first integrated electric water transit network connecting islands for just ₹20-40.",
            "Watch a Kathakali performance at the Kerala Kathakali Centre; arrive 45 minutes early to watch the artists apply intricate natural mineral makeup.",
            "Jew Town antique shops offer brassware and spices, but always check for authentic spice harvest packaging.",
            "Dress respectfully inside the active Paradesi Synagogue (bare feet, covered knees)."
        ],
        "how_to_reach": {
            "air": "Cochin International Airport (COK), the world's first fully solar-powered airport, 35 km from Fort Kochi.",
            "rail": "Ernakulam Junction (ERS) and Ernakulam Town (ERN) are major national railheads.",
            "road": "Well-connected via NH66 and NH544 with AC electric buses operated by KSRTC."
        }
    },
    {
        "id": "shillong",
        "name": "Shillong & Meghalaya",
        "title": "Abode of Clouds, Living Root Bridges & Waterfalls",
        "state": "Meghalaya",
        "region": "Northeast",
        "category": "Hill Stations & Nature",
        "best_season": "Sept - May (Clear skies & trekking)",
        "ideal_days": "4-5 days",
        "avg_daily_budget": 2900,
        "rating": 4.9,
        "coordinates": [25.5788, 91.8933],
        "image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Double Decker Living Root Bridge nestled in the rainforest of Cherrapunji",
        "description": "Known as the 'Scotland of the East', Meghalaya is blessed with pine-covered hills, the world's rainiest inhabited lands, crystal-clear Umngot River at Dawki, and ancient bio-engineering marvels: living root bridges handcrafted over centuries by the Khasi tribe.",
        "highlights": ["Double Decker Living Root Bridge (Nongriat)", "Dawki Umngot River Boat Ride", "Nohkalikai Falls (India's tallest plunge)", "Mawlynnong (Asia's Cleanest Village)", "Elephant Falls & Umiam Lake"],
        "famous_foods": [
            {"dish": "Jadoh", "desc": "Aromatic Khasi rice dish cooked with tender meat, ginger, bay leaves, and wild black sesame"},
            {"dish": "Dohneiiong", "desc": "Savory pork curry cooked with toasted black sesame seeds and rich Khasi herbs"},
            {"dish": "Tungrymbai", "desc": "Traditional fermented soybean paste sautéed with spices and served with hot rice"},
            {"dish": "Khasi Red Tea (Sha Saw)", "desc": "Light invigorating red liquor tea traditionally served in local tea stalls"}
        ],
        "culture_tips": [
            "The trek to Nongriat Double Decker bridge has ~3,500 stone steps down and up. Carry trekking poles, stay hydrated, and wear high-grip shoes.",
            "Respect the indigenous Khasi matrilineal culture and sacred groves (never take leaves or stones from Mawphlang Sacred Forest).",
            "At Dawki border river, avoid throwing any plastic wrappers or bottles into the transparent river water.",
            "Carry rain gear even in dry months as weather can shift quickly in the cloud plateau."
        ],
        "how_to_reach": {
            "air": "Umroi Airport Shillong (SHL) has select regional flights; major gateway is Lokpriya Gopinath Bordoloi Airport Guwahati (GAU), 120 km away.",
            "rail": "Guwahati Railway Station (100 km) is the primary rail junction, linked to all corners of India.",
            "road": "Shared Sumo and comfortable AC taxis commute continuously between Guwahati and Shillong via the scenic 4-lane highway (3 hrs)."
        }
    },
    {
        "id": "amritsar",
        "name": "Amritsar",
        "title": "The Golden Temple, Sacred Waters & Brave History",
        "state": "Punjab",
        "region": "North",
        "category": "Spiritual & Heritage",
        "best_season": "Oct - Mar",
        "ideal_days": "2 days",
        "avg_daily_budget": 1900,
        "rating": 4.9,
        "coordinates": [31.6340, 74.8723],
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Golden Temple shimmering across the sacred Amrit Sarovar at night",
        "description": "The spiritual and cultural center of the Sikh religion, Amritsar is home to the Harmandir Sahib (The Golden Temple). Here, the world's largest community kitchen (Langar) serves over 100,000 free meals daily to people of all backgrounds with boundless generosity.",
        "highlights": ["Harmandir Sahib (Golden Temple)", "Langar Community Kitchen Experience", "Wagah Border Beating Retreat Ceremony", "Jallianwala Bagh Memorial", "Partition Museum"],
        "famous_foods": [
            {"dish": "Amritsari Kulcha with Chole", "desc": "Flaky, crisp tandoor-baked leavened flatbread stuffed with spiced potatoes and smothered in desi ghee"},
            {"dish": "Amritsari Machhi (Fish Fry)", "desc": "Fresh river fish coated with carom seeds, chickpea batter, and deep-fried crisp"},
            {"dish": "Lassi at Ahuja / Gian", "desc": "Thick, creamy churned sweet curd served in a tall clay kulhad with a slab of malai"},
            {"dish": "Pinni & Gulab Jamun", "desc": "Traditional winter energy sweet prepared with whole wheat, dry fruits, and pure ghee"}
        ],
        "culture_tips": [
            "Cover your head at all times inside the Golden Temple complex (bandanas/scarves are provided free at entrances) and deposit shoes at the counter.",
            "Wash your hands and walk through the shallow foot-cleansing water channel before entering the marble parikrama.",
            "Participate in or observe the Langar seva (chopping vegetables or washing dishes) for a deeply moving spiritual experience.",
            "Arrive at the Wagah Border by 3:00 PM to secure good stadium seats for the 4:30 PM parade."
        ],
        "how_to_reach": {
            "air": "Sri Guru Ram Dass Jee International Airport (ATQ) is 11 km from Golden Temple, with domestic and UK/Gulf international flights.",
            "rail": "Amritsar Junction (ASR) is served by multiple daily Shatabdi, Vande Bharat, and express trains from Delhi (5.5 hrs).",
            "road": "Connected via Grand Trunk Road (NH44). Well-maintained express buses run from Chandigarh and Delhi."
        }
    },
    {
        "id": "pondicherry",
        "name": "Pondicherry (Puducherry)",
        "title": "French Colonial Riviera, Auroville & Coastal Serenity",
        "state": "Puducherry (UT)",
        "region": "South",
        "category": "Heritage & Coastal",
        "best_season": "Oct - Mar",
        "ideal_days": "2-3 days",
        "avg_daily_budget": 2400,
        "rating": 4.7,
        "coordinates": [11.9416, 79.8083],
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Pastel yellow French colonial quarters lined with bougainvillea, White Town",
        "description": "A picturesque coastal enclave on the Coromandel Coast, Puducherry preserves its distinctive French colonial legacy alongside rich Tamil heritage. Known for mustard-yellow colonial villas, seaside promenades, bohemian cafes, and the experimental spiritual township of Auroville.",
        "highlights": ["White Town Heritage Walk", "Promenade Beach Rock Beach", "Auroville & Matrimandir", "Sri Aurobindo Ashram", "Paradise Beach via Chunnambar Boat"],
        "famous_foods": [
            {"dish": "French Baguettes & Croissants", "desc": "Freshly baked artisan pastries and sourdough from traditional French bakeries like Baker Street"},
            {"dish": "Creole Fish Curry", "desc": "Unique Franco-Tamil fusion curry made with coconut milk, shallots, and mild spices"},
            {"dish": "Wood-Fired Pizza at Cafe des Arts", "desc": "Thin-crust artisan pizza baked in traditional wood ovens with local herbs"},
            {"dish": "South Indian Filter Kaapi", "desc": "Rich freshly pressed filter coffee from roadside heritage coffee stalls"}
        ],
        "culture_tips": [
            "Rent a vintage bicycle or pastel scooter to pedal leisurely through the grid-like streets of the French Quarter.",
            "Book Matrimandir inner chamber meditation passes at Auroville at least 3-5 days in advance via their official website.",
            "Promenade Beach is completely closed to motor vehicles between 6:00 PM and 7:30 AM every day for peaceful seaside strolls.",
            "Respect the peaceful silence inside Sri Aurobindo Ashram premises."
        ],
        "how_to_reach": {
            "air": "Puducherry Airport (PNY) has regional flights to Bengaluru and Hyderabad. Major international hub is Chennai (MAA), 150 km away.",
            "rail": "Puducherry Railway Station (PDY) links to Chennai, Bengaluru, and Tirupati.",
            "road": "The East Coast Road (ECR) from Chennai is one of India's most scenic coastal drives (3 hours)."
        }
    },
    {
        "id": "kaziranga",
        "name": "Kaziranga & Assam",
        "title": "Home of the Great Indian One-Horned Rhinoceros",
        "state": "Assam",
        "region": "Northeast",
        "category": "Nature & Wildlife",
        "best_season": "Nov - Apr (Park is closed during monsoon)",
        "ideal_days": "2-3 days",
        "avg_daily_budget": 3300,
        "rating": 4.8,
        "coordinates": [26.5775, 93.1711],
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80",
        "hero_caption": "Majestic one-horned rhinoceros grazing in the tall elephant grass of Kaziranga",
        "description": "A UNESCO World Heritage Site in the floodplains of the mighty Brahmaputra River, Kaziranga hosts two-thirds of the world's population of the endangered Great One-horned Rhinoceros, alongside wild water buffalo, Royal Bengal tigers, Asian elephants, and hundreds of migratory birds.",
        "highlights": ["Central Range (Kohora) Rhino Safari", "Western Range (Bagori) Jeep Safari", "Kaziranga National Orchid Park", "Brahmaputra Sunset River Cruise", "Assam Tea Garden Walk"],
        "famous_foods": [
            {"dish": "Assamese Thali with Khar & Tenga", "desc": "Traditional alkali dish made from sun-dried banana peels and tangy sour fish curry with tomato"},
            {"dish": "Masor Tenga", "desc": "Refreshing sour fish curry cooked with outenga (elephant apple) or tomatoes"},
            {"dish": "Duck Meat Curry with Ash Gourd", "desc": "Rich Assamese winter delicacy cooked with local spices and black pepper"},
            {"dish": "Assam CTC & Orthodox Black Tea", "desc": "Bold, malty breakfast tea grown in surrounding lush tea plantations"}
        ],
        "culture_tips": [
            "Book morning 6:00 AM Jeep safaris for the best wildlife photography light and animal activity.",
            "Park operates strictly from November 1 to April 30; avoid planning visits during monsoon due to Brahmaputra flooding.",
            "Visit the Kaziranga Orchid and Biodiversity Park to witness over 500 indigenous orchid species and traditional Bihu dance.",
            "Strictly follow forest guide instructions: never alight from the safari vehicle inside the sanctuary."
        ],
        "how_to_reach": {
            "air": "Nearest airports are Jorhat (97 km) and Guwahati (217 km / 4.5 hours drive via NH715).",
            "rail": "Nearest railheads are Furkating (75 km) and Jakhalabandha (40 km); Guwahati is the primary national terminal.",
            "road": "Regular ASTC state transport and private AC buses operate along the National Highway directly outside park ranges."
        }
    }
]

ATTRACTIONS = [
    # JAIPUR
    {
        "id": "amber-fort",
        "destination_id": "jaipur",
        "name": "Amber Fort & Palace",
        "category": "Monument",
        "entry_fee_inr": 100,
        "entry_fee_foreign": 500,
        "timings": "8:00 AM - 5:30 PM, Light Show: 7:00 PM",
        "ideal_duration": "3 hours",
        "coordinates": [26.9855, 75.8513],
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
        "description": "Constructed from yellow and pink sandstone and white marble, this 16th-century fortress overlooks Maota Lake. Inside, the Sheesh Mahal (Mirror Palace) dazzles with convex glass mirrors imported from Belgium.",
        "insider_tip": "Reach by 8:30 AM before the tour buses arrive. Walk through the underground tunnel linking Amber to Jaigarh Fort."
    },
    {
        "id": "hawa-mahal",
        "destination_id": "jaipur",
        "name": "Hawa Mahal (Palace of Winds)",
        "category": "Monument",
        "entry_fee_inr": 50,
        "entry_fee_foreign": 200,
        "timings": "9:00 AM - 5:00 PM",
        "ideal_duration": "1 hour",
        "coordinates": [26.9239, 75.8267],
        "image": "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=800&q=80",
        "description": "A five-story pyramid-shaped pink palace featuring 953 intricately carved jharokhas (casements). It was designed to allow royal women to observe street festivals without being seen from outside.",
        "insider_tip": "Cross the street to the rooftop 'Tattoo Cafe' or 'Wind View Cafe' for the iconic unobstructed frontal photograph."
    },
    {
        "id": "jantar-mantar-jaipur",
        "destination_id": "jaipur",
        "name": "Jantar Mantar Astronomical Observatory",
        "category": "Heritage",
        "entry_fee_inr": 50,
        "entry_fee_foreign": 200,
        "timings": "9:00 AM - 5:00 PM",
        "ideal_duration": "1.5 hours",
        "coordinates": [26.9196, 75.8243],
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
        "description": "A collection of 19 monumental architectural astronomical instruments built by Sawai Jai Singh II, featuring the world's largest stone sundial (Samrat Yantra) with 2-second accuracy.",
        "insider_tip": "Hire an authorized audio guide or official guide to comprehend the incredible mathematical ingenuity."
    },
    # VARANASI
    {
        "id": "dashashwamedh-ghat",
        "destination_id": "varanasi",
        "name": "Dashashwamedh Ghat & Evening Aarti",
        "category": "Spiritual",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "Open 24 hours; Aarti starts 6:30 PM (Winter) / 7:00 PM (Summer)",
        "ideal_duration": "2 hours",
        "coordinates": [25.3076, 83.0104],
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
        "description": "The main and most vibrant ghat on the Ganges. Every evening, young priests in ceremonial robes perform the Grand Ganga Aarti with multi-tiered brass oil lamps, conch shells, and incense.",
        "insider_tip": "Hire a shared wooden boat by 5:30 PM to anchor on the river facing the ghat for an unobstructed view of the aarti."
    },
    {
        "id": "kashi-vishwanath",
        "destination_id": "varanasi",
        "name": "Kashi Vishwanath Temple & Corridor",
        "category": "Spiritual",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "4:00 AM - 11:00 PM",
        "ideal_duration": "2 hours",
        "coordinates": [25.3109, 83.0107],
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
        "description": "Dedicated to Lord Shiva, this sacred Jyotirlinga shrine has drawn pilgrims for millennia. The recently renovated corridor seamlessly connects the sanctum directly to the Ganga ghats.",
        "insider_tip": "Electronic gadgets, mobile phones, leather belts, and pens are prohibited. Use the verified locker facilities outside Gate 4."
    },
    {
        "id": "sarnath",
        "destination_id": "varanasi",
        "name": "Sarnath Buddhist Deer Park & Dhamek Stupa",
        "category": "Heritage",
        "entry_fee_inr": 25,
        "entry_fee_foreign": 300,
        "timings": "9:00 AM - 5:00 PM",
        "ideal_duration": "2.5 hours",
        "coordinates": [25.3811, 83.0214],
        "image": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
        "description": "Located 10 km northeast of Varanasi, this is the holy site where Gautama Buddha delivered his first sermon (Dhammacakkappavattana Sutta) after attaining enlightenment.",
        "insider_tip": "Do not miss the Sarnath Archaeological Museum housing the original 3rd-century BCE Lion Capital of Ashoka (India's national emblem)."
    },
    # MUNNAR
    {
        "id": "eravikulam-national-park",
        "destination_id": "munnar",
        "name": "Eravikulam National Park (Rajamalai)",
        "category": "Wildlife & Nature",
        "entry_fee_inr": 200,
        "entry_fee_foreign": 500,
        "timings": "7:30 AM - 4:00 PM (Closed Feb-Mar for calving)",
        "ideal_duration": "3 hours",
        "coordinates": [10.2000, 77.0800],
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "description": "Home to the largest surviving population of the endangered Nilgiri Tahr (mountain goat) and the Anamudi peak (2,695m), the highest mountain peak in South India.",
        "insider_tip": "Book entry tickets online at eravikulamnationalpark.in in advance to avoid 2-hour queue at the safari bus boarding point."
    },
    {
        "id": "mattupetty-dam",
        "destination_id": "munnar",
        "name": "Mattupetty Dam & Speedboat Lake",
        "category": "Nature",
        "entry_fee_inr": 20,
        "entry_fee_foreign": 50,
        "timings": "9:30 AM - 5:00 PM",
        "ideal_duration": "1.5 hours",
        "coordinates": [10.1062, 77.1246],
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "description": "A gravity masonry dam nestled among tea estates where travelers enjoy speedboat rides, serene pine forest walks, and frequent sightings of wild elephant herds drinking by the water.",
        "insider_tip": "Combine with Echo Point (5 km further ahead) where your voice naturally rebounds off the surrounding green hill ranges."
    },
    # GOA
    {
        "id": "basilica-bom-jesus",
        "destination_id": "goa",
        "name": "Basilica of Bom Jesus (Old Goa)",
        "category": "Heritage",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "9:00 AM - 6:30 PM (Sundays open 10:30 AM)",
        "ideal_duration": "1.5 hours",
        "coordinates": [15.5009, 73.9116],
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
        "description": "A 400-year-old Baroque Catholic basilica holding the mortal sacred relics of St. Francis Xavier. A UNESCO World Heritage Site with distinctive laterite stone architecture.",
        "insider_tip": "Visit Se Cathedral directly across the road, renowned for its golden bell, one of the finest and largest bells in the world."
    },
    {
        "id": "palolem-beach",
        "destination_id": "goa",
        "name": "Palolem Beach & Butterfly Beach",
        "category": "Beaches",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "Open 24 hours",
        "ideal_duration": "Half day",
        "coordinates": [15.0100, 74.0232],
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
        "description": "A crescent-shaped beach fringed by shady coconut palms and calm swimmable waters in South Goa. Take a traditional fiber boat out to secluded Butterfly Beach and spot playful dolphins.",
        "insider_tip": "Rent a kayak at high tide (₹200/hr) and paddle along the tranquil northern backwater estuary towards Monkey Island."
    },
    # AGRA
    {
        "id": "taj-mahal",
        "destination_id": "agra",
        "name": "Taj Mahal",
        "category": "Wonder of the World",
        "entry_fee_inr": 50,
        "entry_fee_foreign": 1100,
        "timings": "30 mins before sunrise until 30 mins before sunset (CLOSED FRIDAYS)",
        "ideal_duration": "3 hours",
        "coordinates": [27.1751, 78.0421],
        "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
        "description": "Commissioned by Mughal Emperor Shah Jahan in 1632 in memory of his beloved wife Mumtaz Mahal. Built with translucent white Makrana marble and pietra dura gemstone inlays.",
        "insider_tip": "Enter through the East Gate at 5:45 AM for sunrise. The morning light casts a golden-rose glow on the marble with minimal tourists."
    },
    {
        "id": "agra-fort",
        "destination_id": "agra",
        "name": "Agra Fort (Red Fort)",
        "category": "Monument",
        "entry_fee_inr": 50,
        "entry_fee_foreign": 650,
        "timings": "6:00 AM - 6:00 PM",
        "ideal_duration": "2 hours",
        "coordinates": [27.1795, 78.0211],
        "image": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
        "description": "The primary residence of the emperors of the Mughal Dynasty until 1638. A massive red sandstone fortress with Jahangiri Mahal, Diwan-i-Khas, and the Musamman Burj balcony overlooking the Taj.",
        "insider_tip": "Stand inside Musamman Burj where Shah Jahan spent his final captive years gazing at his beloved Taj Mahal across the river."
    },
    # LEH LADAKH
    {
        "id": "pangong-tso",
        "destination_id": "ladakh",
        "name": "Pangong Tso Lake",
        "category": "Nature & Adventure",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "Daylight hours (ILP permit required)",
        "ideal_duration": "Full day / overnight camp",
        "coordinates": [33.7595, 78.6674],
        "image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=800&q=80",
        "description": "An endorheic high-altitude salt lake situated at 4,350 meters extending from India to Tibet. The water shifts through hues of turquoise, cobalt blue, and jade green throughout the day.",
        "insider_tip": "Stay overnight in eco-cottages at Spangmik for stargazing under crystal clear pollution-free Milky Way skies."
    },
    {
        "id": "thiksey-monastery",
        "destination_id": "ladakh",
        "name": "Thiksey Monastery (Mini Potala)",
        "category": "Spiritual & Heritage",
        "entry_fee_inr": 30,
        "entry_fee_foreign": 50,
        "timings": "7:00 AM - 7:00 PM",
        "ideal_duration": "2 hours",
        "coordinates": [34.0583, 77.6667],
        "image": "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?auto=format&fit=crop&w=800&q=80",
        "description": "A 12-story Gelugpa sect monastery perched dramatically on a hill resemblance to Lhasa's Potala Palace. Houses a magnificent 15-meter tall statue of the Maitreya (Future) Buddha.",
        "insider_tip": "Arrive at 6:30 AM to witness the monk's morning assembly prayer with deep Tibetan horns, drums, and butter tea."
    },
    # HAMPI
    {
        "id": "vittala-temple",
        "destination_id": "hampi",
        "name": "Vijaya Vittala Temple & Stone Chariot",
        "category": "Heritage & Monument",
        "entry_fee_inr": 40,
        "entry_fee_foreign": 600,
        "timings": "8:30 AM - 5:30 PM",
        "ideal_duration": "2.5 hours",
        "coordinates": [15.3350, 76.4760],
        "image": "https://images.unsplash.com/photo-1600100397608-f010f443b772?auto=format&fit=crop&w=800&q=80",
        "description": "The pinnacle of Vijayanagara architectural art, famous for its iconic Stone Chariot (depicted on the ₹50 currency note) and the Ranga Mantapa musical stone pillars that resonate with musical notes.",
        "insider_tip": "Electric buggies (₹20) run from the parking area to the temple gate for visitors who prefer not to walk the 1 km sandy path in afternoon heat."
    },
    # AMRITSAR
    {
        "id": "golden-temple",
        "destination_id": "amritsar",
        "name": "Harmandir Sahib (The Golden Temple)",
        "category": "Spiritual",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "Open 24 hours",
        "ideal_duration": "3-4 hours",
        "coordinates": [31.6200, 74.8765],
        "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
        "description": "The holiest Gurdwara of Sikhism, plated with pure gold leaf and surrounded by the sacred pool (Amrit Sarovar). Welcomes all people regardless of religion, caste, or nationality.",
        "insider_tip": "Visit twice: once at sunset to see the marble reflections and again around 10:00 PM for the sacred Palki Sahib night procession."
    },
    # PONDICHERRY
    {
        "id": "auroville-matrimandir",
        "destination_id": "pondicherry",
        "name": "Matrimandir & Auroville Visitor Centre",
        "category": "Spiritual & Architecture",
        "entry_fee_inr": 0,
        "entry_fee_foreign": 0,
        "timings": "9:00 AM - 4:00 PM (Pass required for inner meditation chamber)",
        "ideal_duration": "3 hours",
        "coordinates": [12.0070, 79.8106],
        "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
        "description": "A golden geodesic dome designed as a universal spiritual sanctuary for silent concentration, featuring a 70 cm pure optical crystal globe fed by natural sunlight.",
        "insider_tip": "The viewing point walk is free with a pass from the Visitor's Centre; inner chamber meditation requires booking online 3-5 days prior."
    }
]

TRANSPORT_ROUTES = [
    {
        "origin": "Delhi",
        "destination": "Jaipur",
        "distance_km": 280,
        "options": [
            {
                "mode": "Train (Vande Bharat / Shatabdi)",
                "duration": "3h 45m - 4h 30m",
                "fare_range": "₹850 - ₹1,650",
                "comfort_rating": 4.9,
                "frequency": "Multiple trains daily",
                "booking_tip": "Book Vande Bharat (Train 20978) or Ajmer Shatabdi. Meals are included in the ticket.",
                "best_for": "Best balance of speed, comfort, and city-center arrival"
            },
            {
                "mode": "Flight",
                "duration": "55 mins (flight) + 2.5h airport procedures",
                "fare_range": "₹2,200 - ₹4,500",
                "comfort_rating": 4.2,
                "frequency": "4-6 flights daily",
                "booking_tip": "IndiGo / Air India from Terminal 2 or 3. Useful primarily if connecting from an international flight.",
                "best_for": "Connecting air passengers"
            },
            {
                "mode": "Expressway Cab / Self-Drive",
                "duration": "4h - 4h 30m",
                "fare_range": "₹3,200 - ₹4,500 (Sedan/SUV)",
                "comfort_rating": 4.5,
                "frequency": "On-demand (Uber Intercity / MakeMyTrip)",
                "booking_tip": "Use the new Delhi-Mumbai Expressway via Sohna for smooth 6-lane cruising.",
                "best_for": "Families, small groups carrying lots of luggage"
            },
            {
                "mode": "AC Volvo Bus",
                "duration": "5h - 6h",
                "fare_range": "₹450 - ₹900",
                "comfort_rating": 4.0,
                "frequency": "Every 30 mins from Bikaner House & ISBT",
                "booking_tip": "Rajasthan Roadways RSRTC Scania or Zingbus booked via RedBus.",
                "best_for": "Budget travelers & solo backpackers"
            }
        ]
    },
    {
        "origin": "Delhi",
        "destination": "Agra",
        "distance_km": 210,
        "options": [
            {
                "mode": "Gatimaan Express Train",
                "duration": "1h 40m",
                "fare_range": "₹750 - ₹1,500",
                "comfort_rating": 5.0,
                "frequency": "Runs daily except Fridays (departs Hazrat Nizamuddin 8:10 AM)",
                "booking_tip": "India's fastest heritage tourist train. Hostess service and hot breakfast served onboard.",
                "best_for": "Day trip to Taj Mahal without highway traffic"
            },
            {
                "mode": "Yamuna Expressway Cab",
                "duration": "3h - 3h 30m",
                "fare_range": "₹2,600 - ₹3,800",
                "comfort_rating": 4.6,
                "frequency": "On demand",
                "booking_tip": "Seamless expressway driving. Stop at the modern expressway rest plazas for breakfast.",
                "best_for": "Door-to-door convenience"
            },
            {
                "mode": "Taj Express / Superfast Train",
                "duration": "2h 30m - 3h",
                "fare_range": "₹250 - ₹650",
                "comfort_rating": 4.1,
                "frequency": "Frequent trains from New Delhi Station",
                "booking_tip": "Book AC Chair Car (CC) on IRCTC for quick inexpensive travel.",
                "best_for": "Budget conscious day-trippers"
            }
        ]
    },
    {
        "origin": "Mumbai",
        "destination": "Goa",
        "distance_km": 590,
        "options": [
            {
                "mode": "Flight",
                "duration": "1h 15m",
                "fare_range": "₹2,400 - ₹5,000",
                "comfort_rating": 4.7,
                "frequency": "15+ flights daily to GOI (Dabolim) and GOX (Mopa)",
                "booking_tip": "Book 3 weeks in advance. Fly to GOX for North Goa beaches, or GOI for South Goa.",
                "best_for": "Quickest and most comfortable"
            },
            {
                "mode": "Vande Bharat / Tejas Express (Konkan Rail)",
                "duration": "7h 45m - 8h 30m",
                "fare_range": "₹1,400 - ₹2,900",
                "comfort_rating": 4.9,
                "frequency": "6 days a week from CSMT Mumbai",
                "booking_tip": "Spectacular panoramic journey crossing dozens of Western Ghats tunnels, viaducts, and waterfalls.",
                "best_for": "Scenic rail enthusiasts"
            },
            {
                "mode": "Overnight Sleeper Bus",
                "duration": "12h - 14h",
                "fare_range": "₹800 - ₹1,800",
                "comfort_rating": 3.8,
                "frequency": "30+ operators departing evening from Borivali/Dadar",
                "booking_tip": "Choose multi-axle AC Volvo/Scania sleeper (e.g. Paulo, Intrcity SmartBus).",
                "best_for": "Saves one night hotel accommodation"
            }
        ]
    },
    {
        "origin": "Bengaluru",
        "destination": "Munnar",
        "distance_km": 475,
        "options": [
            {
                "mode": "Train to Aluva/Ernakulam + Scenic Taxi",
                "duration": "9h train + 3.5h hill drive",
                "fare_range": "₹1,200 (Train 3A) + ₹2,800 (Hill Cab)",
                "comfort_rating": 4.5,
                "frequency": "Daily overnight trains from KSR Bengaluru",
                "booking_tip": "Board Kanyakumari Express or Kochuveli AC Express at night; wake up in Kerala at dawn.",
                "best_for": "Relaxed overnight journey avoiding long bus curves"
            },
            {
                "mode": "Direct AC Sleeper Bus",
                "duration": "10h - 11h",
                "fare_range": "₹950 - ₹1,700",
                "comfort_rating": 4.1,
                "frequency": "Direct night buses from Madiwala/Electronic City",
                "booking_tip": "KSRTC Airavat or private AC sleeper. Book lower berths for smoother mountain curves.",
                "best_for": "Direct door-to-hill connectivity without vehicle transfers"
            },
            {
                "mode": "Flight to Kochi (COK) + Cab",
                "duration": "1h flight + 3.5h scenic drive",
                "fare_range": "₹2,300 (flight) + ₹3,000 (prepaid airport taxi)",
                "comfort_rating": 4.8,
                "frequency": "Multiple daily direct flights",
                "booking_tip": "Pre-book airport taxi from official CIAL counter inside arrivals for transparent fixed rates.",
                "best_for": "Maximum speed and comfort"
            }
        ]
    },
    {
        "origin": "Delhi",
        "destination": "Varanasi",
        "distance_km": 820,
        "options": [
            {
                "mode": "Vande Bharat Express (Train 22436)",
                "duration": "8 hours",
                "fare_range": "₹1,750 (CC) - ₹3,300 (EC)",
                "comfort_rating": 4.9,
                "frequency": "Daily except Thursdays (departs NDLS 6:00 AM)",
                "booking_tip": "Leaves early morning, arrives in Varanasi at 2:00 PM in time for evening Aarti. Clean, fast, and on-time.",
                "best_for": "Premier rail journey in India"
            },
            {
                "mode": "Flight",
                "duration": "1h 20m",
                "fare_range": "₹2,800 - ₹5,500",
                "comfort_rating": 4.6,
                "frequency": "8+ flights daily",
                "booking_tip": "Book morning flights to maximize your time along the ghats.",
                "best_for": "Fastest option"
            },
            {
                "mode": "Overnight Rajdhani / Shiv Ganga Express",
                "duration": "11h - 12h",
                "fare_range": "₹1,400 (3A) - ₹3,200 (1A)",
                "comfort_rating": 4.6,
                "frequency": "Daily night departures",
                "booking_tip": "Book Shiv Ganga Express (12560); extremely punctual and clean sleeper train.",
                "best_for": "Overnight travel saving hotel cost"
            }
        ]
    }
]

PRACTICAL_GUIDE = {
    "visas": {
        "title": "Indian Tourist Visa (e-Visa)",
        "summary": "India provides convenient electronic visas (e-Tourist Visa) for citizens of over 165 countries.",
        "points": [
            {"label": "Official Portal", "val": "Apply ONLY at the official government website: indianvisaonline.gov.in (beware of fake commercial duplicate sites)."},
            {"label": "Categories", "val": "30-day double entry (approx $25 in high season, $10 in low season), 1-year multiple entry ($40), and 5-year multiple entry ($80)."},
            {"label": "Processing Time", "val": "Usually processed within 72 to 96 hours. Apply at least 4 to 7 days before your scheduled flight."},
            {"label": "Entry Points", "val": "Valid for arrival at 29 designated international airports and 5 major seaports."}
        ]
    },
    "currency_and_upi": {
        "title": "Currency, UPI & Digital Payments",
        "summary": "India has the world's most advanced digital payment ecosystem, but carrying cash remains helpful for small town markets.",
        "points": [
            {"label": "Currency", "val": "Indian Rupee (INR - ₹). Common banknote denominations: ₹10, ₹20, ₹50, ₹100, ₹200, ₹500."},
            {"label": "UPI for International Visitors", "val": "Foreign tourists can now obtain 'UPI One World' wallet accounts at major international airports (Delhi, Mumbai, Bengaluru) via authorized PPI issuers."},
            {"label": "Credit/Debit Cards", "val": "Visa & Mastercard are widely accepted at hotels, restaurants, and supermarkets. American Express has limited acceptance."},
            {"label": "ATM Usage", "val": "Use ATMs attached to reputable national bank branches (SBI, HDFC, ICICI, Axis). Always decline ATM currency conversion and choose 'Charge in INR'."},
            {"label": "Tipping Culture", "val": "Restaurants: 7-10% if no service charge is included. Porters: ₹50-100. Guides/Drivers: ₹300-500/day."}
        ]
    },
    "sim_and_connectivity": {
        "title": "SIM Cards, eSIM & Internet",
        "summary": "Getting connected in India is affordable with world-class 5G coverage across cities.",
        "points": [
            {"label": "Airport Counters", "val": "Airtel and Jio offer tourist SIM kiosks right in international arrival halls. Requires original passport, visa copy, and a passport-size photo."},
            {"label": "eSIM Options", "val": "Airalo, Nomad, and Holafly offer convenient digital eSIMs without physical paperwork for immediate connectivity on arrival."},
            {"label": "Cost & Data", "val": "A 28-day local tourist pack costs approx ₹300-450 (~$4-5 USD) for 1.5GB to 2GB high-speed 5G data per day plus unlimited local calls."},
            {"label": "Emergency Number", "val": "Dial 112 for all-in-one emergency dispatch (Police, Fire, Ambulance) anywhere in India."}
        ]
    },
    "cultural_etiquette": {
        "title": "Cultural Norms & Temple Etiquette",
        "summary": "India is diverse and warm, with traditions varying across states.",
        "points": [
            {"label": "Temple Dress Code", "val": "Dress modestly when entering temples, mosques, and gurdwaras. Keep shoulders and knees covered. Remove shoes outside."},
            {"label": "Greetings", "val": "A folded-hands 'Namaste' or 'Namaskar' is universally respected and appreciated everywhere."},
            {"label": "Right Hand Rule", "val": "Traditionally, use your right hand when giving or receiving money, gifts, and food."},
            {"label": "Photography", "val": "Always ask permission before taking portraits of locals, sadhus (ascetics), or inside sanctum sanctorums."}
        ]
    },
    "safety_and_health": {
        "title": "Health, Food Safety & Scams to Avoid",
        "summary": "Sensible travel precautions ensure a safe, memorable, and trouble-free trip.",
        "points": [
            {"label": "Drinking Water", "val": "Drink only sealed bottled water (reputable brands: Kinley, Aquafina, Bisleri) or filtered/purified water. Avoid tap water and ice cubes from street carts."},
            {"label": "Street Food Guide", "val": "Eat at street stalls that have long local queues and where food is prepared piping hot in front of you. Avoid pre-cut cut fruits exposed to air."},
            {"label": "Touts & Taxi Scams", "val": "At railway stations and airports, use pre-paid taxi booths or ride apps (Uber, Ola). Ignore touts claiming your hotel is burned down or closed."},
            {"label": "Emergency Helpline Numbers", "val": "National Emergency: 112 | 24x7 Multi-lingual Tourist Helpline: 1363 | Women Helpline: 1091 | Railway Protection: 139"}
        ]
    }
}

PACKING_ITEMS = [
    {"id": "doc1", "category": "Documents", "item": "Passport & valid Indian e-Visa printouts (carry 2 copies)", "essential": True},
    {"id": "doc2", "category": "Documents", "item": "Travel & medical insurance policy document with emergency contact", "essential": True},
    {"id": "doc3", "category": "Documents", "item": "Passport-sized physical photos (helpful for permits/SIM cards)", "essential": False},
    {"id": "doc4", "category": "Documents", "item": "Printed copies of confirmed train & hotel reservations", "essential": True},
    
    {"id": "clo1", "category": "Clothing", "item": "Lightweight, breathable cotton / linen clothing for tropical climates", "essential": True},
    {"id": "clo2", "category": "Clothing", "item": "Light shawl / scarf / dupatta (essential for covering head/shoulders in temples)", "essential": True},
    {"id": "clo3", "category": "Clothing", "item": "Comfortable slip-on walking shoes (easy removal at temple entrances)", "essential": True},
    {"id": "clo4", "category": "Clothing", "item": "Warm fleece jacket / thermal layer (for North India winters or Ladakh/hills)", "essential": False},
    {"id": "clo5", "category": "Clothing", "item": "UV sunglasses and broad-brim sun hat", "essential": False},

    {"id": "med1", "category": "Health & First Aid", "item": "Electrolyte powder sachets (ORS) for hydration in warm weather", "essential": True},
    {"id": "med2", "category": "Health & First Aid", "item": "Mosquito & insect repellent (DEET or Odomos herbal lotion)", "essential": True},
    {"id": "med3", "category": "Health & First Aid", "item": "Hand sanitizer & biodegradable wet wipes", "essential": True},
    {"id": "med4", "category": "Health & First Aid", "item": "Digestive enzyme / stomach relief medication (e.g. Loperamide)", "essential": True},
    {"id": "med5", "category": "Health & First Aid", "item": "Personal prescription medications in original labeled containers", "essential": True},

    {"id": "tech1", "category": "Electronics", "item": "Type D / Type C universal plug adapter (India standard 230V, 50Hz)", "essential": True},
    {"id": "tech2", "category": "Electronics", "item": "High-capacity power bank (10,000 to 20,000 mAh) for long train rides", "essential": True},
    {"id": "tech3", "category": "Electronics", "item": "Offline Google Maps downloaded for destination cities", "essential": True},
    {"id": "tech4", "category": "Electronics", "item": "Noise-canceling earphones / earplugs for peaceful sleep during transit", "essential": False}
]
