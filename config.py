"""
config.py
Application configuration settings for Personalized AI Tourist Guide.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "travel-india-secure-key-2026-prod")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DATABASE = os.path.join(os.path.dirname(__file__), "travel_guide.db")
