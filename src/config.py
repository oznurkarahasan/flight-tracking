import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # İstanbul (IST/SAW), Ankara (ESB), İzmir (ADB)
    ORIGINS = ["IST", "SAW", "ESB", "ADB"]
    DESTINATION = "AMS"
    
    DATE_RANGES = [
        ("2026-08-01", "2026-08-07"),
        ("2027-01-20", "2027-01-30")
    ]